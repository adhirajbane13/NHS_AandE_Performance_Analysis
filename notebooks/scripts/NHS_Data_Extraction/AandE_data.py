import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
from datetime import datetime, timedelta
import re

class AandEData:
    def __init__(self):
        self.base_url = "https://www.england.nhs.uk/statistics/statistical-work-areas/ae-waiting-times-and-activity/ae-attendances-and-emergency-admissions-{}-{}/"

    def download_data(self, start_date, end_date):
        # Converting start and end dates to datetime objects
        start_dt = datetime.strptime(start_date, "%B %Y")
        end_dt = datetime.strptime(end_date, "%B %Y")

        # Generating a list of valid month-year strings (e.g., "January 2021", "February 2021", ...)
        current_dt = start_dt
        valid_month_years = set()

        while current_dt <= end_dt:
            valid_month_years.add(current_dt.strftime("%B %Y"))
            current_dt += timedelta(days=32)
            current_dt = current_dt.replace(day=1)

        # List to store DataFrames
        df_list = []

        # Iterating over possible NHS years
        for year in range(start_dt.year - 1, end_dt.year + 1):
            nhs_year = f"{year}-{str(year + 1)[-2:]}"  # e.g., "2021-22"
            url = self.base_url.format(year, str(year + 1)[-2:])

            print(f"Accessing: {url}")
            response = requests.get(url)

            if response.status_code != 200:
                print(f"Failed to access {url}")
                continue

            # Parsing the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Finding all links on the page
            for link in soup.find_all('a', href=True):
                link_text = link.get_text(strip=True)
                file_url = link['href']

                if "Monthly A&E" in link_text and "CSV" in link_text:
                    # Extracting the month and year from the link text using regex
                    match = re.search(r'(\bJanuary|\bFebruary|\bMarch|\bApril|\bMay|\bJune|\bJuly|\bAugust|\bSeptember|\bOctober|\bNovember|\bDecember) (\d{4})', link_text)
                    if match:
                        file_month = match.group(1)  # Extracted month
                        file_year = match.group(2)   # Extracted year
                        file_month_year = f"{file_month} {file_year}"

                        # Strict filtering: Downloading only if month-year is within the requested range
                        if file_month_year in valid_month_years:
                            # Converting relative URL to absolute if needed
                            if not file_url.startswith("http"):
                                file_url = requests.compat.urljoin(url, file_url)

                            # Downloading and loading the file directly into memory
                            file_response = requests.get(file_url)

                            if file_response.status_code == 200:
                                try:
                                    # Reading CSV file from memory (without saving to local disk)
                                    df = pd.read_csv(StringIO(file_response.text))

                                    # Standardizing column names
                                    column_mapping = {
                                        "Number of A&E attendances Type 1": "A&E attendances Type 1",
                                        "Number of A&E attendances Type 2": "A&E attendances Type 2",
                                        "Number of A&E attendances Other A&E Department": "A&E attendances Other A&E Department",
                                        "Number of attendances over 4hrs Type 1": "Attendances over 4hrs Type 1",
                                        "Number of attendances over 4hrs Type 2": "Attendances over 4hrs Type 2",
                                        "Number of attendances over 4hrs Other A&E Department": "Attendances over 4hrs Other Department"
                                    }

                                    # Renaming columns based on the mapping
                                    df.rename(columns=column_mapping, inplace=True)

                                    df["Year"] = file_year
                                    df["Month"] = file_month
                                    df_list.append(df)
                                    print(f"Downloaded & Loaded: {file_month_year}")
                                except Exception as e:
                                    print(f"Error reading {file_url}: {e}")
                            else:
                                print(f"Failed to download: {file_url}")

        # Combining all dataframes into one
        if df_list:
            combined_df = pd.concat(df_list, ignore_index=True)
            combined_df = combined_df[~combined_df["Parent Org"].str.contains("total", case=False, na=False, regex=True)]
            print("All valid CSV files loaded into memory and combined.")

            # Defining month order for sorting
            month_order = {
                "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
                "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
            }

            # Converting month names to numbers
            combined_df["Month_Number"] = combined_df["Month"].map(month_order)

            # Sorting by actual year first, then by month number
            combined_df = combined_df.sort_values(by=["Year", "Month_Number"]).drop(columns=["Month_Number"])
            return combined_df
        else:
            print("No valid CSV files were downloaded.")
