**Student Name:** Asif Iqbal  
**Student ID:** 10245789    
**Course:** M.Sc. Data Science   
**University:** IU International University

# Programming With Python: Ideal Function Matcher

Python program for matching mathematical functions using least squares and sqrt(2) threshold criteria.  

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Place CSV files in `data/` directory:
- `train.csv` - Training data (4 functions)
- `ideal.csv` - Ideal functions (50 functions)
- `test.csv` - Test data points

Run:
```bash
python -m src.main
```

## Testing

```bash
pytest tests/
```

## Output

- `mapped_data.db` - SQLite database with results
- `results.html` - Interactive Bokeh visualization
