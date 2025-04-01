# <img src="notebooks/nhs-logo-880x4951.jpeg" alt="NHS Logo" width="60" height="30"/> A&E Performance Analytics Dashboard

An end-to-end analytics project visualizing Accident & Emergency (A&E) department performance across NHS Trusts in England, using **Python**, **PostgreSQL**, **Docker**, and **Power BI**. The dashboard offers interactive filtering, KPI tracking, drill-through insights, and data storytelling to support data-informed healthcare decisions.

---

## Motivation

With increasing strain on NHS A&E services, visualizing performance trends over time and across trusts is essential for capacity planning, policy design, and performance evaluation. This project aims to deliver a user-friendly and insightful dashboard that communicates the current state of NHS A&E services while enabling deep exploration.

---

## Tech Stack

- **Python**: ETL pipeline for data extraction, cleaning, and transformation  
- **PostgreSQL + Docker**: Structured storage and containerized database setup  
- **Power BI (Import Mode)**: Interactive data visualization using:
  - DAX (for custom KPIs, time intelligence)
  - Bookmarks and slicers for navigation and filtering
  - Drill-throughs and storytelling elements  
- **Windows Task Scheduler**: Automating ETL jobs with conda environment and Docker integration

---

## ETL Process

| Step | Description |
|------|-------------|
| Data Source | Monthly NHS A&E attendance extracted by web-scraping(Separate package created to extract data for fixed interval) |
| Cleaning | Handling missing values, duplicates, standardizing columns |
| Transformation | Formatting `Period`, extracting `Year` and `Month`, summarizing |
| Storage | Inserting the cleaned dataset into a PostgreSQL table (`nhs_ae_attendances`) using SQLAlchemy |
| Automation | `.bat` script scheduled using Windows Task Scheduler (with Docker + Conda activation) |

---

## Custom Python Package for Data Extraction

This project includes a **custom-built Python package** named `AandEData`, located in [`scripts/NHS_Data_Extraction/AandE_data.py`](notebooks/scripts/NHS_Data_Extraction/AandE_data.py). This package allows users to extract NHS A&E attendance data dynamically for any **start and end month-year range**.

```python
from scripts.NHS_Data_Extraction.AandE_data import AandEData

# Downloading data between April 2018 and current month
combined_df = AandEData().download_data("April 2018", "February 2025")
```

The module performs the following:
- Automatically downloads monthly CSVs from NHS England’s website  
- Merges the data  
- Returns a single DataFrame ready for cleaning, transformation and loading into a database

---

## Dashboard Features

### KPI Cards (Top Metrics)
- Total A&E Attendances  
- % Patients Waiting > 4 Hours 
- Emergency Admissions  
- 12+ Hour Waits from DTA to Admission  

### Visuals

- **Year-wise Trend in Total Attendances**  
  A line chart displaying annual A&E attendances across all NHS Trusts, helping identify long-term trends.  
  *Drill-through enabled* to explore monthly details.

- **NHS Trust-Level Attendance Breakdown by Department Type**  
  A clustered bar chart showing A&E attendances per trust, split across Type 1, Type 2, and Other departments.

- **NHS Trusts by Percentage of Patients Waiting Over 4 Hours**  
  A horizontal bar chart displaying **all NHS Trusts**, ranked by the percentage of patients who waited more than 4 hours across **all A&E department types**.  
  *Conditional formatting* helps highlight performance issues.

- **Monthly Total Attendances**  
  A trend chart that displays how total attendances vary month to month over time.

- **Dynamic Slicers (NHS Trust, Year)**  
  Enable real-time filtering of all visuals, enhancing interactivity and user control.

- **Data Storytelling Narrative**  
  A DAX-powered summary view that converts selected data into a plain-English narrative with navigation bookmarks.

## Dashboard Walkthrough

Experience the dashboard in action with this quick walkthrough showing interactive filtering, KPIs, and storytelling(Click on the video thumbnail below):

[![Watch the demo](https://img.youtube.com/vi/n97qh0wzoUI/0.jpg)](https://www.youtube.com/watch?v=n97qh0wzoUI)
[Dashboard Link](<iframe title="NHS_AandE_DB" width="1140" height="541.25" src="https://app.powerbi.com/reportEmbed?reportId=fd34ce1e-378a-458e-b8ad-879d48531b12&autoAuth=true&ctid=da123707-1b61-44c7-bdaa-98e62f1ea74e" frameborder="0" allowFullScreen="true"></iframe>)
---

##  NHS A&E Definitions

> Based on NHS England’s official definitions (v4.0, July 2019)

### A&E Department Types
- **Type 1**: Consultant-led 24-hour major emergency unit with full resuscitation
- **Type 2**: Consultant-led specialty A&E (e.g., eye hospital, dental)
- **Type 3**: Minor Injury Units / Walk-in / Urgent Care Centre (nurse or GP-led)

### Key Metrics
- **A&E Attendances**: Total unplanned visits (Type 1, 2, 3)
- **>4 Hour Waits**: Patients staying in A&E over 4 hours from arrival to departure
- **12+ Hour Delays**: Patients waiting >12 hours from Decision-to-Admit (DTA) to admission
- **Emergency Admissions**: Patients admitted via A&E departments

[Read the full NHS A&E Definitions document here][(https://www.england.nhs.uk/statistics/statistical-work-areas/ae-waiting-times-and-activity/](https://www.england.nhs.uk/statistics/wp-content/uploads/sites/2/2019/07/AE-Attendances-Emergency-Definitions-v4.0-final-July-2019.pdf))

---

## Project Structure
```
NHS_AandE_Performance_Analysis/
│
├── dashboards/                      # Power BI dashboard files
│   └── NHS_AandE_DB.pbix
│
├── notebooks/                       # Analysis notebooks and related assets
│   ├── scripts/
│   └── NHS_Data_Extraction/
│       ├── __init__.py         # Makes this a Python package
│       └── AandE_data.py       # Custom package for data extraction
│   │
│   ├── AE-Attendances-Emergency-Definitions-v4.0-final-July-2019.pdf   # Official A&E terminology definitions
│   ├── Data_Analysis.ipynb         # Initial data exploration
│   ├── Data_Analysis_new.ipynb     # Cleaned and final analysis notebook
│   ├── Data_Analysis_new.html      # HTML export of final notebook
│   ├── Data_Analysis_new.pdf       # PDF version of analysis
│   ├── NHSAandE_data_ETL.py        # ETL pipeline script for database load
│   ├── docker-compose.yaml         # Docker config file for PostgreSQL
│   ├── etl_log.txt                 # Log file for ETL execution
│   └── nhs-logo-880x4951.jpeg      # NHS logo for dashboard branding
│
├── .gitignore
├── requirements.txt                # Python dependencies
├── Setup.py
├── run_etl.bat                     #  Windows batch file for scheduling ETL jobs
└── README.md                       # Project overview and documentation
```

---

## Usage Guide

### Start PostgreSQL (Docker)
```bash
cd path/to/project-docker-file
docker-compose up -d
```

### Run ETL Script
```bash
conda activate ./nhs_env
python notebooks/NHSAandE_data_ETL.py
```

### Automate
Use `run_etl.bat` with **Windows Task Scheduler** for periodic updates.

---

## Author

**Adhiraj Banerjee**  
Data Analyst, [LinkedIn](https://www.linkedin.com/in/adhiraj-banerjee/)
