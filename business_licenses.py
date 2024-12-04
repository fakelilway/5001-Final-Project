"""
Zihan Jiang
CS 5001, Fall 2024
Final Project
This is the BusinessLicense class for the final project.
"""

import pandas as pd  # Import pandas for flexible date parsing


class BusinessLicense:
    """
    Purpose:
        Represents a single business license.
    Attributes:
        issued_date (datetime): The date when the license was issued.
        local_area (str): The geographical area in Vancouver where the
                          business operates.
    """

    def __init__(self, issued_date, local_area):
        """
        Purpose:
            Initializes a BusinessLicense object with the issued date and
            local area.
        Parameters:
            issued_date (str): The issued date as a string.
            local_area (str): The local area as a string.
        Returns:
            Nothing
        """
        self.issued_date = self.parse_date(issued_date)
        self.local_area = local_area.strip()
        print(
            f"Initialized BusinessLicense: issued_date={self.issued_date}, "
            f"local_area={self.local_area}"
        )

    @staticmethod
    def parse_date(date_str):
        """
        Purpose:
            Parses a date string into a datetime object
            using pandas.to_datetime for flexible parsing.
        Parameters:
            date_str (str): The date string to be parsed.
        Returns:
            datetime or None: The parsed datetime object, or None if parsing
                              fails or no date is provided.
        """
        if not date_str:
            print("No date provided to parse.")
            return None
        try:
            parsed_date = pd.to_datetime(date_str.strip(), errors="coerce")
            if pd.isna(parsed_date):
                print(f"Failed to parse date: {date_str}")
                return None
            print(f"Parsed date successfully: {parsed_date}")
            return parsed_date
        except Exception as e:
            print(f"Failed to parse date: {date_str} with error {e}")
            return None

    @property
    def year(self):
        """
        Purpose:
            Returns the year part of the issued date.
        Parameters:
            Nothing
        Returns:
            int or None: The year, or None if issued_date is None.
        """
        if self.issued_date:
            return self.issued_date.year
        return None

    @property
    def month(self):
        """
        Purpose:
            Returns the month part of the issued date.
        Parameters:
            Nothing
        Returns:
            int or None: The month, or None if issued_date is None.
        """
        if self.issued_date:
            return self.issued_date.month
        return None

    @property
    def year_month(self):
        """
        Purpose:
            Returns the issued date formatted as 'YYYY-MM'.
        Parameters:
            Nothing
        Returns:
            str or None: The formatted date string, or None if issued_date is
                         None.
        """
        if self.issued_date:
            return self.issued_date.strftime("%Y-%m")
        return None
