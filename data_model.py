"""
Zihan Jiang
CS 5001, Fall 2024
Final Project
This is the model file for the final project.
"""

import requests  # For downloading data from the web
import pandas as pd  # For data manipulation and parsing
from io import StringIO  # For treating strings as file-like objects
from building_permits import BuildingPermit  # Import BuildingPermit class
from business_licenses import BusinessLicense  # Import BusinessLicense class


class DataModel:
    """
    Purpose:
        Handles data downloading, cleaning, parsing, and analysis.
    Attributes:
        permits (list): A list to store BuildingPermit objects.
        licenses (list): A list to store BusinessLicense objects.
    """

    def __init__(self):
        """
        Purpose:
            Initializes the DataModel with empty lists for permits & licenses.
        Parameters:
            None
        Returns:
            Nothing
        """
        self.permits = []  # List to store BuildingPermit objects
        self.licenses = []  # List to store BusinessLicense objects
        print("Initialized DataModel with empty permits and licenses lists.")

    def download_data(self, url):
        """
        Purpose:
            Downloads data from the given URL.
        Parameters:
            url (str): The URL to download data from.
        Returns:
            str or None: The content of the response decoded as 'utf-8',
            or None if an error occurs.
        """
        print(f"Attempting to download data from URL: {url}")
        try:
            response = requests.get(url)  # Send a GET request to the URL
            response.raise_for_status()  # Raise an HTTPError if the response
            # was unsuccessful
            print("Data downloaded successfully.")
            return response.content.decode("utf-8")  # Decode response content
        except requests.exceptions.RequestException as e:
            print(f"Error downloading data: {e}")  # Print an error message
            return None  # Return None if an error occurs

    def parse_permit_data(self, csv_data):
        """
        Purpose:
            Parses CSV data into BuildingPermit objects.
        Parameters:
            csv_data (str): The CSV data as a string.
        Returns:
            Nothing
        """
        print("Parsing building permits data...")
        try:
            data = pd.read_csv(StringIO(csv_data), delimiter=";")
            for _, row in data.iterrows():
                issued_date = row.get("IssueDate", None)
                geo_local_area = row.get("GeoLocalArea", None)
                issued_date = str(issued_date).strip() if pd.notna(issued_date) else ""
                geo_local_area = (
                    str(geo_local_area).strip() if pd.notna(geo_local_area) else ""
                )
                permit = BuildingPermit(issued_date, geo_local_area)
                if permit.issued_date:  # Only add valid permits
                    self.permits.append(permit)
                    print(f"Added permit: {permit}")
            print(f"Total permits parsed: {len(self.permits)}")
        except Exception as e:
            print(f"Error parsing building permits data: {e}")

    def parse_license_data(self, csv_data):
        """
        Purpose:
            Parses CSV data into BusinessLicense objects.
        Parameters:
            csv_data (str): The CSV data as a string.
        Returns:
            Nothing
        """
        print("Parsing business licenses data...")
        try:
            data = pd.read_csv(StringIO(csv_data), delimiter=";")
            for _, row in data.iterrows():
                issued_date = row.get("IssuedDate", None)
                local_area = row.get("LocalArea", None)
                issued_date = str(issued_date).strip() if pd.notna(issued_date) else ""
                local_area = str(local_area).strip() if pd.notna(local_area) else ""
                license = BusinessLicense(issued_date, local_area)
                if license.issued_date:  # Only add valid licenses
                    self.licenses.append(license)
                    print(f"Added license: {license}")
            print(f"Total licenses parsed: {len(self.licenses)}")
        except Exception as e:
            print(f"Error parsing business licenses data: {e}")

    def filter_data_2024(self):
        """
        Purpose:
            Filters permits and licenses to include only those issued in the
            year 2024.
        Parameters:
            None
        Returns:
            Nothing
        """
        print("Filtering data for the year 2024...")
        initial_permits_count = len(self.permits)
        initial_licenses_count = len(self.licenses)
        self.permits = [permit for permit in self.permits if permit.year == 2024]
        self.licenses = [license for license in self.licenses if license.year == 2024]
        print(f"Filtered permits from {initial_permits_count} to {len(self.permits)}.")
        print(
            f"Filtered licenses from {initial_licenses_count} to "
            f"{len(self.licenses)}."
        )

    def count_permits_by_month(self, neighborhood=None):
        """
        Purpose:
            Counts the number of building permits by month, optionally filtered
            by neighborhood.
        Parameters:
            neighborhood (str): The neighborhood to filter by, or None for all
                                neighborhoods.
        Returns:
            dict: A dictionary with 'YYYY-MM' as keys and counts as values.
        """
        print(f"Counting permits by month for neighborhood: {neighborhood}")
        counts = {}
        for permit in self.permits:
            if neighborhood is None or permit.geo_local_area == neighborhood:
                if permit.year_month not in counts:
                    counts[permit.year_month] = 0
                counts[permit.year_month] += 1
        print(f"Permit counts by month: {counts}")
        return counts

    def count_licenses_by_month(self, neighborhood=None):
        """
        Purpose:
            Counts the number of business licenses by month, optionally filtered
            by neighborhood.
        Parameters:
            neighborhood (str): The neighborhood to filter by, or None for all
                                neighborhoods.
        Returns:
            dict: A dictionary with 'YYYY-MM' as keys and counts as values.
        """
        print(f"Counting licenses by month for neighborhood: {neighborhood}")
        counts = {}
        for license in self.licenses:
            if neighborhood is None or license.local_area == neighborhood:
                if license.year_month not in counts:
                    counts[license.year_month] = 0
                counts[license.year_month] += 1
        print(f"License counts by month: {counts}")
        return counts

    def prepare_line_chart_data(self, neighborhood=None):
        """
        Purpose:
            Prepares data for the line chart visualization.
        Parameters:
            neighborhood (str): The neighborhood to filter by, or None for all
                                neighborhoods.
        Returns:
            list: A list of dictionaries containing month, permits,
            and licenses counts.
        """
        print(f"Preparing line chart data for neighborhood: {neighborhood}")
        permit_counts = self.count_permits_by_month(neighborhood)
        license_counts = self.count_licenses_by_month(neighborhood)

        # Ensure all months are represented
        months = [f"2024-{month:02d}" for month in range(1, 13)]
        data = []
        for month in months:
            data.append(
                {
                    "month": month,
                    "permits": permit_counts.get(month, 0),
                    "licenses": license_counts.get(month, 0),
                }
            )
        print(f"Line chart data: {data}")
        return data

    def prepare_grouped_bar_data(self, neighborhood=None):
        """
        Purpose:
            Prepares data for the grouped bar chart visualization.
        Parameters:
            neighborhood (str): The neighborhood to filter by, or None for all
                                neighborhoods.
        Returns:
            dict: A dictionary containing total permits and total licenses.
        """
        print(f"Preparing grouped bar chart data for neighborhood: {neighborhood}")
        total_permits = len(
            [
                permit
                for permit in self.permits
                if neighborhood is None or permit.geo_local_area == neighborhood
            ]
        )
        total_licenses = len(
            [
                license
                for license in self.licenses
                if neighborhood is None or license.local_area == neighborhood
            ]
        )
        grouped_data = {
            "Building Permits": total_permits,
            "Business Licenses": total_licenses,
        }
        print(f"Grouped bar chart data: {grouped_data}")
        return grouped_data
