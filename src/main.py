import pandas as pd
import os

# SMART PATH FIX: This finds the data folder no matter where you run the script from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "sample_transactions.csv")

def load_data(path: str) -> pd.DataFrame:
    """Load transaction data from CSV."""
    return pd.read_csv(path)

def flag_risks(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    
    # Convert date so we can find weekends
    df["date"] = pd.to_datetime(df["date"])
    
    # Existing rules
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["flag_missing_amount"] = df["amount"].isna()
    df["flag_missing_vendor"] = df["vendor"].isna() | (df["vendor"].astype(str).str.strip() == "")
    
    # Weekend rule
    df["flag_weekend"] = df["date"].dt.weekday > 4 
    
    key_cols = ["date", "amount", "vendor", "department"]
    df["flag_duplicate"] = df.duplicated(subset=key_cols, keep=False)
    df["flag_high_amount"] = df["amount"].fillna(0) >= 5000

    # Overall flag
    df["flag_any_risk"] = (
        df["flag_missing_amount"]
        | df["flag_missing_vendor"]
        | df["flag_duplicate"]
        | df["flag_high_amount"]
        | df["flag_weekend"]
    )
    return df

def print_summary(df: pd.DataFrame) -> None:
    total = len(df)
    flagged = int(df["flag_any_risk"].sum())

    print("=== AI Risk Anomaly Detector (v0.1) ===")
    print(f"Total transactions: {total}")
    print(f"Flagged transactions: {flagged}")
    print(f"- Weekend transactions: {int(df['flag_weekend'].sum())}") # Displays the new count
    # ... rest of your print code ...

def main() -> None:
    df = load_data(DATA_PATH)
    df_flagged = flag_risks(df)
    print_summary(df_flagged)

if __name__ == "__main__":
    main()
