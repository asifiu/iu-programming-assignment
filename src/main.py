from src.database import setup_database, populate_database
from src.dataloader import load_csvs
from src.matcher import run_analysis
from src.plotter import plot_results


def main():
    """Main execution function"""
    
    print("Loading CSV files...")
    train_df, ideal_df, test_df = load_csvs()
    print(f"Training: {train_df.shape}, Ideal: {ideal_df.shape}, Test: {test_df.shape}")
    
    print("\nSetting up database...")
    engine, session = setup_database()
    populate_database(session, train_df, ideal_df)
    
    print("\nRunning analysis...")
    chosen_functions, results_df = run_analysis()
    
    print("\nCreating visualization...")
    plot_results(train_df, ideal_df, test_df, results_df, chosen_functions)
    
    print("\nAnalysis complete!")
    session.close()


if __name__ == "__main__":
    main()
