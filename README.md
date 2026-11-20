# Build Workflow Automation Using Apache Airflow
**College MLOps Assignment 4**

---

## 1. Assignment Objective

The objective of this assignment is to design, implement, and automate an end-to-end Machine Learning Operations (MLOps) data pipeline using **Apache Airflow**.

The pipeline orchestrates five sequential tasks:
1. **Data Extraction**: Ingest raw customer records from `data/input.csv`, validate file presence, and stage an extraction copy.
2. **Data Validation**: Audit the raw dataset for missing values, invalid records (negative age, impossible age ranges, negative purchase amounts), and duplicate IDs.
3. **Data Processing**: Clean and impute missing numerical values (using median), impute missing categorical fields (`Unknown`), remove invalid and duplicate records, and produce a cleaned dataset at `output/processed_data.csv`.
4. **Report Generation**: Compile a comprehensive performance report with pipeline execution statistics, saving it to `output/summary_report.txt`.
5. **Notification**: Emit a success notification confirming successful pipeline execution and referencing artifact locations.

---

## 2. Theoretical Foundations

### What is Workflow Orchestration?
In modern data engineering and MLOps, machine learning systems rarely consist of a single standalone script. Instead, they require multi-stage workflows—spanning ingestion, validation, preprocessing, feature engineering, model training, evaluation, and deployment.

**Workflow Orchestration** is the practice of coordinating, scheduling, and monitoring complex, multi-step computational pipelines to ensure tasks execute in the correct order, with error recovery, retries, and auditability.

### What is Apache Airflow?
**Apache Airflow** is an open-source platform created by Airbnb to programmatically author, schedule, and monitor workflows. Workflows in Airflow are written purely in Python, offering unlimited flexibility, modularity, dynamic configuration, and extensive integration with databases, cloud providers, and computing clusters.

Key components of Airflow:
- **Scheduler**: Monitors all tasks and DAGs, triggering task instances whose dependencies are satisfied.
- **Webserver / UI**: Provides a modern browser-based dashboard to inspect DAGs, task states, execution logs, run histories, and manual controls.
- **Metadata Database**: Stores pipeline states, variables, connections, user credentials, and execution history (typically SQLite for local testing or PostgreSQL/MySQL for production).
- **Executor**: Defines how and where worker tasks run (e.g., `SequentialExecutor`, `LocalExecutor`, `CeleryExecutor`, `KubernetesExecutor`).

### What is a DAG?
A **DAG** (**Directed Acyclic Graph**) is a mathematical representation of a workflow where:
- **Directed**: Each edge between tasks points in a specific direction, enforcing execution order ($A \rightarrow B$).
- **Acyclic**: The graph contains no closed loops. Task $A$ cannot depend on Task $B$ if Task $B$ depends on Task $A$, preventing infinite execution cycles.
- **Graph**: A collection of nodes (tasks) and edges (dependencies).

---

## 3. Project Structure

```
Assignment4/
│
├── dags/
│   └── data_pipeline_dag.py        # Airflow DAG definition with 5 sequential PythonOperator tasks
│
├── data/
│   └── input.csv                   # Raw customer dataset with deliberate missing and invalid values
│
├── output/
│   ├── extracted_data.csv          # Staged copy saved during Task 1 (Extraction)
│   ├── processed_data.csv          # Cleaned, imputed, deduplicated dataset from Task 3
│   └── summary_report.txt          # Detailed audit and execution metrics from Task 4
│
├── logs/                           # Airflow runtime logs for tasks and scheduler
├── screenshots/                    # Screenshots for college submission
│   └── SCREENSHOT_GUIDE.md         # Exact instructions on the 6 screenshots to capture
│
├── requirements.txt                # Python package dependencies with Airflow constraints
├── docker-compose.yaml             # Optional turnkey Docker setup
├── run_pipeline_standalone.py      # Standalone verification runner
├── README.md                       # Comprehensive project documentation
└── .gitignore                      # Git exclusion rules for clean version control
```

---

## 4. Why Airflow Requires WSL2 or Docker on Windows

> [!IMPORTANT]
> **Operating System Note**: Apache Airflow **does not natively support Windows**. Its scheduler, process forkers, signal handling, and execution engines rely on POSIX-compliant system calls (`fcntl`, `termios`, process forking).
>
> To run Airflow on Windows, you must use either:
> 1. **WSL2 (Windows Subsystem for Linux - Ubuntu)** *(Recommended for this assignment)*, OR
> 2. **Docker Desktop** (with Linux container backend).

---

## 5. Step-by-Step Installation & Setup (WSL2 + Ubuntu)

Follow these exact steps to run Airflow inside WSL2 Ubuntu:

### Step 5.1: Install WSL2 (One-Time Setup)
1. Open PowerShell **as Administrator** on your Windows machine.
2. Run:
   ```powershell
   wsl --install -d Ubuntu
   ```
3. Restart your computer if prompted by Windows.
4. After restarting, open the **Ubuntu** terminal from your Start Menu.
5. Set your Linux username and password when prompted.

### Step 5.2: Navigate to Project Directory inside WSL
Open your Ubuntu terminal. Your Windows `C:\` drive is automatically mounted at `/mnt/c/`:
```bash
cd "/mnt/c/College/SEM 5/MLOPs/Assignment_4"
pwd
ls -la
```

### Step 5.3: Set Up a Dedicated Python Virtual Environment
Update Ubuntu packages and create an isolated virtual environment:
```bash
sudo apt update && sudo apt install -y python3-venv python3-pip

# Create dedicated virtual environment
python3 -m venv airflow_env

# Activate virtual environment
source airflow_env/bin/activate
```

### Step 5.4: Install Apache Airflow Using Official Constraints
To guarantee dependency compatibility without version conflicts, install Airflow 2.10.4 with its official constraint file:
```bash
AIRFLOW_VERSION=2.10.4
PYTHON_VERSION="$(python3 --version | cut -d ' ' -f 2 | cut -d '.' -f 1-2)"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

pip install --upgrade pip
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
pip install pandas numpy
```

Verify installation:
```bash
airflow version
```
*(Should output `2.10.4`)*

### Step 5.5: Configure Airflow Home
Set the `AIRFLOW_HOME` environment variable so Airflow uses our project directory:
```bash
export AIRFLOW_HOME="$(pwd)"
echo "AIRFLOW_HOME set to: $AIRFLOW_HOME"
```

To make this persistent whenever you activate your virtual environment:
```bash
echo 'export AIRFLOW_HOME="/mnt/c/College/SEM 5/MLOPs/Assignment_4"' >> airflow_env/bin/activate
```

### Step 5.6: Initialize the Airflow Database
Run database migration to initialize the SQLite metadata database:
```bash
airflow db migrate
```
*(For Airflow versions prior to 2.7, `airflow db init` is equivalent).*

### Step 5.7: Create an Administrator User
Create the administrator account for the Airflow Web UI:
```bash
airflow users create \
    --username admin \
    --firstname Student \
    --lastname MLOps \
    --role Admin \
    --email student@mlops.edu \
    --password admin
```

---

## 6. Starting Airflow Services

Airflow requires two services to run simultaneously: the **Webserver** and the **Scheduler**.

### Option A: Separate Terminals (Standard Production/Testing Mode)

**Terminal 1 — Start Webserver:**
```bash
cd "/mnt/c/College/SEM 5/MLOPs/Assignment_4"
source airflow_env/bin/activate
export AIRFLOW_HOME="$(pwd)"
airflow webserver --port 8080
```

**Terminal 2 — Start Scheduler:**
```bash
cd "/mnt/c/College/SEM 5/MLOPs/Assignment_4"
source airflow_env/bin/activate
export AIRFLOW_HOME="$(pwd)"
airflow scheduler
```

### Option B: Airflow Standalone Mode (Single Command Convenience)
Airflow provides a convenient command that boots the webserver, scheduler, and worker simultaneously in a single terminal:
```bash
cd "/mnt/c/College/SEM 5/MLOPs/Assignment_4"
source airflow_env/bin/activate
export AIRFLOW_HOME="$(pwd)"
airflow standalone
```

---

## 7. Accessing the Web UI & Triggering the Workflow

1. Open your browser and navigate to:
   ```
   http://localhost:8080
   ```
2. Log in using the admin credentials:
   - **Username**: `admin`
   - **Password**: `admin`
3. In the DAGs list, find **`data_pipeline_dag`**.
4. Unpause the DAG by clicking the toggle switch on the left from **OFF** to **ON** (turns blue).
5. Trigger the DAG manually by clicking the **Play button ▶ (Trigger DAG)** on the right.
6. Click into `data_pipeline_dag` to view the **Graph View** or **Grid View**.
7. Watch each of the 5 tasks transition from queued (grey) $\rightarrow$ running (lime green) $\rightarrow$ success (dark green).

---

## 8. CLI Alternative Execution & Verification

You can also test and verify the DAG entirely via the Airflow command line:

```bash
# 1. Verify DAG detection
airflow dags list | grep data_pipeline_dag

# 2. List all 5 tasks
airflow tasks list data_pipeline_dag

# 3. Test individual tasks without starting scheduler
airflow tasks test data_pipeline_dag extract 2025-01-01
airflow tasks test data_pipeline_dag validate 2025-01-01
airflow tasks test data_pipeline_dag process 2025-01-01
airflow tasks test data_pipeline_dag report 2025-01-01
airflow tasks test data_pipeline_dag notify 2025-01-01

# 4. Trigger the complete DAG run via CLI
airflow dags trigger data_pipeline_dag
```

---

## 9. DAG Architecture & Task Breakdown

The DAG is defined in `dags/data_pipeline_dag.py` with:
- **DAG ID**: `data_pipeline_dag`
- **Schedule**: `@daily` (Midnight UTC every day)
- **catchup**: `False` (Prevents backfilling runs from start date to present)
- **Retries**: 1 retry with a 1-minute retry delay

### Task Dependency Pipeline
```
[extract] ────► [validate] ────► [process] ────► [report] ────► [notify]
```

### Detailed Task Roles

| Stage | Task ID | Operator | Responsibilities | Output Artifact |
|---|---|---|---|---|
| 1 | `extract` | `PythonOperator` | Checks `data/input.csv` exists; counts raw records; creates staged copy. | `output/extracted_data.csv` |
| 2 | `validate` | `PythonOperator` | Computes missing value counts per column; detects invalid ages ($<0$ or $>120$) and negative purchase amounts; logs audit metrics. | XCom Validation Stats |
| 3 | `process` | `PythonOperator` | Deduplicates customer IDs; removes invalid rows; imputes numerical fields with median; imputes missing categoricals with `Unknown`; standardizes casing. | `output/processed_data.csv` |
| 4 | `report` | `PythonOperator` | Aggregates metrics from previous stages; writes a formatted summary audit report. | `output/summary_report.txt` |
| 5 | `notify` | `PythonOperator` | Prints notification banner confirming execution completion and artifact paths; executes only after `report`. | Console / Airflow Log Banner |

---

## 10. Expected Pipeline Output & Audit Metrics

### Raw Input Summary (`data/input.csv`)
- **Total records extracted**: 16
- **Missing values**:
  - `age`: 1 missing (Row `CUST006`)
  - `gender`: 1 missing (Row `CUST008`)
  - `purchase_amount`: 1 missing (Row `CUST007`)
  - `city`: 1 missing (Row `CUST009`)
- **Invalid records**:
  - `CUST010`: Negative age (`-8`)
  - `CUST011`: Unrealistic age (`145`)
  - `CUST012`: Negative purchase amount (`-65.00`)
- **Duplicate records**:
  - `CUST003`: Duplicate row

### Cleaned Output Summary (`output/summary_report.txt`)
```
================================================================================
           APACHE AIRFLOW DATA PIPELINE SUMMARY REPORT
================================================================================
DAG ID                     : data_pipeline_dag
Execution Timestamp        : 2026-11-10 02:59:09 UTC
Processing Completion Status: SUCCESS

--------------------------------------------------------------------------------
1. PIPELINE EXECUTION METRICS
--------------------------------------------------------------------------------
Total records extracted    : 16
Total records processed    : 12
Missing values identified  : 4
Invalid records identified : 3
Duplicate records removed  : 1

--------------------------------------------------------------------------------
2. DATA TRANSFORMATION DETAILS
--------------------------------------------------------------------------------
- Input data source        : .../data/input.csv
- Extracted copy location  : .../output/extracted_data.csv
- Cleaned dataset location : .../output/processed_data.csv
- Numerical Imputation     : Age (Median), Purchase Amount (Median)
- Categorical Imputation   : Gender ('Unknown'), City ('Unknown')
- Validation Criteria      : Age [0-120], Purchase Amount >= 0, Unique customer_id

================================================================================
Generated automatically by Apache Airflow Workflow Automation Pipeline.
================================================================================
```

---

## 11. Screenshots Required for College Submission

Take the following 6 screenshots (refer to `screenshots/SCREENSHOT_GUIDE.md` for full details):

1. **`screenshots/01_airflow_dashboard.png`**: Web UI DAGs list showing `data_pipeline_dag` toggled ON with schedule `@daily`.
2. **`screenshots/02_dag_graph_view.png`**: Graph View showing `extract >> validate >> process >> report >> notify`.
3. **`screenshots/03_successful_dag_run.png`**: Graph/Grid view showing all 5 tasks highlighted in solid green (`success`).
4. **`screenshots/04_task_instance_details.png`**: Task Instance details page for the `validate` or `process` task.
5. **`screenshots/05_task_logs.png`**: Airflow log view showing the detailed validation and transformation logs.
6. **`screenshots/06_summary_report_and_output.png`**: Terminal or VS Code showing the generated `summary_report.txt` and `processed_data.csv`.

---

## 12. Troubleshooting Common Issues

### Issue 1: `ModuleNotFoundError: No module named 'fcntl'`
- **Cause**: Trying to run Airflow natively in PowerShell/Command Prompt on Windows.
- **Solution**: Run Airflow inside WSL2 Ubuntu or Docker containers.

### Issue 2: DAG is not visible in Web UI
- **Cause**: Airflow is scanning the default `~/airflow/dags` instead of our project directory.
- **Solution**: Ensure `export AIRFLOW_HOME="$(pwd)"` was executed in both terminals before starting the webserver and scheduler.

### Issue 3: Port 8080 already in use
- **Cause**: Another service or process is bound to port 8080.
- **Solution**: Run the webserver on an alternative port:
  ```bash
  airflow webserver --port 8081
  ```
  Then access `http://localhost:8081`.

---

## 13. Conclusion

This project demonstrates a production-grade MLOps data workflow automated using Apache Airflow:
- Applied robust workflow orchestration principles with directed acyclic graphs.
- Enforced strict data validation, anomaly filtering, median imputation, and categorical standardization.
- Configured programmatic task dependencies, automated retry policies, and structured reporting.
- Designed an auditable, reproducible, and verifiable pipeline ready for enterprise deployment.

