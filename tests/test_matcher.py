import pandas as pd
import pytest

from src.database import setup_database, populate_database
from src.matcher import DataAnalyzer


@pytest.fixture
def test_data():
    """Create test data"""
    train = pd.DataFrame({
        'x': [1, 2, 3],
        'y1': [2, 4, 6],
        'y2': [1, 2, 3],
        'y3': [0, 0, 0],
        'y4': [10, 20, 30]
    })
    
    ideal = pd.DataFrame({
        'x': [1, 2, 3],
        **{f'y{i}': [float(i*j) for j in [1, 2, 3]] for i in range(1, 51)}
    })
    
    return train, ideal


def test_database_setup():
    """Test database creation"""
    engine, session = setup_database('sqlite:///:memory:')
    assert engine is not None
    assert session is not None
    session.close()


def test_data_loading(test_data):
    """Test data loading into database"""
    train, ideal = test_data
    engine, session = setup_database('sqlite:///:memory:')
    populate_database(session, train, ideal)
    
    result = pd.read_sql('SELECT * FROM training_data', engine)
    assert len(result) == 3
    session.close()


def test_function_selection(test_data):
    """Test ideal function selection"""
    train, ideal = test_data
    engine, session = setup_database('sqlite:///:memory:')
    populate_database(session, train, ideal)
    
    analyzer = DataAnalyzer('sqlite:///:memory:')
    analyzer.session = session
    chosen = analyzer.select_best_ideal_functions()
    
    assert len(chosen) == 4
    assert 'y1' in chosen
    analyzer.close()


def test_mapping_requires_selection():
    """Test that mapping requires function selection first"""
    analyzer = DataAnalyzer('sqlite:///:memory:')
    
    with pytest.raises(Exception):
        analyzer.map_test_data()
    
    analyzer.close()
