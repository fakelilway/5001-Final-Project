"""
Zihan Jiang
CS 5001, Fall 2024
Final Project
This is the dashboard driver file for the final project.
"""

from data_model import DataModel
from data_controller import DataController
from data_view import DataView


def main():
    """
    Purpose:
        Entry point for the program. Sets up the model, view, and controller.
    
    Parameters:
        Nothing

    Returns:
        Nothing
    """
    # Initialize the Model
    data_model = DataModel()

    # Load data into the model
    print("Loading data...")
    permits_url = (
        "https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/"
        "issued-building-permits/exports/csv?lang=en&timezone=America%2FLos_"
        "Angeles&use_labels=true&delimiter=%3B"
    )
    licenses_url = (
        "https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/"
        "business-licences/exports/csv?lang=en&timezone=America%2FLos_"
        "Angeles&use_labels=true&delimiter=%3B"
    )

    # Download and parse data
    permits_data = data_model.download_data(permits_url)
    licenses_data = data_model.download_data(licenses_url)

    if not permits_data and not licenses_data:
        print("Failed to load permits and licenses data.")
        return
    elif not permits_data:
        print("Failed to load permits data.")
        return
    elif not licenses_data:
        print("Failed to load licenses data.")
        return

    data_model.parse_permit_data(permits_data)
    data_model.parse_license_data(licenses_data)
    data_model.filter_data_2024()

    # Initialize the View
    data_view = DataView()

    # Initialize the Controller
    data_controller = DataController(data_model, data_view)

    # Start the application
    data_controller.run()


if __name__ == "__main__":
    main()
