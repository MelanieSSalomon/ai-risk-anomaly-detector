import pandas as pd

DATA_PATH = "data/sample_transactions.csv"


def load_data(path: str) -> pd.DataFrame:
    """Load transaction data from CSV."""
    return pd.read_csv(path)


def flag_risks(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add simple risk flags:
    - missing amount
    - missing vendor
    - duplicate transactions (same date, amount, vendor, department)
    - high amount (>= 5000)
    - weekend orders
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    
    # Normalize missing values
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    df["flag_missing_amount"] = df["amount"].isna()
    df["flag_missing_vendor"] = df["vendor"].isna() | (df["vendor"].astype(str).str.strip() == "")
    df["flag_weekend"] = df["date"].dt.weekday > 4
    key_cols = ["date", "amount", "vendor", "department"]
    df["flag_duplicate"] = df.duplicated(subset=key_cols, keep=False)

    df["flag_high_amount"] = df["amount"].fillna(0) >= 5000

    # Overall flag if any rule triggers
    df["flag_any_risk"] = (
        df["flag_missing_amount"]
        | df["flag_missing_vendor"]
        | df["flag_duplicate"]
        | df["flag_high_amount"]
        | df["flag_weekend"]    )

    return df


def print_summary(df: pd.DataFrame) -> None:
    total = len(df)
    flagged = int(df["flag_any_risk"].sum())

    print("=== AI Risk Anomaly Detector (v0.1) ===")
    print(f"Total transactions: {total}")
    print(f"Flagged transactions: {flagged}")
    print()

    print("Flag counts:")
    print(f"- Missing amount: {int(df['flag_missing_amount'].sum())}")
    print(f"- Missing vendor: {int(df['flag_missing_vendor'].sum())}")
    print(f"- Duplicate transactions: {int(df['flag_duplicate'].sum())}")
    print(f"- High amount (>= 5000): {int(df['flag_high_amount'].sum())}")
    print()

    if flagged > 0:
        print("Preview of flagged transactions:")
        cols = ["date", "amount", "vendor", "department", "notes",
                "flag_missing_amount", "flag_missing_vendor", "flag_duplicate", "flag_high_amount"]
        preview = df.loc[df["flag_any_risk"], cols].head(10)
        print(preview.to_string(index=False))


def main() -> None:
    df = load_data(DATA_PATH)
    df_flagged = flag_risks(df)
    print_summary(df_flagged)


if __name__ == "__main__":
    main()# Entry point for AI risk anomaly detector
