"""
Workflow Automation Pipeline using Apache Airflow
Assignment: Build Workflow Automation Using Apache Airflow
DAG ID: data_pipeline_dag
"""

from datetime import datetime, timedelta
import logging
from pathlib import Path
import pandas as pd
import numpy as np

from airflow import DAG
from airflow.operators.python import PythonOperator

# -------------------------------------------------------------------------
# Path Configurations
# -------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

INPUT_FILE = DATA_DIR / "input.csv"
EXTRACTED_FILE = OUTPUT_DIR / "extracted_data.csv"
PROCESSED_FILE = OUTPUT_DIR / "processed_data.csv"
REPORT_FILE = OUTPUT_DIR / "summary_report.txt"

# Configure standard logger
logger = logging.getLogger("airflow.task")


# -------------------------------------------------------------------------
# TASK 1: DATA EXTRACTION
# -------------------------------------------------------------------------
def extract_data(**context):
    """
    Reads data/input.csv using Pandas, validates file existence,
    displays record count, and saves extracted dataset to output directory.
    """
    logger.info("=" * 60)
    logger.info("TASK 1: DATA EXTRACTION STARTED")
    logger.info("=" * 60)

    # 1. Validate that input file exists
    if not INPUT_FILE.exists():
        err_msg = f"Input file not found at expected location: {INPUT_FILE}"
        logger.error(err_msg)
        raise FileNotFoundError(err_msg)

    # 2. Read dataset using Pandas
    df = pd.read_csv(INPUT_FILE)
    record_count = len(df)
    logger.info(f"Successfully loaded input file: {INPUT_FILE}")
    logger.info(f"Total records extracted: {record_count}")
    logger.info(f"Columns present: {list(df.columns)}")

    # 3. Ensure output directory exists and save extracted copy
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(EXTRACTED_FILE, index=False)
    logger.info(f"Extracted dataset saved to: {EXTRACTED_FILE}")

    # Pass extraction metadata forward via XCom
    extraction_stats = {
        "extracted_file": str(EXTRACTED_FILE),
        "total_extracted": int(record_count),
    }
    logger.info("TASK 1: DATA EXTRACTION COMPLETED SUCCESSFULLY")
    return extraction_stats


# -------------------------------------------------------------------------
# TASK 2: DATA VALIDATION
# -------------------------------------------------------------------------
def validate_data(**context):
    """
    Checks missing values, identifies invalid records, generates validation
    statistics, logs results, and passes summary forward.
    """
    logger.info("=" * 60)
    logger.info("TASK 2: DATA VALIDATION STARTED")
    logger.info("=" * 60)

    # Retrieve extraction metadata from Task 1 via XCom
    ti = context["ti"]
    extract_meta = ti.xcom_pull(task_ids="extract")
    extracted_path = Path(extract_meta["extracted_file"]) if extract_meta else EXTRACTED_FILE

    df = pd.read_csv(extracted_path)
    logger.info(f"Loaded {len(df)} records for validation from {extracted_path}")

    # 1. Missing Values Check
    missing_per_col = df.isnull().sum().to_dict()
    total_missing_values = int(df.isnull().sum().sum())
    rows_with_missing = int(df.isnull().any(axis=1).sum())

    logger.info(f"Missing values count per column: {missing_per_col}")
    logger.info(f"Total missing value cells: {total_missing_values}")
    logger.info(f"Total rows containing missing values: {rows_with_missing}")

    # 2. Invalid Records Identification
    # Age validation: age must not be null and must be between 0 and 120
    invalid_age_mask = (df["age"] < 0) | (df["age"] > 120)
    invalid_age_count = int(invalid_age_mask.fillna(False).sum())

    # Purchase amount validation: purchase_amount must not be negative
    invalid_purchase_mask = df["purchase_amount"] < 0
    invalid_purchase_count = int(invalid_purchase_mask.fillna(False).sum())

    # Gender validation: valid values are M, F, Other or NaN
    valid_genders = ["M", "F", "Other", "m", "f"]
    invalid_gender_mask = ~df["gender"].isin(valid_genders) & df["gender"].notnull()
    invalid_gender_count = int(invalid_gender_mask.sum())

    # Combined invalid rows mask
    combined_invalid_mask = invalid_age_mask.fillna(False) | invalid_purchase_mask.fillna(False) | invalid_gender_mask
    total_invalid_records = int(combined_invalid_mask.sum())
    invalid_indices = df[combined_invalid_mask].index.tolist()

    logger.info(f"Invalid age records count: {invalid_age_count}")
    logger.info(f"Invalid purchase_amount records count: {invalid_purchase_count}")
    logger.info(f"Invalid gender records count: {invalid_gender_count}")
    logger.info(f"Total invalid records identified: {total_invalid_records} (Row indices: {invalid_indices})")

    # 3. Duplicate Records Check
    duplicate_count = int(df.duplicated(subset=["customer_id"]).sum())
    logger.info(f"Duplicate customer_id records detected: {duplicate_count}")

    # Pass validation statistics forward via XCom
    validation_stats = {
        "total_missing_values": total_missing_values,
        "rows_with_missing": rows_with_missing,
        "missing_per_col": missing_per_col,
        "total_invalid_records": total_invalid_records,
        "invalid_indices": invalid_indices,
        "duplicate_count": duplicate_count,
    }
    logger.info("TASK 2: DATA VALIDATION COMPLETED SUCCESSFULLY")
    return validation_stats


# -------------------------------------------------------------------------
# TASK 3: DATA PROCESSING
# -------------------------------------------------------------------------
def process_data(**context):
    """
    Handles missing numerical values (imputation), handles missing categorical
    values (imputation), removes duplicates and invalid rows, applies cleaning,
    and saves output/processed_data.csv.
    """
    logger.info("=" * 60)
    logger.info("TASK 3: DATA PROCESSING STARTED")
    logger.info("=" * 60)

    ti = context["ti"]
    extract_meta = ti.xcom_pull(task_ids="extract")
    extracted_path = Path(extract_meta["extracted_file"]) if extract_meta else EXTRACTED_FILE

    df = pd.read_csv(extracted_path)
    initial_len = len(df)
    logger.info(f"Starting processing with {initial_len} raw records")

    # 1. Remove duplicate records
    dup_mask = df.duplicated(subset=["customer_id"], keep="first")
    duplicates_removed = int(dup_mask.sum())
    df_no_dups = df[~dup_mask].copy()
    logger.info(f"Removed {duplicates_removed} duplicate customer_id record(s)")

    # 2. Filter out invalid records (e.g. negative age, age > 120, negative purchase)
    invalid_mask = (
        (df_no_dups["age"] < 0)
        | (df_no_dups["age"] > 120)
        | (df_no_dups["purchase_amount"] < 0)
    )
    invalid_records_removed = int(invalid_mask.fillna(False).sum())
    df_valid = df_no_dups[~invalid_mask.fillna(False)].copy()
    logger.info(f"Filtered out {invalid_records_removed} invalid record(s)")

    # 3. Handle missing numerical values: Impute with median
    median_age = round(float(df_valid["age"].median()), 0)
    median_purchase = round(float(df_valid["purchase_amount"].median()), 2)

    df_valid["age"] = df_valid["age"].fillna(median_age).astype(int)
    df_valid["purchase_amount"] = df_valid["purchase_amount"].fillna(median_purchase).round(2)
    logger.info(f"Imputed missing age with median ({median_age})")
    logger.info(f"Imputed missing purchase_amount with median ({median_purchase})")

    # 4. Handle missing categorical values: Impute with 'Unknown'
    df_valid["gender"] = df_valid["gender"].fillna("Unknown").astype(str).str.strip().str.upper()
    df_valid["city"] = df_valid["city"].fillna("Unknown").astype(str).str.strip().str.title()
    logger.info("Imputed missing gender with 'Unknown' and standardized casing")
    logger.info("Imputed missing city with 'Unknown' and standardized title casing")

    # 5. Clean customer_id
    df_valid["customer_id"] = df_valid["customer_id"].astype(str).str.strip()

    # 6. Save processed dataset
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df_valid.to_csv(PROCESSED_FILE, index=False)
    processed_count = len(df_valid)
    logger.info(f"Cleaned dataset saved to: {PROCESSED_FILE}")
    logger.info(f"Final processed records count: {processed_count}")

    processing_stats = {
        "processed_file": str(PROCESSED_FILE),
        "total_processed": int(processed_count),
        "duplicates_removed": int(duplicates_removed),
        "invalid_removed": int(invalid_records_removed),
    }
    logger.info("TASK 3: DATA PROCESSING COMPLETED SUCCESSFULLY")
    return processing_stats


# -------------------------------------------------------------------------
# TASK 4: REPORT GENERATION
# -------------------------------------------------------------------------
def generate_report(**context):
    """
    Generates output/summary_report.txt with comprehensive ETL execution metrics.
    """
    logger.info("=" * 60)
    logger.info("TASK 4: REPORT GENERATION STARTED")
    logger.info("=" * 60)

    ti = context["ti"]
    extract_stats = ti.xcom_pull(task_ids="extract") or {"total_extracted": 0}
    validation_stats = ti.xcom_pull(task_ids="validate") or {
        "total_missing_values": 0,
        "total_invalid_records": 0,
        "duplicate_count": 0,
    }
    processing_stats = ti.xcom_pull(task_ids="process") or {
        "total_processed": 0,
        "duplicates_removed": 0,
        "invalid_removed": 0,
    }

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
Total records extracted    : {extract_stats.get('total_extracted', 'N/A')}
Total records processed    : {processing_stats.get('total_processed', 'N/A')}
Missing values identified  : {validation_stats.get('total_missing_values', 'N/A')}
Invalid records identified : {validation_stats.get('total_invalid_records', 'N/A')}
Duplicate records removed  : {processing_stats.get('duplicates_removed', 'N/A')}

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

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report_content)

    logger.info(f"Summary report generated at: {REPORT_FILE}")
    logger.info("\n" + report_content)
    logger.info("TASK 4: REPORT GENERATION COMPLETED SUCCESSFULLY")

    return {"report_file": str(REPORT_FILE), "status": "SUCCESS"}


# -------------------------------------------------------------------------
# TASK 5: NOTIFICATION
# -------------------------------------------------------------------------
def send_notification(**context):
    """
    Prints a success notification and report location.
    Executes only after successful report generation.
    """
    logger.info("=" * 60)
    logger.info("TASK 5: NOTIFICATION STARTED")
    logger.info("=" * 60)

    ti = context["ti"]
    report_meta = ti.xcom_pull(task_ids="report")
    report_path = report_meta.get("report_file", str(REPORT_FILE)) if report_meta else str(REPORT_FILE)
    status = report_meta.get("status", "SUCCESS") if report_meta else "SUCCESS"

    notification_message = f"""
********************************************************************************
[AIRFLOW NOTIFICATION] WORKFLOW COMPLETED SUCCESSFULLY!
--------------------------------------------------------------------------------
Pipeline Status : {status}
DAG ID          : data_pipeline_dag
Summary Report  : {report_path}
Processed Data  : {PROCESSED_FILE}
All 5 tasks executed and validated without errors.
********************************************************************************
"""
    print(notification_message)
    logger.info(notification_message)
    logger.info("TASK 5: NOTIFICATION COMPLETED SUCCESSFULLY")
    return "Notification delivered successfully"


# -------------------------------------------------------------------------
# DAG Definition and Default Arguments
# -------------------------------------------------------------------------
default_args = {
    "owner": "mlops_student",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="data_pipeline_dag",
    default_args=default_args,
    description="MLOps Assignment 4: Automated Data Pipeline with Apache Airflow",
    schedule_interval="@daily",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=["mlops", "assignment4", "data_pipeline", "automation"],
) as dag:

    extract_task = PythonOperator(
        task_id="extract",
        python_callable=extract_data,
        provide_context=True,
    )

    validate_task = PythonOperator(
        task_id="validate",
        python_callable=validate_data,
        provide_context=True,
    )

    process_task = PythonOperator(
        task_id="process",
        python_callable=process_data,
        provide_context=True,
    )

    report_task = PythonOperator(
        task_id="report",
        python_callable=generate_report,
        provide_context=True,
    )

    notify_task = PythonOperator(
        task_id="notify",
        python_callable=send_notification,
        provide_context=True,
    )

    # -------------------------------------------------------------------------
    # Exact Task Dependencies
    # -------------------------------------------------------------------------
    extract_task >> validate_task >> process_task >> report_task >> notify_task

