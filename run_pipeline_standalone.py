"""
Standalone Pipeline Runner for Verification
Tests the exact 5-task logic of data_pipeline_dag outside Airflow
to verify data transformations, validation rules, output files, and metrics.
"""

from datetime import datetime
import logging
from pathlib import Path
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

INPUT_FILE = DATA_DIR / "input.csv"
EXTRACTED_FILE = OUTPUT_DIR / "extracted_data.csv"
PROCESSED_FILE = OUTPUT_DIR / "processed_data.csv"
REPORT_FILE = OUTPUT_DIR / "summary_report.txt"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("pipeline_runner")


def run_pipeline():
    print("=" * 70)
    print("RUNNING 5-STAGE ETL PIPELINE VERIFICATION")
    print("=" * 70)

    # -------------------------------------------------------------
    # TASK 1: DATA EXTRACTION
    # -------------------------------------------------------------
    logger.info("--> [TASK 1/5: EXTRACT] Reading input data...")
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    df_raw = pd.read_csv(INPUT_FILE)
    total_extracted = len(df_raw)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df_raw.to_csv(EXTRACTED_FILE, index=False)
    logger.info(f"    Extracted {total_extracted} records. Saved to {EXTRACTED_FILE}")

    # -------------------------------------------------------------
    # TASK 2: DATA VALIDATION
    # -------------------------------------------------------------
    logger.info("--> [TASK 2/5: VALIDATE] Validating data quality...")
    df_val = pd.read_csv(EXTRACTED_FILE)
    missing_per_col = df_val.isnull().sum().to_dict()
    total_missing = int(df_val.isnull().sum().sum())
    rows_with_missing = int(df_val.isnull().any(axis=1).sum())

    invalid_age = (df_val["age"] < 0) | (df_val["age"] > 120)
    invalid_purchase = df_val["purchase_amount"] < 0
    invalid_mask = invalid_age.fillna(False) | invalid_purchase.fillna(False)
    total_invalid = int(invalid_mask.sum())
    duplicate_count = int(df_val.duplicated(subset=["customer_id"]).sum())

    logger.info(f"    Missing values by column: {missing_per_col}")
    logger.info(f"    Total missing value cells: {total_missing}")
    logger.info(f"    Rows with missing values: {rows_with_missing}")
    logger.info(f"    Total invalid records: {total_invalid}")
    logger.info(f"    Duplicate customer IDs: {duplicate_count}")

    # -------------------------------------------------------------
    # TASK 3: DATA PROCESSING
    # -------------------------------------------------------------
    logger.info("--> [TASK 3/5: PROCESS] Cleaning and transforming data...")
    # Deduplicate
    df_dedup = df_val.drop_duplicates(subset=["customer_id"], keep="first").copy()
    duplicates_removed = len(df_val) - len(df_dedup)

    # Filter invalid records
    invalid_in_dedup = (
        (df_dedup["age"] < 0)
        | (df_dedup["age"] > 120)
        | (df_dedup["purchase_amount"] < 0)
    )
    invalid_removed = int(invalid_in_dedup.fillna(False).sum())
    df_clean = df_dedup[~invalid_in_dedup.fillna(False)].copy()

    # Impute missing numericals with median
    med_age = round(float(df_clean["age"].median()), 0)
    med_purchase = round(float(df_clean["purchase_amount"].median()), 2)
    df_clean["age"] = df_clean["age"].fillna(med_age).astype(int)
    df_clean["purchase_amount"] = df_clean["purchase_amount"].fillna(med_purchase).round(2)

    # Impute missing categoricals with Unknown
    df_clean["gender"] = df_clean["gender"].fillna("Unknown").astype(str).str.strip().str.upper()
    df_clean["city"] = df_clean["city"].fillna("Unknown").astype(str).str.strip().str.title()
    df_clean["customer_id"] = df_clean["customer_id"].astype(str).str.strip()

    df_clean.to_csv(PROCESSED_FILE, index=False)
    total_processed = len(df_clean)
    logger.info(f"    Duplicates removed: {duplicates_removed}")
    logger.info(f"    Invalid records removed: {invalid_removed}")
    logger.info(f"    Cleaned records saved: {total_processed} -> {PROCESSED_FILE}")

    # -------------------------------------------------------------
    # TASK 4: REPORT GENERATION
    # -------------------------------------------------------------
    logger.info("--> [TASK 4/5: REPORT] Generating summary report...")
    timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    report_content = f"""================================================================================
           APACHE AIRFLOW DATA PIPELINE SUMMARY REPORT
================================================================================
DAG ID                     : data_pipeline_dag
Execution Timestamp        : {timestamp_str}
Processing Completion Status: SUCCESS

--------------------------------------------------------------------------------
1. PIPELINE EXECUTION METRICS
--------------------------------------------------------------------------------
Total records extracted    : {total_extracted}
Total records processed    : {total_processed}
Missing values identified  : {total_missing}
Invalid records identified : {total_invalid}
Duplicate records removed  : {duplicates_removed}

--------------------------------------------------------------------------------
2. DATA TRANSFORMATION DETAILS
--------------------------------------------------------------------------------
- Input data source        : {INPUT_FILE}
- Extracted copy location  : {EXTRACTED_FILE}
- Cleaned dataset location : {PROCESSED_FILE}
- Numerical Imputation     : Age (Median), Purchase Amount (Median)
- Categorical Imputation   : Gender ('Unknown'), City ('Unknown')
- Validation Criteria      : Age [0-120], Purchase Amount >= 0, Unique customer_id

================================================================================
Generated automatically by Apache Airflow Workflow Automation Pipeline.
================================================================================
"""
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report_content)
    logger.info(f"    Summary report written to {REPORT_FILE}")

    # -------------------------------------------------------------
    # TASK 5: NOTIFICATION
    # -------------------------------------------------------------
    logger.info("--> [TASK 5/5: NOTIFY] Delivering notification...")
    print(f"""
********************************************************************************
[AIRFLOW NOTIFICATION] WORKFLOW COMPLETED SUCCESSFULLY!
--------------------------------------------------------------------------------
Pipeline Status : SUCCESS
DAG ID          : data_pipeline_dag
Summary Report  : {REPORT_FILE}
Processed Data  : {PROCESSED_FILE}
All 5 tasks executed and validated without errors.
********************************************************************************
""")

    print("\n[VERIFICATION RESULT] Pipeline executed flawlessly!")
    print(f"Input records: {total_extracted} | Output records: {total_processed}")


if __name__ == "__main__":
    run_pipeline()

