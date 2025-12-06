import os

import pandas as pd


def load_csvs():
    """
    Load train, ideal, and test CSV files
    """
    data_dir = os.path.join(os.path.dirname(__file__), '../data')
    
    train = pd.read_csv(os.path.join(data_dir, 'train.csv'))
    ideal = pd.read_csv(os.path.join(data_dir, 'ideal.csv'))
    test = pd.read_csv(os.path.join(data_dir, 'test.csv'))
    
    return train, ideal, test
