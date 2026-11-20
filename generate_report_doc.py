"""
generate_report_doc.py
Comprehensive generator for MLOps Assignment 4 Lab Report Word Document:
"Build Workflow Automation Using Apache Airflow"
Adheres strictly to the VIT Pune Department of AI & DS Lab Manual specifications.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

DOC_DIR = r"C:\College\SEM 5\MLOPs\Assignment_4"
REPORT_FILENAME = "MLOps_Assignment_4_Workflow_Automation_Airflow_Report.docx"
REPORT_ALT_FILENAME = "Assignment_Report.docx"

PRIMARY_COLOR = RGBColor(15, 76, 129)     # Deep Classic Blue (#0F4C81)
SECONDARY_COLOR = RGBColor(30, 64, 175)   # Subheading Blue (#1E40AF)
TEXT_COLOR = RGBColor(30, 41, 59)         # Dark Slate (#1E293B)
MUTED_COLOR = RGBColor(100, 116, 139)     # Slate Gray (#64748B)

def set_cell_background(cell, fill_hex):
    """Set background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set inner padding for a table cell (in twips: 20 twips = 1 pt)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_table_borders(table, color="D1D5DB", sz="4", val="single"):
    """Apply clean borders to a table."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_heading_1(doc, text):
    """Add a styled Heading 1."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = PRIMARY_COLOR
    return p

def add_heading_2(doc, text):
    """Add a styled Heading 2."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = SECONDARY_COLOR
    return p

def add_body_paragraph(doc, text, bold_prefix="", space_after=4):
    """Add a standard body paragraph."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
        r_pre.font.color.rgb = PRIMARY_COLOR
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(11)
    run.font.color.rgb = TEXT_COLOR
    return p

def add_bullet_point(doc, text, bold_prefix=""):
    """Add a bullet point paragraph."""
    p = doc.add_paragraph(style="List Paragraph")
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(10.5)
        r_pre.font.bold = True
        r_pre.font.color.rgb = PRIMARY_COLOR
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(10.5)
    run.font.color.rgb = TEXT_COLOR
    return p

def add_code_block(doc, code_text):
    """Add a clean shaded code box."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'<w:left w:val="single" w:sz="12" w:space="0" w:color="0F4C81"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(code_text.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(30, 41, 59)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_figure(doc, img_path, caption_text, width=Inches(5.8)):
    """Add a centered figure with an italicized caption."""
    if not os.path.exists(img_path):
        print(f"[WARN] Image not found: {img_path}")
        return
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(6)
    p_img.paragraph_format.space_after = Pt(2)
    p_img.paragraph_format.keep_with_next = True
    run_img = p_img.add_run()
    run_img.add_picture(img_path, width=width)
    
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(0)
    p_cap.paragraph_format.space_after = Pt(8)
    run_cap = p_cap.add_run(caption_text)
    run_cap.font.name = "Calibri"
    run_cap.font.size = Pt(9.5)
    run_cap.font.italic = True
    run_cap.font.bold = True
    run_cap.font.color.rgb = MUTED_COLOR

def build_document():
    doc = docx.Document()
    
    # Set page margins to 1 inch
    section = doc.sections[0]
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)
    section.header_distance = Inches(0.5)
    section.footer_distance = Inches(0.5)

    # -------------------------------------------------------------------------
    # COVER PAGE TABLE
    # -------------------------------------------------------------------------
    p_cover = doc.add_paragraph()
    p_cover.paragraph_format.space_after = Pt(4)
    run_c = p_cover.add_run("Cover Page")
    run_c.font.name = "Calibri"
    run_c.font.size = Pt(13)
    run_c.font.bold = True
    run_c.font.color.rgb = PRIMARY_COLOR

    cover_table = doc.add_table(rows=15, cols=2)
    cover_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cover_table.autofit = False
    set_table_borders(cover_table, color="B0C4DE", sz="6", val="single")

    cover_table.columns[0].width = Inches(2.2)
    cover_table.columns[1].width = Inches(4.3)

    # Row 0: Logo & Institute Heading
    cell_logo = cover_table.cell(0, 0)
    cell_inst = cover_table.cell(0, 1)
    set_cell_background(cell_logo, "F8FAFC")
    set_cell_background(cell_inst, "F8FAFC")
    set_cell_margins(cell_logo, top=140, bottom=140, left=140, right=140)
    set_cell_margins(cell_inst, top=140, bottom=140, left=140, right=140)

    # Add Logo
    logo_path = os.path.join(DOC_DIR, "vit_logo.jpeg")
    p_l = cell_logo.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if os.path.exists(logo_path):
        p_l.add_run().add_picture(logo_path, width=Inches(1.35))
    else:
        p_l.add_run("[VIT LOGO]")

    # Add Institute Header Text
    p_inst = cell_inst.paragraphs[0]
    p_inst.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r1 = p_inst.add_run("Bansilal Ramnath Agarwal Charitable Trust's\n")
    r1.font.name = "Calibri"
    r1.font.size = Pt(10)
    r1.font.color.rgb = MUTED_COLOR
    
    r2 = p_inst.add_run("Vishwakarma Institute of Technology, Pune\n")
    r2.font.name = "Calibri"
    r2.font.size = Pt(13)
    r2.font.bold = True
    r2.font.color.rgb = PRIMARY_COLOR
    
    r3 = p_inst.add_run("(An Autonomous Institute Affiliated to Savitribai Phule Pune University)")
    r3.font.name = "Calibri"
    r3.font.size = Pt(9.5)
    r3.font.italic = True
    r3.font.color.rgb = MUTED_COLOR

    # Table metadata rows
    table_data = [
        ("Department", "Department of Artificial Intelligence and Data Science"),
        ("Student Name", "Gaurang"),
        ("Class", "TY (Third Year B.Tech)"),
        ("Division", "B"),
        ("Roll No", "[Roll Number]"),
        ("PRN NO", "[PRN Number]"),
        ("Semester", "Semester V (Sem 5)"),
        ("Academic Year", "2026-27"),
        ("Subject Name & Code", "MLOps (AI3206C)"),
        ("Assignment No.", "4"),
        ("Title of Assignment", "Build Workflow Automation Using Apache Airflow"),
        ("Date of Performance", "10/11/2026"),
        ("Date of Submission", "20/11/2026"),
        ("", ""),
    ]

    for idx, (label, val) in enumerate(table_data, start=1):
        c0 = cover_table.cell(idx, 0)
        c1 = cover_table.cell(idx, 1)
        set_cell_margins(c0, top=70, bottom=70, left=120, right=120)
        set_cell_margins(c1, top=70, bottom=70, left=120, right=120)

        if idx % 2 == 1:
            set_cell_background(c0, "F8FAFC")
            set_cell_background(c1, "F8FAFC")
        else:
            set_cell_background(c0, "FFFFFF")
            set_cell_background(c1, "FFFFFF")

        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r_lbl = p0.add_run(label)
        r_lbl.font.name = "Calibri"
        r_lbl.font.size = Pt(10)
        r_lbl.font.bold = True
        r_lbl.font.color.rgb = PRIMARY_COLOR

        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r_val = p1.add_run(val)
        r_val.font.name = "Calibri"
        r_val.font.size = Pt(10)
        r_val.font.color.rgb = TEXT_COLOR
        if label in ["Assignment No.", "Title of Assignment", "Student Name"]:
            r_val.font.bold = True

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # AIM
    # -------------------------------------------------------------------------
    add_heading_1(doc, "Aim")
    add_body_paragraph(
        doc,
        "To design, implement, schedule, and automate an end-to-end multi-stage Data Preprocessing and "
        "Quality Auditing Pipeline using Apache Airflow (PythonOperator, DAG scheduling, and task dependencies) "
        "in a Linux/WSL2 environment, ensuring automated missing-value handling, outlier validation, deduplication, "
        "structured audit reporting, and pipeline execution notifications."
    )

    # -------------------------------------------------------------------------
    # PROBLEM STATEMENT
    # -------------------------------------------------------------------------
    add_heading_1(doc, "Problem Statement")
    add_body_paragraph(
        doc,
        "In enterprise Machine Learning Operations (MLOps), machine learning models are heavily dependent on continuous, "
        "reliable streams of preprocessed, high-quality data. In traditional setups, data ingestion, cleaning, validation, "
        "and transformation workflows are often implemented as monolithic Python scripts or manual cron jobs. These legacy "
        "approaches introduce catastrophic operational vulnerabilities:"
    )
    add_bullet_point(
        doc,
        "Lack of Dependency Tracking: Manual scripts and naive cron schedulers cannot natively represent complex task hierarchies "
        "or enforce directional dependencies (e.g., ensuring data cleaning only executes after data extraction and validation succeed).",
        "1. "
    )
    add_bullet_point(
        doc,
        "Silent Failures and Data Corruption: When intermediate steps fail silently or produce corrupt data (e.g., negative purchase amounts, "
        "impossible ages, missing categorical fields), downstream model training continues unchecked, leading to corrupt weights and degraded inference.",
        "2. "
    )
    add_bullet_point(
        doc,
        "Absence of Automatic Retries & Fault Recovery: Network timeouts, locked files, or transient IO failures terminate unmanaged scripts completely, "
        "requiring manual intervention without intelligent retry intervals or backoff mechanisms.",
        "3. "
    )
    add_bullet_point(
        doc,
        "Lack of Centralized Observability & Auditability: Traditional scripts provide no centralized UI to inspect execution states, task durations, "
        "historical run logs, or quantitative summary metrics across pipeline runs.",
        "4. "
    )
    add_body_paragraph(
        doc,
        "To solve these critical challenges, this assignment implements a production-grade workflow automation system using Apache Airflow. "
        "The project orchestrates five decoupled, sequential tasks (extract >> validate >> process >> report >> notify) scheduled via a Directed "
        "Acyclic Graph (DAG) with daily recurrence (@daily), catchup disabled, automated error-retries, centralized log streaming, and verifiable artifact export."
    )

    # -------------------------------------------------------------------------
    # OBJECTIVES
    # -------------------------------------------------------------------------
    add_heading_1(doc, "Objectives")
    add_body_paragraph(doc, "This assignment maps directly to the Course Outcomes (CO) for MLOps (AI3206C):")
    add_bullet_point(doc, "Understand workflow orchestration principles, Directed Acyclic Graph (DAG) mechanics, and the role of automated pipeline schedulers in the modern MLOps lifecycle.", "• Objective 1 (CO1): ")
    add_bullet_point(doc, "Implement automated data ingestion and validation for raw tabular datasets, auditing missing values, invalid records, and duplicate primary keys.", "• Objective 2 (CO2): ")
    add_bullet_point(doc, "Construct modular, isolated pipeline stages using PythonOperator abstractions to perform data extraction, data quality validation, numerical median imputation, categorical imputation, and deduplication.", "• Objective 3 (CO3): ")
    add_bullet_point(doc, "Configure programmatic task dependencies (extract >> validate >> process >> report >> notify), retry intervals, and recurring cron/preset schedules (@daily) with catchup=False.", "• Objective 4 (CO4): ")
    add_bullet_point(doc, "Deploy and monitor the pipeline through the Apache Airflow Webserver (Port 8080) and Scheduler, inspecting the Graph View, Grid View, Task Instances, and centralized execution logs.", "• Objective 5 (CO5): ")
    add_bullet_point(doc, "Generate automated pipeline audit reports (output/summary_report.txt) and console notification banners confirming artifact generation and execution success.", "• Objective 6 (CO6): ")

    # -------------------------------------------------------------------------
    # TOOLS, TECHNOLOGIES AND ENVIRONMENT
    # -------------------------------------------------------------------------
    add_heading_1(doc, "Tools, Technologies and Environment")
    
    env_table = doc.add_table(rows=8, cols=2)
    env_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    env_table.autofit = False
    set_table_borders(env_table, color="D1D5DB", sz="4", val="single")
    env_table.columns[0].width = Inches(2.2)
    env_table.columns[1].width = Inches(4.3)

    env_data = [
        ("Operating System", "Windows 11 with WSL2 (Ubuntu 22.04 LTS POSIX environment)"),
        ("Programming Language", "Python 3.10 / Python 3.12 (Dedicated Virtual Environment: airflow_env)"),
        ("Orchestration Framework", "Apache Airflow 2.10.4 (Installed via official constraints file)"),
        ("Core Libraries", "pandas 2.2.3, numpy 1.26.4, pendulum, python-dateutil"),
        ("Webserver & UI", "Airflow Webserver (Flask-AppBuilder, port 8080) with RBAC Authentication"),
        ("Scheduler & Database", "Airflow Scheduler (Heartbeat loop) & SQLite Metadata DB (airflow.db)"),
        ("Dataset", "data/input.csv (16 customer records with missing cells, invalid ages, and negative amounts)"),
        ("Output Artifacts", "output/extracted_data.csv, output/processed_data.csv, output/summary_report.txt"),
    ]

    for idx, (item, det) in enumerate(env_data):
        c0 = env_table.cell(idx, 0)
        c1 = env_table.cell(idx, 1)
        set_cell_margins(c0, top=70, bottom=70, left=120, right=120)
        set_cell_margins(c1, top=70, bottom=70, left=120, right=120)
        if idx % 2 == 0:
            set_cell_background(c0, "F8FAFC")
            set_cell_background(c1, "F8FAFC")
        else:
            set_cell_background(c0, "FFFFFF")
            set_cell_background(c1, "FFFFFF")

        p0 = c0.paragraphs[0]
        r0 = p0.add_run(item)
        r0.font.name = "Calibri"
        r0.font.size = Pt(10)
        r0.font.bold = True
        r0.font.color.rgb = PRIMARY_COLOR

        p1 = c1.paragraphs[0]
        r1 = p1.add_run(det)
        r1.font.name = "Calibri"
        r1.font.size = Pt(10)
        r1.font.color.rgb = TEXT_COLOR

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # -------------------------------------------------------------------------
    # BACKGROUND THEORY
    # -------------------------------------------------------------------------
    add_heading_1(doc, "Background Theory")

    add_heading_2(doc, "a) Introduction to Workflow Orchestration & DAGs")
    add_body_paragraph(
        doc,
        "In production machine learning systems, data engineering and model training pipelines are non-trivial distributed workflows. "
        "Workflow orchestration refers to the automated configuration, coordination, and management of computer systems and software pipelines. "
        "Rather than executing uncoordinated, standalone scripts, orchestration engines model business logic as a Directed Acyclic Graph (DAG)."
    )
    add_body_paragraph(
        doc,
        "A Directed Acyclic Graph (DAG) is a topological representation of a workflow where vertices represent discrete tasks and directed "
        "edges represent execution dependencies. Because the graph is strictly acyclic, execution loops are impossible, guaranteeing that "
        "tasks proceed monotonically towards a well-defined completion state. In MLOps, DAGs ensure that data validation cannot run before "
        "extraction completes, model training cannot commence on corrupt data, and deployment triggers only upon passing quality gates."
    )

    add_heading_2(doc, "b) Why Apache Airflow? Comparison with Legacy Alternatives")
    add_body_paragraph(
        doc,
        "Apache Airflow was developed at Airbnb to solve complex enterprise scheduling challenges. Workflows in Airflow are authored purely as "
        "Python code ('configuration-as-code'). This enables developers to utilize standard software engineering practices including version "
        "control, continuous integration, unit testing, dynamic task generation, and modular encapsulation."
    )

    # Comparison Table
    comp_table = doc.add_table(rows=5, cols=4)
    comp_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    comp_table.autofit = False
    set_table_borders(comp_table, color="D1D5DB", sz="4", val="single")
    comp_table.columns[0].width = Inches(1.5)
    comp_table.columns[1].width = Inches(1.6)
    comp_table.columns[2].width = Inches(1.6)
    comp_table.columns[3].width = Inches(1.8)

    headers = ["Feature", "Apache Airflow", "Cron Jobs", "Custom Python Scripts"]
    for i, h in enumerate(headers):
        c = comp_table.cell(0, i)
        set_cell_background(c, "0F4C81")
        set_cell_margins(c, top=80, bottom=80, left=100, right=100)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    comp_rows = [
        ("Workflow Definition", "Python Code (DAGs)", "Crontab text strings", "Monolithic scripts"),
        ("Dependency Resolution", "Native visual DAGs (>> / <<)", "None (Time-based only)", "Nested function calls"),
        ("Monitoring & UI", "Rich Web UI (Graph/Grid)", "None (Raw terminal/mail)", "None (stdout logs)"),
        ("Fault Recovery", "Automatic retries & alerts", "Fails silently", "Manual re-run required"),
    ]

    for row_idx, r_data in enumerate(comp_rows, start=1):
        for col_idx, val in enumerate(r_data):
            cell = comp_table.cell(row_idx, col_idx)
            set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
            if row_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")
            else:
                set_cell_background(cell, "FFFFFF")
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(9)
            if col_idx == 0:
                r.font.bold = True
                r.font.color.rgb = PRIMARY_COLOR
            elif col_idx == 1:
                r.font.bold = True
                r.font.color.rgb = SECONDARY_COLOR
            else:
                r.font.color.rgb = TEXT_COLOR

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_heading_2(doc, "c) Key Components and Terminology")
    add_bullet_point(doc, "The overarching workflow container defined in Python. It encapsulates tasks, scheduling intervals, start dates, and default retry arguments.", "1. DAG (Directed Acyclic Graph): ")
    add_bullet_point(doc, "The conceptual template that defines a unit of work. Common operators include PythonOperator, BashOperator, and SQLOperator.", "2. Operator: ")
    add_bullet_point(doc, "An instantiated node in the DAG graph representing a specific execution unit parameterized with inputs and dependencies.", "3. Task & Task Instance: ")
    add_bullet_point(doc, "The persistent daemon service that continuously monitors active DAGs, evaluates task dependencies, triggers scheduled runs, and submits runnable tasks to the executor.", "4. Airflow Scheduler: ")
    add_bullet_point(doc, "The Flask-AppBuilder web interface allowing engineers to monitor pipeline health, trigger runs manually, inspect real-time logs, and debug failures.", "5. Airflow Webserver: ")
    add_bullet_point(doc, "The central RDBMS (SQLite, PostgreSQL, or MySQL) storing the operational state of all DAGs, task runs, variables, user credentials, and execution history.", "6. Metadata Database: ")
    add_bullet_point(doc, "Cross-Communication mechanism allowing tasks to exchange lightweight metadata (such as record counts, error statistics, and file paths) across isolated execution environments.", "7. XCom (Cross-Communication): ")
    add_bullet_point(doc, "A DAG configuration parameter. When set to False, Airflow skips executing historical unrun intervals between the start_date and the current date upon activation.", "8. Catchup: ")

    add_heading_2(doc, "d) Benefits and Limitations")
    add_body_paragraph(
        doc,
        "Benefits: (1) Pure Python Authoring: Enables dynamic task generation, complex conditional branching, and seamless integration with Pandas, Scikit-Learn, and MLflow. "
        "(2) Observability: Out-of-the-box Graph, Grid, and Gantt charts provide complete visibility into task latency and bottlenecks. "
        "(3) Resilient Error Handling: Configurable retries, exponential backoffs, and execution timeouts prevent transient failure propagation."
    )
    add_body_paragraph(
        doc,
        "Limitations & Trade-offs: (1) POSIX Constraint on Windows: Airflow requires Linux-specific system calls (fcntl, fork), preventing native Windows execution and necessitating WSL2 or Docker containers. "
        "(2) Heavyweight Infrastructure: Running scheduler, webserver, and database daemons introduces operational overhead compared to lightweight alternatives. "
        "(3) XCom Size Limits: XComs are intended strictly for lightweight metadata; storing large dataframes in XCom strains the metadata database, requiring intermediate file storage."
    )

    # -------------------------------------------------------------------------
    # ARCHITECTURE / WORKFLOW DIAGRAM
    # -------------------------------------------------------------------------
    add_heading_1(doc, "Architecture / Workflow Diagram")
    add_body_paragraph(
        doc,
        "The following diagram illustrates the complete architectural design of the Apache Airflow automation pipeline. "
        "The workflow continuously monitors the raw customer dataset, executes five strictly chained tasks inside the "
        "data_pipeline_dag container, utilizes XComs for inter-task auditing, and persists clean data and summary reports."
    )
    
    arch_img = os.path.join(DOC_DIR, "architecture_diagram.png")
    add_figure(doc, arch_img, "Figure 1: End-to-End Apache Airflow Workflow Automation Pipeline Architecture", width=Inches(6.2))

    add_body_paragraph(
        doc,
        "Architectural Walkthrough: The pipeline begins at data/input.csv containing raw customer records. "
        "The Airflow Scheduler initiates a DAG Run based on the @daily schedule. Task 1 (extract) validates file presence, logs row counts, "
        "and stages an extraction copy. Task 2 (validate) audits null values across columns and checks for out-of-range numericals (-8, 145, -65.0). "
        "Task 3 (process) filters invalid rows, eliminates duplicate IDs, and performs median imputation. Task 4 (report) aggregates the execution "
        "metrics into output/summary_report.txt. Finally, Task 5 (notify) prints the success banner and artifact references."
    )

    # -------------------------------------------------------------------------
    # PROCEDURE (STEP-BY-STEP IMPLEMENTATION)
    # -------------------------------------------------------------------------
    add_heading_1(doc, "Procedure (Step-by-Step Implementation)")

    add_heading_2(doc, "Step 1: System Diagnostic & WSL2 Linux Environment Setup")
    add_body_paragraph(
        doc,
        "Because Apache Airflow depends on UNIX POSIX system calls (such as fcntl and process forking) that are unavailable natively on Windows, "
        "the environment was inspected via PowerShell. To provide a POSIX-compliant environment, Windows Subsystem for Linux (WSL2) with Ubuntu 22.04 LTS "
        "was configured."
    )
    add_code_block(
        doc,
        "# PowerShell (Administrator) - Install WSL2 Ubuntu Distribution\n"
        "wsl --install -d Ubuntu\n\n"
        "# Open Ubuntu Terminal and navigate to the project directory\n"
        "cd \"/mnt/c/College/SEM 5/MLOPs/Assignment_4\"\n"
        "pwd\n"
        "ls -la"
    )

    add_heading_2(doc, "Step 2: Dedicated Virtual Environment & Airflow 2.10.4 Installation")
    add_body_paragraph(
        doc,
        "To avoid package version conflicts and adhere to MLOps best practices, a dedicated virtual environment (airflow_env) was initialized. "
        "Apache Airflow 2.10.4 was installed using its official constraint file matching Python version specifications."
    )
    add_code_block(
        doc,
        "# Initialize and activate dedicated virtual environment\n"
        "sudo apt update && sudo apt install -y python3-venv python3-pip\n"
        "python3 -m venv airflow_env\n"
        "source airflow_env/bin/activate\n\n"
        "# Install Apache Airflow 2.10.4 with official constraint URL\n"
        "AIRFLOW_VERSION=2.10.4\n"
        "PYTHON_VERSION=\"$(python3 --version | cut -d ' ' -f 2 | cut -d '.' -f 1-2)\"\n"
        "CONSTRAINT_URL=\"https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt\"\n"
        "pip install --upgrade pip\n"
        "pip install \"apache-airflow==${AIRFLOW_VERSION}\" --constraint \"${CONSTRAINT_URL}\"\n"
        "pip install pandas numpy"
    )

    add_heading_2(doc, "Step 3: Database Migration & Administrator Account Creation")
    add_body_paragraph(
        doc,
        "The AIRFLOW_HOME environment variable was pointed to the assignment directory. Database migration was executed via airflow db migrate "
        "to generate the SQLite metadata schema, and an administrator account was created for Web UI access."
    )
    add_code_block(
        doc,
        "# Configure AIRFLOW_HOME pointing to the project root\n"
        "export AIRFLOW_HOME=\"$(pwd)\"\n\n"
        "# Initialize/Migrate Airflow metadata database\n"
        "airflow db migrate\n\n"
        "# Create Admin User for Web UI Authentication\n"
        "airflow users create \\\n"
        "    --username admin \\\n"
        "    --firstname Student \\\n"
        "    --lastname MLOps \\\n"
        "    --role Admin \\\n"
        "    --email student@mlops.edu \\\n"
        "    --password admin"
    )

    add_heading_2(doc, "Step 4: Creation of Controlled Sample Dataset with Edge Cases")
    add_body_paragraph(
        doc,
        "A realistic customer transaction dataset was created in data/input.csv containing 16 records across five columns: customer_id, age, gender, "
        "purchase_amount, and city. Deliberate missing values and invalid records were introduced to thoroughly exercise the validation stage."
    )
    add_code_block(
        doc,
        "# Injected Data Quality Edge Cases in data/input.csv:\n"
        "- Missing Values  : CUST006 (age=NaN), CUST007 (purchase_amount=NaN), CUST008 (gender=NaN), CUST009 (city=NaN)\n"
        "- Invalid Records : CUST010 (age=-8), CUST011 (age=145, >120 limit), CUST012 (purchase_amount=-65.0, <0 limit)\n"
        "- Duplicate Record: CUST003 (replicated record with identical customer_id)"
    )

    add_heading_2(doc, "Step 5: DAG Implementation & Five-Task Modular Pipeline")
    add_body_paragraph(
        doc,
        "The DAG was authored in dags/data_pipeline_dag.py utilizing PythonOperator. Five distinct callable functions were implemented: "
        "(1) extract_data, (2) validate_data, (3) process_data, (4) generate_report, and (5) send_notification. Inter-task metadata passing "
        "was coordinated via XComs."
    )
    add_code_block(
        doc,
        "# Task Dependency Definition in dags/data_pipeline_dag.py\n"
        "default_args = {\n"
        "    'owner': 'mlops_student',\n"
        "    'depends_on_past': False,\n"
        "    'retries': 1,\n"
        "    'retry_delay': timedelta(minutes=1),\n"
        "}\n\n"
        "with DAG(\n"
        "    dag_id='data_pipeline_dag',\n"
        "    default_args=default_args,\n"
        "    schedule_interval='@daily',\n"
        "    start_date=datetime(2025, 1, 1),\n"
        "    catchup=False,\n"
        ") as dag:\n"
        "    extract_task >> validate_task >> process_task >> report_task >> notify_task"
    )

    add_heading_2(doc, "Step 6: Starting Scheduler and Webserver Daemons")
    add_body_paragraph(
        doc,
        "Airflow services were started in separate terminal windows. The Webserver provides the HTTP graphical user interface on port 8080, "
        "while the Scheduler actively monitors DAG definitions, evaluates cron triggers, and schedules task instances."
    )
    add_code_block(
        doc,
        "# Terminal 1: Launch Airflow Webserver\n"
        "source airflow_env/bin/activate && export AIRFLOW_HOME=\"$(pwd)\"\n"
        "airflow webserver --port 8080\n\n"
        "# Terminal 2: Launch Airflow Scheduler\n"
        "source airflow_env/bin/activate && export AIRFLOW_HOME=\"$(pwd)\"\n"
        "airflow scheduler"
    )

    add_heading_2(doc, "Step 7: Manual DAG Triggering & Execution Monitoring")
    add_body_paragraph(
        doc,
        "The Web UI was accessed at http://localhost:8080 using the admin credentials. The data_pipeline_dag was toggled from OFF to ON, "
        "and manually triggered using the Trigger DAG button. The Graph View was monitored in real time as each task progressed through queued, "
        "running, and success states."
    )
    
    dash_img = os.path.join(DOC_DIR, "fig_airflow_dashboard.png")
    add_figure(doc, dash_img, "Figure 2: Airflow Web UI Dashboard Showing Active data_pipeline_dag and Execution States", width=Inches(6.0))

    graph_img = os.path.join(DOC_DIR, "fig_dag_graph.png")
    add_figure(doc, graph_img, "Figure 3: Airflow Graph View Confirming Sequential Execution and All Tasks in SUCCESS State", width=Inches(6.2))

    add_heading_2(doc, "Step 8: Task Instance & Real-Time Log Inspection")
    add_body_paragraph(
        doc,
        "Task instances were inspected via the Web UI to verify execution metadata (operator, duration, try count, XCom values) and ensure "
        "that log output accurately recorded missing values and invalid rows."
    )
    
    inst_img = os.path.join(DOC_DIR, "fig_task_instance_details.png")
    add_figure(doc, inst_img, "Figure 4: Task Instance Details Page for the validate Task (Duration: 1.17s, State: SUCCESS)", width=Inches(5.8))

    logs_img = os.path.join(DOC_DIR, "fig_task_execution_logs.png")
    add_figure(doc, logs_img, "Figure 5: Centralized Task Execution Logs Stream Auditing Data Quality and Imputation Steps", width=Inches(6.0))

    add_heading_2(doc, "Step 9: Output Verification and Summary Report Inspection")
    add_body_paragraph(
        doc,
        "Final outputs were audited in the output/ directory. The summary report (output/summary_report.txt) and the processed dataset "
        "(output/processed_data.csv) confirmed that 16 records were extracted, 4 missing values imputed, 3 invalid records removed, "
        "1 duplicate dropped, leaving 12 clean records."
    )
    
    rep_img = os.path.join(DOC_DIR, "fig_summary_report.png")
    add_figure(doc, rep_img, "Figure 6: Generated Pipeline Summary Report and Output CSV Verification", width=Inches(5.8))

    # -------------------------------------------------------------------------
    # CODE / CONFIGURATION FILES
    # -------------------------------------------------------------------------
    add_heading_1(doc, "Code / Configuration Files")
    add_body_paragraph(doc, "The primary source code defining the five-task workflow automation pipeline is presented below:")

    add_heading_2(doc, "1. Airflow DAG Definition (dags/data_pipeline_dag.py)")
    
    dag_path = os.path.join(DOC_DIR, "dags", "data_pipeline_dag.py")
    if os.path.exists(dag_path):
        with open(dag_path, "r", encoding="utf-8") as f:
            dag_code = f.read()
    else:
        dag_code = "# DAG file not found"
    add_code_block(doc, dag_code)

    add_heading_2(doc, "2. Raw Customer Input Dataset (data/input.csv)")
    csv_path = os.path.join(DOC_DIR, "data", "input.csv")
    if os.path.exists(csv_path):
        with open(csv_path, "r", encoding="utf-8") as f:
            csv_content = f.read()
    else:
        csv_content = "# CSV file not found"
    add_code_block(doc, csv_content)

    add_heading_2(doc, "3. Generated Summary Report (output/summary_report.txt)")
    rpt_path = os.path.join(DOC_DIR, "output", "summary_report.txt")
    if os.path.exists(rpt_path):
        with open(rpt_path, "r", encoding="utf-8") as f:
            rpt_content = f.read()
    else:
        rpt_content = "# Report file not found"
    add_code_block(doc, rpt_content)

    add_heading_2(doc, "4. Requirements and Constraints (requirements.txt)")
    req_path = os.path.join(DOC_DIR, "requirements.txt")
    if os.path.exists(req_path):
        with open(req_path, "r", encoding="utf-8") as f:
            req_content = f.read()
    else:
        req_content = "# requirements.txt not found"
    add_code_block(doc, req_content)

    add_body_paragraph(doc, "GitHub Repository Link: https://github.com/GaurangJagtap/A4", bold_prefix="Project Repository: ")

    # -------------------------------------------------------------------------
    # OUTPUT / RESULTS
    # -------------------------------------------------------------------------
    add_heading_1(doc, "Output / Results")
    add_body_paragraph(doc, "The output figures captured during workflow execution and artifact generation are summarized in the table below:")

    fig_table = doc.add_table(rows=7, cols=2)
    fig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    fig_table.autofit = False
    set_table_borders(fig_table, color="D1D5DB", sz="4", val="single")
    fig_table.columns[0].width = Inches(1.8)
    fig_table.columns[1].width = Inches(4.7)

    fig_captions = [
        ("Figure", "Description"),
        ("Figure 1", "End-to-End Apache Airflow Workflow Automation Pipeline Architecture Diagram"),
        ("Figure 2", "Airflow Web UI Dashboard Showing data_pipeline_dag active, scheduled @daily, and execution history"),
        ("Figure 3", "DAG Graph View displaying all 5 tasks (extract >> validate >> process >> report >> notify) in green SUCCESS state"),
        ("Figure 4", "Task Instance Details page for the validate task confirming PythonOperator execution and runtime duration"),
        ("Figure 5", "Centralized Task Execution Logs Stream detailing data quality checks, invalid record detection, and imputation"),
        ("Figure 6", "Generated Pipeline Summary Report (summary_report.txt) and Processed Dataset (processed_data.csv) verification"),
    ]

    for idx, (fig_id, desc) in enumerate(fig_captions):
        c0 = fig_table.cell(idx, 0)
        c1 = fig_table.cell(idx, 1)
        set_cell_margins(c0, top=70, bottom=70, left=120, right=120)
        set_cell_margins(c1, top=70, bottom=70, left=120, right=120)
        if idx == 0:
            set_cell_background(c0, "0F4C81")
            set_cell_background(c1, "0F4C81")
            col_text = RGBColor(255, 255, 255)
            bold_flag = True
        elif idx % 2 == 1:
            set_cell_background(c0, "F8FAFC")
            set_cell_background(c1, "F8FAFC")
            col_text = TEXT_COLOR
            bold_flag = False
        else:
            set_cell_background(c0, "FFFFFF")
            set_cell_background(c1, "FFFFFF")
            col_text = TEXT_COLOR
            bold_flag = False

        p0 = c0.paragraphs[0]
        r0 = p0.add_run(fig_id)
        r0.font.name = "Calibri"
        r0.font.size = Pt(9.5)
        r0.font.bold = bold_flag or (idx > 0)
        r0.font.color.rgb = col_text if idx == 0 else PRIMARY_COLOR

        p1 = c1.paragraphs[0]
        r1 = p1.add_run(desc)
        r1.font.name = "Calibri"
        r1.font.size = Pt(9.5)
        r1.font.bold = bold_flag
        r1.font.color.rgb = col_text

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # Pipeline Metrics Comparison Table
    add_heading_2(doc, "Data Transformation & Pipeline Audit Metrics")
    add_body_paragraph(doc, "A quantitative comparison between the initial raw dataset and the cleaned, transformed output dataset is shown below:")

    metrics_table = doc.add_table(rows=6, cols=3)
    metrics_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    metrics_table.autofit = False
    set_table_borders(metrics_table, color="D1D5DB", sz="4", val="single")
    metrics_table.columns[0].width = Inches(2.5)
    metrics_table.columns[1].width = Inches(2.0)
    metrics_table.columns[2].width = Inches(2.0)

    m_headers = ["Pipeline Audit Metric", "Raw Ingested Dataset", "Processed Cleaned Dataset"]
    for i, h in enumerate(m_headers):
        c = metrics_table.cell(0, i)
        set_cell_background(c, "0F4C81")
        set_cell_margins(c, top=80, bottom=80, left=100, right=100)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    m_rows = [
        ("Total Record Count", "16 records", "12 records (Valid & unique)"),
        ("Missing Value Cells (NaN)", "4 cells (Age, Gender, Purchase, City)", "0 cells (Median & 'Unknown' Imputed)"),
        ("Invalid Numerical Records", "3 records (-8, 145, -65.0)", "0 records (Completely filtered out)"),
        ("Duplicate Customer IDs", "1 duplicate (CUST003)", "0 duplicates (Deduplicated)"),
        ("Overall Pipeline Status", "Unprocessed / Raw", "SUCCESS (Fully Audited)"),
    ]

    for row_idx, r_data in enumerate(m_rows, start=1):
        for col_idx, val in enumerate(r_data):
            cell = metrics_table.cell(row_idx, col_idx)
            set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
            if row_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")
            else:
                set_cell_background(cell, "FFFFFF")
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(9)
            if col_idx == 0:
                r.font.bold = True
                r.font.color.rgb = PRIMARY_COLOR
            elif col_idx == 2:
                r.font.bold = True
                r.font.color.rgb = RGBColor(22, 101, 52)  # Dark green
            else:
                r.font.color.rgb = TEXT_COLOR

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # -------------------------------------------------------------------------
    # OBSERVATIONS AND ANALYSIS
    # -------------------------------------------------------------------------
    add_heading_1(doc, "Observations and Analysis")
    add_bullet_point(
        doc,
        "Automated Data Quality Auditing and Anomaly Identification: Task 2 (validate) successfully identified 4 missing value cells, "
        "3 invalid records (negative age -8, out-of-range age 145, negative purchase amount -65.0), and 1 duplicate customer ID without interrupting pipeline execution. "
        "This proves that programmatic data validation gates prevent silent corruptions from propagating downstream into ML models.",
        "1. "
    )
    add_bullet_point(
        doc,
        "Robust Imputation and Categorical Standardization: In Task 3 (process), missing numerical fields were cleanly imputed using median values "
        "(Age median: 36, Purchase Amount median: 175.8) to maintain statistical distribution stability against outliers. Missing categorical values "
        "were safely imputed with 'Unknown' and formatted into standard title-casing, eliminating scoring-time key errors.",
        "2. "
    )
    add_bullet_point(
        doc,
        "Strict Deduplication and Record Cleanliness: The pipeline dropped 1 duplicate record (CUST003) and filtered out 3 invalid records, transforming "
        "an initial raw set of 16 records into 12 verified, high-quality instances. This demonstrates how Airflow pipelines safeguard database consistency.",
        "3. "
    )
    add_bullet_point(
        doc,
        "Decoupled Communication via Airflow XComs: Passing metadata dictionary structures (total_extracted, total_missing_values, duplicates_removed) "
        "via XCom return values allowed Task 4 (report) to aggregate pipeline execution metrics cleanly without coupling task memory spaces or reloading raw data.",
        "4. "
    )
    add_bullet_point(
        doc,
        "Operating System Constraints and WSL2 Necessity: Airflow scheduler and webserver daemons rely on POSIX process forking and fcntl file locking, "
        "which fail natively on Windows (ModuleNotFoundError: No module named 'fcntl'). Utilizing WSL2 with Ubuntu 22.04 LTS provided seamless native Linux compatibility "
        "while maintaining file interoperability with the host Windows file system via /mnt/c/.",
        "5. "
    )
    add_bullet_point(
        doc,
        "Pipeline Idempotency, Retries, and Fault Tolerance: Configuring default_args with retries=1 and retry_delay=timedelta(minutes=1) ensures that "
        "transient IO or network hiccups do not permanently fail the pipeline. Furthermore, setting catchup=False prevents resource-exhausting backfills of historical DAG runs upon initial activation.",
        "6. "
    )

    # -------------------------------------------------------------------------
    # CONCLUSION
    # -------------------------------------------------------------------------
    add_heading_1(doc, "Conclusion")
    add_body_paragraph(
        doc,
        "Thus, we have successfully designed, implemented, scheduled, and automated an end-to-end multi-stage data preprocessing pipeline using Apache Airflow. "
        "By decomposing data workflows into five distinct, decoupled tasks (extract >> validate >> process >> report >> notify) and configuring daily scheduling (@daily) "
        "with automatic error retries, we eliminated manual intervention and silent data corruption. This assignment demonstrates how enterprise workflow orchestration "
        "provides the scalability, auditability, observability, and deterministic reliability essential for building production-ready MLOps systems."
    )

    # -------------------------------------------------------------------------
    # REFERENCES
    # -------------------------------------------------------------------------
    add_heading_1(doc, "References")
    references = [
        "Apache Airflow Documentation, 'Core Concepts: DAGs, Tasks, and Operators', Apache Software Foundation, https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/index.html, accessed 20/11/2026.",
        "Apache Airflow Documentation, 'PythonOperator Reference & XComs Guide', Apache Software Foundation, https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/python.html, accessed 20/11/2026.",
        "M. Treveil et al., Introducing MLOps: How to Scale Machine Learning in the Enterprise, O'Reilly Media, 2020.",
        "D. Sculley et al., 'Hidden Technical Debt in Machine Learning Systems', Advances in Neural Information Processing Systems (NeurIPS), 2015.",
        "L. E. Lwakatare et al., 'Large-scale Machine Learning Systems in Production: MLOps Framework and Case Studies', IEEE Software, vol. 37, no. 4, pp. 60-67, 2020.",
        "Microsoft Learn, 'Install Linux on Windows with WSL2', Microsoft Corporation, https://learn.microsoft.com/en-us/windows/wsl/install, accessed 20/11/2026."
    ]
    for ref in references:
        add_bullet_point(doc, ref, "• ")

    # Save documents
    out_path_1 = os.path.join(DOC_DIR, REPORT_FILENAME)
    out_path_2 = os.path.join(DOC_DIR, REPORT_ALT_FILENAME)
    doc.save(out_path_1)
    doc.save(out_path_2)
    print(f"Report successfully generated and saved to:\n  1. {out_path_1}\n  2. {out_path_2}")

if __name__ == "__main__":
    build_document()
