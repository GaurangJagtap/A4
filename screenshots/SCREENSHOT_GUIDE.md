# Required Screenshots Checklist for College Submission

This guide specifies the exact screenshots required for your MLOps Assignment 4 college submission. Keep filenames consistent so evaluators can inspect them easily.

---

### Screenshot 1: Airflow Dashboard / DAGs List View
- **File Name**: `screenshots/01_airflow_dashboard.png`
- **URL to open**: `http://localhost:8080/home`
- **What to capture**:
  - The main Airflow Web UI showing the list of DAGs.
  - Highlight the row `data_pipeline_dag`.
  - Show the DAG toggle active (ON / blue switch), schedule `@daily`, owner `mlops_student`, and the recent run circle indicators (green circle for successful runs).

---

### Screenshot 2: DAG Graph View (5 Tasks & Dependencies)
- **File Name**: `screenshots/02_dag_graph_view.png`
- **URL to open**: `http://localhost:8080/dags/data_pipeline_dag/graph`
- **What to capture**:
  - The Graph View showing all five tasks connected in sequential order:
    `extract` ➔ `validate` ➔ `process` ➔ `report` ➔ `notify`
  - Shows clear task node labels and directional dependency arrows.

---

### Screenshot 3: Successful DAG Run Execution
- **File Name**: `screenshots/03_successful_dag_run.png`
- **URL to open**: `http://localhost:8080/dags/data_pipeline_dag/grid` or Graph View after trigger
- **What to capture**:
  - All 5 task boxes surrounded by solid **dark green borders/fills** indicating `success` state.
  - The run status showing `success` with run duration and execution date.

---

### Screenshot 4: Task Instance Details Page
- **File Name**: `screenshots/04_task_instance_details.png`
- **URL to open**: Click on any task box (e.g., `validate` or `process`) in Graph/Grid view ➔ Click **"Task Instance Details"**
- **What to capture**:
  - Task ID: `validate` or `process`
  - State: `success`
  - Start date, end date, duration, operator: `PythonOperator`
  - Try number: `1`

---

### Screenshot 5: Task Execution Logs
- **File Name**: `screenshots/05_task_logs.png`
- **URL to open**: Click on the `validate` or `report` task box ➔ Click **"Log"**
- **What to capture**:
  - The log stream showing:
    - `TASK 2: DATA VALIDATION STARTED`
    - Missing values count per column
    - Invalid records identified (e.g. invalid age, negative purchase amount)
    - `TASK 2: DATA VALIDATION COMPLETED SUCCESSFULLY`

---

### Screenshot 6: Generated Summary Report & Output Verification
- **File Name**: `screenshots/06_summary_report_and_output.png`
- **What to capture**:
  - Terminal or VS Code editor showing the content of `output/summary_report.txt` and directory listing of `output/processed_data.csv`.
  - Shows `Total records extracted: 16`, `Total records processed: 12`, `Missing values identified: 4`, `Invalid records identified: 3`, `Duplicate records removed: 1`.

---

### Quick Capture Tip (Windows):
- Use `Win + Shift + S` (Snipping Tool) to capture each window and paste/save directly into the `screenshots/` directory.

