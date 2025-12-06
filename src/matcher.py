import csv
import math

import pandas as pd

from src.database import TestResults, setup_database


class DataAnalyzer:
    """Main class for function matching analysis"""
    
    def __init__(self, db_path='sqlite:///mapped_data.db'):
        self.db_path = db_path
        self.engine, self.session = setup_database(db_path)
        self.chosen_functions = {}
        self.max_deviations = {}
    
    def select_best_ideal_functions(self):
        """
        Select 4 best ideal functions using the least squares criterion
        """
        training_data = pd.read_sql('SELECT * FROM training_data', self.engine)
        ideal_data = pd.read_sql('SELECT * FROM ideal_functions', self.engine)
        
        training_cols = ['y1', 'y2', 'y3', 'y4']
        ideal_cols = [f'y{i}' for i in range(1, 51)]
        
        for train_col in training_cols:
            min_sse = float('inf')
            best_ideal = None
            
            for ideal_col in ideal_cols:
                sse = ((training_data[train_col] - ideal_data[ideal_col]) ** 2).sum()
                if sse < min_sse:
                    min_sse = sse
                    best_ideal = ideal_col
            
            self.chosen_functions[train_col] = best_ideal
            deviations = abs(training_data[train_col] - ideal_data[best_ideal])
            self.max_deviations[train_col] = deviations.max()
            
            print(f"{train_col} -> {best_ideal} (SSE: {min_sse:.4f})")
        
        return self.chosen_functions
    
    def map_test_data(self, test_csv_path='../data/test.csv'):
        """
        Map test data to chosen ideal functions
        """
        if not self.chosen_functions:
            raise Exception("Must select ideal functions first")
        
        ideal_data = pd.read_sql('SELECT * FROM ideal_functions', self.engine)
        results = []
        
        with open(test_csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for line in reader:
                x_test = float(line['x'])
                y_test = float(line['y'])
                
                closest_idx = (ideal_data['x'] - x_test).abs().idxmin()
                ideal_row = ideal_data.iloc[closest_idx]
                
                best_match = None
                min_dev = float('inf')
                
                for train_func, ideal_func in self.chosen_functions.items():
                    deviation = abs(y_test - ideal_row[ideal_func])
                    threshold = self.max_deviations[train_func] * math.sqrt(2)
                    
                    if deviation <= threshold and deviation < min_dev:
                        min_dev = deviation
                        func_num = int(ideal_func[1:])
                        best_match = {
                            'x': x_test,
                            'y': y_test,
                            'delta_y': deviation,
                            'function_id': ideal_func,
                            'func_num': func_num
                        }
                
                if best_match:
                    results.append(best_match)
                    result = TestResults(
                        x=best_match['x'],
                        y=best_match['y'],
                        delta_y=best_match['delta_y'],
                        ideal_func_num=best_match['func_num']
                    )
                    self.session.add(result)
        
        self.session.commit()
        results_df = pd.DataFrame(results)
        print(f"Mapped {len(results_df)} test points")
        return results_df
    
    def close(self):
        """Close database session"""
        if self.session:
            self.session.close()


def run_analysis(db_path='sqlite:///mapped_data.db'):
    """
    Run complete analysis workflow
    """
    analyzer = DataAnalyzer(db_path)
    
    print("\nSelecting ideal functions...")
    chosen = analyzer.select_best_ideal_functions()
    
    print("\nMapping test data...")
    results = analyzer.map_test_data()
    
    analyzer.close()
    return chosen, results
