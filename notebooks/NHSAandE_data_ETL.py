import pandas as pd
import requests
from io import StringIO
import numpy as np
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from scripts.NHS_Data_Extraction.AandE_data import AandEData
import subprocess
import os
import time
from datetime import datetime

# Automatically set end_date to current month-year
start_date = "April 2018"
end_date = datetime.today().strftime("%B %Y")  # e.g., "March 2025"

# # Run docker-compose up -d to start PostgreSQL container
# DOCKER_PATH = "C:\\UoS_Lab\\Jobs\\Projects\\NHS_Data_Projects\\NHSA&E_Performance_Analysis_and_Forecasting\\notebooks" 

# print("Starting Docker container...")
# subprocess.run(["docker-compose", "up", "-d"], cwd=DOCKER_PATH)

# # Step 3: Wait for PostgreSQL to fully start
# print("Waiting for PostgreSQL to initialize...")
# time.sleep(10)  # ⏱️ Adjust if needed based on your system

combined_df = AandEData().download_data(start_date,end_date)

# Checking for missing values after dropping unnecessary columns
missing_values_after_cleanup = combined_df.isnull().sum()
print("Missing values in dataset after initial cleanup:")
print(missing_values_after_cleanup[missing_values_after_cleanup > 0])

categorical_columns = ['Org Code', 'Parent Org', 'Org name']
for col in categorical_columns:
    combined_df[col] = combined_df[col].astype('category')

columns_to_keep = ['Period', 'Org Code', 'Parent Org', 'Org name']  # Columns to be kept

# Identifying columns to drop (those with null values but NOT in columns_to_keep)
columns_to_drop = [col for col in combined_df.columns if col not in columns_to_keep and combined_df[col].isnull().any()]

# Dropping only those columns
combined_df.drop(columns=columns_to_drop, inplace=True)

combined_df.dropna(inplace=True) # Dropping rows with missing values

# Check for duplicate rows
duplicate_count = combined_df.duplicated().sum()
print(f"Number of duplicate rows: {duplicate_count}")

if duplicate_count > 0:
    # Drop duplicate rows
    combined_df.drop_duplicates(inplace=True)
    print("Duplicate rows removed!")

# Convert 'Period' to datetime format (Month-Year format)
combined_df["Period"] = pd.to_datetime(combined_df["Month"] + " " + combined_df["Year"].astype(str), format="%B %Y")

# Convert to Year-Month format (YYYY-MM) for analysis
combined_df["Period"] = combined_df["Period"].dt.strftime("%Y-%m")

# Verify the conversion
print("Converted 'Period' column data type:")
print(combined_df.dtypes["Period"])

# Display unique periods to confirm formatting
print("\nUnique periods in dataset:")
print(combined_df["Period"].unique())

print("Data cleaning completed!\n")
print(combined_df.info())
print("\n")

# Define PostgreSQL database credentials
POSTGRES_URL = "localhost:5432"
POSTGRES_DB = "mydatabase"
POSTGRES_USER = "myuser"
POSTGRES_PASSWORD = "mypassword"

# Create the database URL for SQLAlchemy
database_url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_URL}/{POSTGRES_DB}"

# Create an engine
engine = create_engine(database_url)

# Optional: Use a sessionmaker if you plan to do ORM operations
Session = sessionmaker(bind=engine)
session = Session()
combined_df.to_sql(
    name='nhs_ae_attendances',  # Name of the table to write to
    con=engine,  # SQLAlchemy engine created earlier
    index=False,  # Do not write DataFrame index as a column
    if_exists='replace'  # If table exists, drop it, recreate it, and insert data
)

with engine.connect() as connection:
    result = connection.execute(text('''SELECT * FROM nhs_ae_attendances ORDER BY "Period" DESC LIMIT 5'''))
    for row in result:
        print(row)

session.close()
print("ETL completed and data loaded into PostgreSQL!")
