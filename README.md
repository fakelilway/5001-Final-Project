# 2024 Building Permits and Business Licences Issued Visualization in the City of Vancouver

## Project Overview
This MVC architecture project aims to visualize construction activities and business growth in Vancouver's neighborhoods for the year 2024. It focuses on displaying trends in building permits and business licenses issued, which reflect the economic activities within the city. The project utilizes data from the City of Vancouver's Open Data Portal and provides interactive visualizations through a user-friendly interface.

### Data Sources
1. **Issued Building Permits**: [Link to Dataset](https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/issued-building-permits/exports/csv?lang=en&timezone=America%2FLos_Angeles&use_labels=true&delimiter=%3B)
2. **Business Licenses**: [Link to Dataset](https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/business-licences/exports/csv?lang=en&timezone=America%2FLos_Angeles&use_labels=true&delimiter=%3B)

### Visualizations
The project provides two types of visualizations:
- **Grouped Bar Chart**: Displays the number of building permits and business licenses issued in different neighborhoods or the entire city for 2024.
- **Line Chart**: Shows monthly trends for building permits and business licenses issued in Vancouver during 2024, allowing users to filter by specific neighborhoods or the entire city.

### User Interactions
- **Visualization Selection**: Users can choose which type of visualization they want to see (either the grouped bar chart or the line chart).
- **Neighborhood Filter**: Users can specify a particular neighborhood or view data for the entire city for both visualizations.

## Project Structure
The codebase is organized into the following main components:

- **building_permits.py**: Handles loading and processing of building permit data from the CSV file.
- **business_licenses.py**: Handles loading and processing of business license data from the CSV file.
- **data_model.py**: Contains the classes for managing building permits and business licenses (i.e., `BuildingPermit` and `BusinessLicense`). It also includes methods to filter, aggregate, and prepare data for visualizations.
- **data_controller.py**: Manages the interaction between the data model and the views, including handling user requests to filter data and generate charts.
- **data_dashboard.py**: Implements the main interface for users, providing interactive options for visualization.
- **data_view.py**: Handles rendering of visualizations using matplotlib.
- **test_model.py**: Contains unit tests for validating the data model's methods, including parsing CSVs and preparing data for visualization.

## Installation and Setup
### Prerequisites
- Python 3.x
- Required Python packages: Pandas, Tkinter, Matplotlib (these are common packages and may already be installed in your environment).

### Installing Additional Packages
Install any missing Python packages via `pip`.

### Running the Project
1. **Download the CSV Files**: Ensure the CSV files for building permits and business licenses are downloaded or accessible from the provided links.
2. **Run the Dashboard**: Start the data dashboard using the following command:

```sh
python data_dashboard.py
```

This will launch the interactive dashboard, allowing users to explore visualizations of Vancouver's construction and business growth activities.

## Usage
- **Grouped Bar Chart**: Run the dashboard and select the "Show Grouped Bar Chart" option to view building permits and business licenses by neighborhood.
- **Line Chart**: Select the "Show Line Chart" option to see trends over time. Users can filter by neighborhood for a more localized view.
- **Type Neighborhood**: Type the specific neighborhood name wanted to display, or type "all" to show the data of the entire city.
  
## Testing
To run the unit tests:

```sh
python test_model.py
```

This will validate that the data parsing, aggregation, and preparation methods are working as intended.

## Limitations & Future Improvements
- **Performance**: Currently, downloading, parsing, and filtering data may take a while. Implementing sorting algorithms or optimizing the data pipeline can improve efficiency.
- **User Interface**: Future updates could include a dropdown menu for neighborhood selection, providing users with a more intuitive way to select areas.
- **Progress Indicators**: Adding a loading screen or progress indicator during data processing can enhance the user experience.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- City of Vancouver Open Data Portal for providing datasets used in this project.
