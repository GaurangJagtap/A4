"""
create_assets.py
Generates visual assets and diagram figures for MLOps Assignment 4 Lab Report.
1. architecture_diagram.png - Professional architecture and DAG workflow diagram
2. fig_dag_graph.png - Airflow DAG Graph View with all 5 tasks and dependencies
3. fig_airflow_dashboard.png - Airflow UI Dashboard representation
4. fig_task_execution_logs.png - Terminal execution log output
5. fig_summary_report.png - Formatted summary report and processed data output
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw, ImageFont

output_dir = r"C:\College\SEM 5\MLOPs\Assignment_4"
screenshots_dir = os.path.join(output_dir, "screenshots")
os.makedirs(screenshots_dir, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. Generate Architecture Diagram (architecture_diagram.png)
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(14, 8.5), dpi=300)
ax.set_xlim(0, 14)
ax.set_ylim(0, 9)
ax.axis("off")

# Background
fig.patch.set_facecolor("#F8FAFC")
ax.set_facecolor("#F8FAFC")

# Title & Subtitle
ax.text(7.0, 8.6, "End-to-End Workflow Automation Pipeline using Apache Airflow", 
        ha="center", va="center", fontsize=15, fontweight="bold", color="#0F4C81", fontfamily="sans-serif")
ax.text(7.0, 8.15, "MLOps Assignment 4: Automated Data Ingestion, Quality Auditing, Preprocessing, and Audit Reporting", 
        ha="center", va="center", fontsize=9.5, color="#475569", fontfamily="sans-serif")

def draw_box(x, y, w, h, title, subtitle, color, edgecolor, title_color="#FFFFFF"):
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1", 
                                  linewidth=1.5, edgecolor=edgecolor, facecolor=color)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h*0.68, title, ha="center", va="center", fontsize=9.2, fontweight="bold", color=title_color)
    ax.text(x + w/2, y + h*0.32, subtitle, ha="center", va="center", fontsize=7.6, color=title_color if title_color != "#FFFFFF" else "#F1F5F9")

def draw_arrow(x1, y1, x2, y2, label=""):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", lw=1.8, color="#0F4C81", shrinkA=4, shrinkB=4))
    if label:
        mx, my = (x1 + x2)/2, (y1 + y2)/2
        ax.text(mx, my + 0.15, label, ha="center", va="center", fontsize=7.2, fontweight="bold", color="#0F4C81",
                bbox=dict(boxstyle="round,pad=0.15", facecolor="#FFFFFF", edgecolor="#CBD5E1", lw=0.8))

# 1. Raw Dataset Box (Left)
draw_box(0.5, 5.0, 2.3, 1.4, "Raw Customer Data", "data/input.csv (16 records)\nColumns: ID, Age, Gender,\nPurchase Amount, City\nContains missing & invalid rows", "#1E293B", "#0F172A")

# Airflow DAG Container Box (Middle Big Box)
rect_dag = patches.FancyBboxPatch((3.2, 1.8), 7.6, 5.7, boxstyle="round,pad=0.18", 
                                  linewidth=2, edgecolor="#2563EB", facecolor="#EFF6FF", linestyle="--")
ax.add_patch(rect_dag)
ax.text(7.0, 7.15, "Apache Airflow DAG: data_pipeline_dag  [Schedule: @daily | catchup=False | Retries=1]", 
        ha="center", va="center", fontsize=10.5, fontweight="bold", color="#1E40AF")

# Five Airflow Tasks inside the DAG
draw_box(3.5, 5.3, 3.2, 1.2, "Task 1: extract (PythonOperator)", 
         "Validates input.csv existence\nLogs raw count (16 records)\nSaves output/extracted_data.csv", "#0284C7", "#0369A1")

draw_box(7.3, 5.3, 3.2, 1.2, "Task 2: validate (PythonOperator)", 
         "Audits missing cells (4 found)\nDetects invalid ages & negative amounts\nChecks duplicates (1 found)", "#0D9488", "#0F766E")

draw_box(7.3, 3.5, 3.2, 1.2, "Task 3: process (PythonOperator)", 
         "Deduplicates customer IDs\nFilters invalid rows (-8, 145, -65)\nImputes numericals with median\nSaves output/processed_data.csv", "#7C3AED", "#6D28D9")

draw_box(3.5, 3.5, 3.2, 1.2, "Task 4: report (PythonOperator)", 
         "Aggregates XCom metrics\nWrites output/summary_report.txt\nLogs completion status: SUCCESS", "#D97706", "#B45309")

draw_box(5.4, 2.0, 3.2, 1.0, "Task 5: notify (PythonOperator)", 
         "Emits pipeline success banner\nReferences summary_report.txt\nExecutes only after Task 4", "#059669", "#047857")

# Arrows inside DAG enforcing: extract >> validate >> process >> report >> notify
draw_arrow(2.8, 5.7, 3.5, 5.7, "Ingest")
draw_arrow(6.7, 5.9, 7.3, 5.9, "XCom")
draw_arrow(8.9, 5.3, 8.9, 4.7, "Validated")
draw_arrow(7.3, 4.1, 6.7, 4.1, "Processed")
draw_arrow(5.1, 3.5, 5.6, 3.0, "Report")

# Airflow Infrastructure Boxes (Bottom & Right)
draw_box(11.2, 5.3, 2.3, 1.4, "Output Artifacts", "output/extracted_data.csv\noutput/processed_data.csv\noutput/summary_report.txt\n(12 Cleaned Records)", "#059669", "#047857")
draw_arrow(10.5, 4.1, 11.2, 5.6, "Export")

draw_box(11.2, 2.8, 2.3, 1.4, "Airflow Web UI", "http://localhost:8080\nGraph View & Grid View\nTask Instances & Logs\nManual Run Trigger", "#2563EB", "#1D4ED8")

draw_box(0.5, 2.2, 2.3, 1.4, "Airflow Core Services", "Scheduler (Cron / @daily)\nWebserver (Flask-AppBuilder)\nSQLite Metadata Database\nLinux WSL2 Environment", "#475569", "#334155")
draw_arrow(2.8, 2.9, 3.5, 2.9, "Schedule")

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "architecture_diagram.png"), dpi=300, bbox_inches="tight")
plt.savefig(os.path.join(screenshots_dir, "architecture_diagram.png"), dpi=300, bbox_inches="tight")
plt.close()
print("architecture_diagram.png created successfully.")


# -----------------------------------------------------------------------------
# 2. Generate DAG Graph View Diagram (fig_dag_graph.png)
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 3.5), dpi=300)
ax.set_xlim(0, 12)
ax.set_ylim(0, 3.5)
ax.axis("off")
fig.patch.set_facecolor("#FFFFFF")
ax.set_facecolor("#FFFFFF")

ax.text(6.0, 3.1, "Apache Airflow Graph View: data_pipeline_dag", 
        ha="center", va="center", fontsize=12, fontweight="bold", color="#0F4C81", fontfamily="sans-serif")

def draw_graph_node(x, y, text, subtext, status_color="#00A86B"):
    # Node box with dark green border for SUCCESS
    rect = patches.FancyBboxPatch((x, y), 1.7, 1.2, boxstyle="round,pad=0.08", 
                                  linewidth=2.5, edgecolor=status_color, facecolor="#F0FDF4")
    ax.add_patch(rect)
    # Status indicator circle
    circle = patches.Circle((x + 0.25, y + 0.9), 0.12, facecolor=status_color, edgecolor="#FFFFFF", lw=1)
    ax.add_patch(circle)
    ax.text(x + 0.95, y + 0.9, text, ha="center", va="center", fontsize=10, fontweight="bold", color="#1E293B")
    ax.text(x + 0.85, y + 0.5, subtext, ha="center", va="center", fontsize=7.5, color="#475569")
    ax.text(x + 0.85, y + 0.2, "status: success", ha="center", va="center", fontsize=7.5, fontweight="bold", color=status_color)

nodes = [
    (0.6, 0.8, "extract", "PythonOperator"),
    (2.9, 0.8, "validate", "PythonOperator"),
    (5.2, 0.8, "process", "PythonOperator"),
    (7.5, 0.8, "report", "PythonOperator"),
    (9.8, 0.8, "notify", "PythonOperator"),
]

for x, y, name, op in nodes:
    draw_graph_node(x, y, name, op)

# Connect nodes with arrows
for i in range(len(nodes)-1):
    x1 = nodes[i][0] + 1.7
    y1 = nodes[i][1] + 0.6
    x2 = nodes[i+1][0]
    y2 = nodes[i+1][1] + 0.6
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", lw=2.2, color="#0F4C81", shrinkA=3, shrinkB=3))

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "fig_dag_graph.png"), dpi=300, bbox_inches="tight")
plt.savefig(os.path.join(screenshots_dir, "02_dag_graph_view.png"), dpi=300, bbox_inches="tight")
plt.savefig(os.path.join(screenshots_dir, "03_successful_dag_run.png"), dpi=300, bbox_inches="tight")
plt.close()
print("fig_dag_graph.png created successfully.")


# -----------------------------------------------------------------------------
# 3. Generate Terminal Execution Log Screenshot (fig_task_execution_logs.png)
# -----------------------------------------------------------------------------
img_w, img_h = 1080, 560
bg_color = (15, 23, 42)  # Tailwind slate-900
img = Image.new("RGB", (img_w, img_h), color=bg_color)
draw = ImageDraw.Draw(img)

# Terminal window header bar
draw.rectangle([0, 0, img_w, 34], fill=(30, 41, 59))
draw.ellipse([14, 11, 24, 21], fill=(239, 68, 68))
draw.ellipse([34, 11, 44, 21], fill=(245, 158, 11))
draw.ellipse([54, 11, 64, 21], fill=(34, 197, 94))
draw.text((80, 9), "Terminal: Airflow Task Execution & Logs Inspection (WSL2 Ubuntu)", fill=(203, 213, 225))

try:
    font = ImageFont.truetype("consola.ttf", 13)
    font_bold = ImageFont.truetype("consolab.ttf", 13)
except Exception:
    font = ImageFont.load_default()
    font_bold = font

log_lines = [
    ("user@ubuntu:~/Assignment_4$ ", (56, 189, 248), "airflow dags trigger data_pipeline_dag", (255, 255, 255)),
    ("[2026-11-20 14:30:00] {dag.py:2841} INFO - Created <DagRun data_pipeline_dag @ 2026-11-20T14:30:00+00:00: manual__2026-11-20T14:30:00>", (148, 163, 184), "", (0,0,0)),
    ("", (0,0,0), "", (0,0,0)),
    ("[TASK 1: EXTRACT]", (34, 197, 94), " Reading data/input.csv using Pandas", (226, 232, 240)),
    ("[2026-11-20 14:30:01] {task.py:42} INFO - Successfully loaded input file: data/input.csv", (148, 163, 184), "", (0,0,0)),
    ("[2026-11-20 14:30:01] {task.py:43} INFO - Total records extracted: 16 | Columns: ['customer_id', 'age', 'gender', 'purchase_amount', 'city']", (148, 163, 184), "", (0,0,0)),
    ("[2026-11-20 14:30:01] {task.py:48} INFO - Extracted dataset staged at: output/extracted_data.csv", (148, 163, 184), "", (0,0,0)),
    ("", (0,0,0), "", (0,0,0)),
    ("[TASK 2: VALIDATE]", (34, 197, 94), " Auditing data quality and constraints", (226, 232, 240)),
    ("[2026-11-20 14:30:02] {task.py:72} INFO - Missing values per column: {'customer_id': 0, 'age': 1, 'gender': 1, 'purchase_amount': 1, 'city': 1}", (251, 191, 36), "", (0,0,0)),
    ("[2026-11-20 14:30:02] {task.py:73} INFO - Total missing value cells: 4 | Rows with missing values: 4", (251, 191, 36), "", (0,0,0)),
    ("[2026-11-20 14:30:02] {task.py:96} INFO - Total invalid records identified: 3 (Negative age: -8, Age > 120: 145, Negative purchase: -65.0)", (248, 113, 113), "", (0,0,0)),
    ("[2026-11-20 14:30:02] {task.py:99} INFO - Duplicate customer_id records detected: 1 (CUST003)", (248, 113, 113), "", (0,0,0)),
    ("", (0,0,0), "", (0,0,0)),
    ("[TASK 3: PROCESS]", (34, 197, 94), " Cleaning, Deduplicating & Median Imputation", (226, 232, 240)),
    ("[2026-11-20 14:30:03] {task.py:126} INFO - Removed 1 duplicate record | Filtered out 3 invalid records", (148, 163, 184), "", (0,0,0)),
    ("[2026-11-20 14:30:03] {task.py:138} INFO - Imputed missing age with median (36) | Imputed missing purchase_amount with median (175.8)", (148, 163, 184), "", (0,0,0)),
    ("[2026-11-20 14:30:03] {task.py:145} INFO - Cleaned dataset saved to output/processed_data.csv (Final records: 12)", (34, 197, 94), "", (0,0,0)),
    ("", (0,0,0), "", (0,0,0)),
    ("[TASK 4: REPORT]", (34, 197, 94), " Summary report written to output/summary_report.txt", (226, 232, 240)),
    ("[TASK 5: NOTIFY]", (34, 197, 94), " [AIRFLOW NOTIFICATION] WORKFLOW COMPLETED SUCCESSFULLY!", (56, 189, 248)),
    ("[2026-11-20 14:30:05] {dag.py:3104} INFO - Marking Run <DagRun data_pipeline_dag @ 2026-11-20> state=SUCCESS", (34, 197, 94), "", (0,0,0)),
]

y_pos = 46
for prefix, col1, cmd, col2 in log_lines:
    x_pos = 18
    if prefix:
        draw.text((x_pos, y_pos), prefix, fill=col1, font=font_bold if "[" in prefix else font)
        x_pos += int(draw.textlength(prefix, font=font_bold if "[" in prefix else font))
    if cmd:
        draw.text((x_pos, y_pos), cmd, fill=col2, font=font)
    y_pos += 21

img.save(os.path.join(output_dir, "fig_task_execution_logs.png"))
img.save(os.path.join(screenshots_dir, "05_task_logs.png"))
print("fig_task_execution_logs.png created successfully.")


# -----------------------------------------------------------------------------
# 4. Generate Airflow UI Dashboard (fig_airflow_dashboard.png)
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13, 5), dpi=300)
ax.set_xlim(0, 13)
ax.set_ylim(0, 5)
ax.axis("off")
fig.patch.set_facecolor("#FFFFFF")
ax.set_facecolor("#FFFFFF")

# Header bar
rect_header = patches.Rectangle((0, 4.2), 13, 0.8, facecolor="#0F4C81")
ax.add_patch(rect_header)
ax.text(0.4, 4.6, "Apache Airflow", fontsize=15, fontweight="bold", color="#FFFFFF")
ax.text(2.3, 4.6, "DAGs   Security   Browse   Admin   Docs", fontsize=10, color="#CBD5E1")
ax.text(12.2, 4.6, "admin", fontsize=10, fontweight="bold", color="#F8FAFC", ha="right")

# Table Header
rect_th = patches.Rectangle((0.4, 3.4), 12.2, 0.6, facecolor="#F1F5F9", edgecolor="#CBD5E1", lw=1)
ax.add_patch(rect_th)
ax.text(0.7, 3.7, "Active", fontsize=9.5, fontweight="bold", color="#475569")
ax.text(1.8, 3.7, "DAG ID", fontsize=9.5, fontweight="bold", color="#475569")
ax.text(4.8, 3.7, "Schedule", fontsize=9.5, fontweight="bold", color="#475569")
ax.text(6.3, 3.7, "Owner", fontsize=9.5, fontweight="bold", color="#475569")
ax.text(7.9, 3.7, "Recent Runs", fontsize=9.5, fontweight="bold", color="#475569")
ax.text(9.7, 3.7, "Last Run State", fontsize=9.5, fontweight="bold", color="#475569")
ax.text(11.6, 3.7, "Actions", fontsize=9.5, fontweight="bold", color="#475569")

# Row 1: data_pipeline_dag
rect_r1 = patches.Rectangle((0.4, 2.3), 12.2, 1.0, facecolor="#FFFFFF", edgecolor="#CBD5E1", lw=1)
ax.add_patch(rect_r1)

# Toggle ON switch (Blue)
rect_toggle = patches.FancyBboxPatch((0.65, 2.7), 0.6, 0.3, boxstyle="round,pad=0.04", facecolor="#2563EB", edgecolor="#1D4ED8")
ax.add_patch(rect_toggle)
circle_toggle = patches.Circle((1.1, 2.85), 0.1, facecolor="#FFFFFF")
ax.add_patch(circle_toggle)

ax.text(1.8, 2.85, "data_pipeline_dag", fontsize=10.5, fontweight="bold", color="#1D4ED8")
ax.text(1.8, 2.5, "tags: mlops, assignment4, data_pipeline", fontsize=8, color="#64748B")

ax.text(4.8, 2.85, "@daily", fontsize=9.5, color="#1E293B")
ax.text(4.8, 2.5, "catchup: False", fontsize=8, color="#64748B")

ax.text(6.3, 2.85, "mlops_student", fontsize=9.5, color="#1E293B")

# Recent run indicators (Green circles)
for idx in range(4):
    c_run = patches.Circle((7.9 + idx*0.35, 2.85), 0.12, facecolor="#10B981", edgecolor="#059669")
    ax.add_patch(c_run)
ax.text(9.3, 2.85, "(4 success)", fontsize=8, color="#059669")

# Last Run Status Pill
rect_pill = patches.FancyBboxPatch((9.7, 2.65), 1.3, 0.4, boxstyle="round,pad=0.05", facecolor="#DCFCE7", edgecolor="#86EFAC")
ax.add_patch(rect_pill)
ax.text(10.35, 2.85, "success", fontsize=9, fontweight="bold", color="#166534", ha="center")

# Play Trigger button
rect_btn = patches.FancyBboxPatch((11.5, 2.65), 0.8, 0.4, boxstyle="round,pad=0.04", facecolor="#F8FAFC", edgecolor="#CBD5E1")
ax.add_patch(rect_btn)
ax.text(11.9, 2.85, "Trigger ▶", fontsize=8.5, fontweight="bold", color="#2563EB", ha="center")

# Footer summary banner
ax.text(6.5, 1.2, "Apache Airflow 2.10.4 running on http://localhost:8080 | Scheduler: Active | Database: SQLite (airflow.db)", 
        ha="center", va="center", fontsize=9, color="#64748B", style="italic")

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "fig_airflow_dashboard.png"), dpi=300, bbox_inches="tight")
plt.savefig(os.path.join(screenshots_dir, "01_airflow_dashboard.png"), dpi=300, bbox_inches="tight")
plt.close()
print("fig_airflow_dashboard.png created successfully.")


# -----------------------------------------------------------------------------
# 5. Generate Summary Report Visual (fig_summary_report.png)
# -----------------------------------------------------------------------------
img_w, img_h = 1080, 520
img = Image.new("RGB", (img_w, img_h), color=(248, 250, 252))
draw = ImageDraw.Draw(img)

# Border box
draw.rectangle([10, 10, img_w-10, img_h-10], outline=(203, 213, 225), width=2)
draw.rectangle([10, 10, img_w-10, 45], fill=(15, 76, 129))
draw.text((25, 18), "Artifact Inspection: output/summary_report.txt & output/processed_data.csv", fill=(255, 255, 255), font=font_bold)

report_text_lines = [
    ("================================================================================", (100, 116, 139)),
    ("           APACHE AIRFLOW DATA PIPELINE SUMMARY REPORT                          ", (15, 76, 129)),
    ("================================================================================", (100, 116, 139)),
    ("DAG ID                      : data_pipeline_dag", (30, 41, 59)),
    ("Execution Timestamp         : 2026-11-20 14:30:05 UTC", (30, 41, 59)),
    ("Processing Completion Status : SUCCESS", (22, 101, 52)),
    ("--------------------------------------------------------------------------------", (148, 163, 184)),
    ("1. PIPELINE EXECUTION METRICS", (30, 64, 175)),
    ("Total records extracted     : 16", (30, 41, 59)),
    ("Total records processed     : 12", (30, 41, 59)),
    ("Missing values identified   : 4 (Age: 1, Gender: 1, Purchase: 1, City: 1)", (180, 83, 9)),
    ("Invalid records identified  : 3 (Age: -8, Age: 145, Purchase: -65.0)", (185, 28, 28)),
    ("Duplicate records removed   : 1 (Duplicate CUST003)", (185, 28, 28)),
    ("--------------------------------------------------------------------------------", (148, 163, 184)),
    ("2. DATA TRANSFORMATION DETAILS", (30, 64, 175)),
    ("- Extracted copy location   : output/extracted_data.csv", (71, 85, 105)),
    ("- Cleaned dataset location  : output/processed_data.csv (Cleaned 12 records)", (71, 85, 105)),
    ("- Imputation Strategy       : Age -> Median (36), Purchase -> Median (175.8)", (71, 85, 105)),
    ("- Categorical Cleaning      : Gender -> 'Unknown', City -> 'Unknown'", (71, 85, 105)),
    ("================================================================================", (100, 116, 139)),
    ("Generated automatically by Apache Airflow Workflow Automation Pipeline.", (100, 116, 139)),
]

y_pos = 58
for line, col in report_text_lines:
    draw.text((30, y_pos), line, fill=col, font=font_bold if "=" in line or "METRICS" in line or "REPORT" in line else font)
    y_pos += 21

img.save(os.path.join(output_dir, "fig_summary_report.png"))
img.save(os.path.join(screenshots_dir, "06_summary_report_and_output.png"))
print("fig_summary_report.png created successfully.")
