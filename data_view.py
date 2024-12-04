"""
Zihan Jiang
CS 5001, Fall 2024
Final Project
This is the view file for the final project.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class DataView:
    """
    Purpose:
        Handles GUI for the project, including rendering visualizations.

    Attributes:
        root (Tk): The main GUI window.
        neighborhood_var (StringVar): The variable for the neighborhood entry.
        neighborhood_entry (Entry): The entry widget for neighborhood selection.
        bar_chart_button (Button): The button for showing the grouped bar chart.
        line_chart_button (Button): The button for showing the line chart.
        chart_frame (Frame): The frame for displaying
    """

    def __init__(self):
        """
        Purpose:
            Initializes the main GUI window.
        Parameters:
            Nothing
        Returns:
            Nothing
        """
        self.root = tk.Tk()
        self.root.title("Data Visualization Dashboard")

        # Create layout
        self.create_widgets()

    def create_widgets(self):
        """
        Purpose:
            Creates GUI elements.
        Parameters:
            Nothing
        Returns:
            Nothing
        """
        # Dropdown for selecting neighborhood
        tk.Label(self.root, text="Select Neighborhood:").grid(
            row=0, column=0, padx=5, pady=5
        )
        self.neighborhood_var = tk.StringVar(value="all")
        self.neighborhood_entry = ttk.Entry(
            self.root, textvariable=self.neighborhood_var, width=30
        )
        self.neighborhood_entry.grid(row=0, column=1, padx=5, pady=5)

        # Buttons for visualizations
        self.bar_chart_button = ttk.Button(self.root, text="Show Grouped Bar Chart")
        self.bar_chart_button.grid(row=1, column=0, padx=5, pady=5)

        self.line_chart_button = ttk.Button(self.root, text="Show Line Chart")
        self.line_chart_button.grid(row=1, column=1, padx=5, pady=5)

        # Area for displaying the chart
        self.chart_frame = tk.Frame(self.root, width=800, height=600)
        self.chart_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def display_chart(self, figure):
        """
        Purpose:
            Displays a matplotlib figure in the GUI.
        Parameters:
            figure (Figure): A Matplotlib figure to display.
        Returns:
            Nothing
        """
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(figure, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def render_grouped_bar_chart(self, data):
        """
        Purpose:
            Renders a grouped bar chart with the given data.
        Parameters:
            data (dict): A dictionary with category names as keys and counts as values.
        Returns:
            Nothing
        """
        figure = Figure(figsize=(8, 6))
        ax = figure.add_subplot(111)
        ax.bar(data.keys(), data.values())
        ax.set_title("Grouped Bar Chart")
        ax.set_xlabel("Category")
        ax.set_ylabel("Count (Permits/Licenses)")

        self.display_chart(figure)

    def render_line_chart(self, data):
        """
        Purpose:
            Renders a line chart with the given data.
        Parameters:
            data (list): A list of dictionaries containing month, permits, and licenses counts.
        Returns:
            Nothing
        """
        figure = Figure(figsize=(8, 6))
        ax = figure.add_subplot(111)

        months = [entry["month"] for entry in data]
        permits = [entry["permits"] for entry in data]
        licenses = [entry["licenses"] for entry in data]

        ax.plot(months, permits, label="Building Permits", marker="o")
        ax.plot(months, licenses, label="Business Licenses", marker="o")
        ax.set_title("Line Chart")
        ax.set_xlabel("Time (Month)")
        ax.set_ylabel("Count (Permits/Licenses)")
        ax.legend()

        # Rotate x-axis labels for better readability
        ax.set_xticks(months)
        ax.set_xticklabels(months, rotation=45, ha="right")

        self.display_chart(figure)

    def show_error(self, message):
        """
        Purpose:
            Displays an error message.
        Parameters:
            message (str): The error message to display.
        Returns:
            Nothing
        """
        messagebox.showerror("Error", message)

    def start(self):
        """
        Purpose:
            Starts the main event loop for the GUI.
        Parameters:
            Nothing
        Returns:
            Nothing
        """
        self.root.mainloop()
