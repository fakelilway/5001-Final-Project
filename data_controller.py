"""
Zihan Jiang
CS 5001, Fall 2024
Final Project
This is the controller file for the final project.
"""


class DataController:
    """
    Purpose:
        Acts as the controller between the model and the view.

    Attributes:
        model (DataModel): The data model.
        view (DataView): The GUI view.
    """

    def __init__(self, model, view):
        """
        Purpose:
            Initializes the controller with the model and view.
        Parameters:
            model (DataModel): The data model.
            view (DataView): The GUI view.
        Returns:
            Nothing
        """
        self.model = model
        self.view = view

        # Set up button actions
        self.view.bar_chart_button.configure(command=self.show_grouped_bar_chart)
        self.view.line_chart_button.configure(command=self.show_line_chart)

    def normalize_neighborhood(self, neighborhood):
        """
        Purpose:
            Normalizes user input for neighborhood names.
        Parameters:
            neighborhood (str): The raw user input.
        Returns:
            str or None: The normalized name or None if "all".
        """
        neighborhood = neighborhood.strip().title()
        if neighborhood.lower() == "all":
            return None
        return neighborhood

    def show_grouped_bar_chart(self):
        """
        Purpose:
            Prepares data and delegates rendering of the grouped bar chart to the view.
        Parameters:
            Nothing
        Returns:
            Nothing
        """
        neighborhood = self.normalize_neighborhood(self.view.neighborhood_var.get())
        data = self.model.prepare_grouped_bar_data(neighborhood)
        self.view.render_grouped_bar_chart(data)

    def show_line_chart(self):
        """
        Purpose:
            Prepares data and delegates rendering of the line chart to the view.
        Parameters:
            Nothing
        Returns:
            Nothing
        """
        neighborhood = self.normalize_neighborhood(self.view.neighborhood_var.get())
        data = self.model.prepare_line_chart_data(neighborhood)
        self.view.render_line_chart(data)

    def run(self):
        """
        Purpose:
            Starts the GUI event loop.
        Parameters:
            Nothing
        Returns:
            Nothing
        """
        self.view.start()
