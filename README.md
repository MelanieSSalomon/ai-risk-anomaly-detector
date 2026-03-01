# AI Risk Anomaly Detector

## Purpose
This project uses Python to assist in identifying anomalous financial transactions that may indicate audit or compliance risk.

## Why this matters (Risk & Audit)
In large datasets, risky transactions can be missed during manual reviews. This tool demonstrates how AI-assisted logic can help auditors and risk teams flag irregular patterns early, improving accuracy and efficiency.

## What this project does
- Reads transaction data from a CSV file  
- Cleans and validates financial data  
- Flags potentially high-risk transactions based on defined rules  
- Produces a simple risk summary for review
## Tech used
- Python
- pandas (data cleaning and analysis)
- CSV files (sample transaction data)

## How to run
1) Install Python 3.x  
2) Download this repo and unzip it  
3) Open a terminal in the project folder  
4) Install dependencies:
```bash
python -m pip install -r requirements.txt

```Install dependencies: pip install pandas (or the sudo version we used).

Run the app: python3 src/main.py.
## Example output


```text
Total transactions: 10
Flagged transactions: 5

Flag counts:
- Missing amount: 1
- Missing vendor: 1
- Duplicate transactions: 2
- High amount (>= 5000): 3
- Weekend orders: 3
```

