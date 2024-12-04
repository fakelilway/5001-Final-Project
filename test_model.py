import unittest
from data_model import DataModel
from io import StringIO


class TestDataModel(unittest.TestCase):
    def setUp(self):
        """
        Sets up a fresh DataModel instance and sample data for each test.
        """
        self.model = DataModel()

        # Sample valid CSV data for permits
        self.valid_permit_csv = StringIO(
            "IssueDate;GeoLocalArea\n"
            "2024-01-01;Downtown\n"
            "2024-02-15;Mount Pleasant\n"
            "2023-12-31;Kitsilano\n"  # Not in 2024
        )

        # Sample valid CSV data for licenses
        self.valid_license_csv = StringIO(
            "IssuedDate;LocalArea\n"
            "2024-01-05;Downtown\n"
            "2024-03-20;Kitsilano\n"
            "2023-11-25;Downtown\n"  # Not in 2024
        )

        # Invalid CSV data
        self.invalid_csv = StringIO("InvalidHeader1;InvalidHeader2\ninvalid;data")

    def test_init(self):
        """
        Tests the initialization of DataModel.
        """
        self.assertIsInstance(self.model.permits, list)
        self.assertIsInstance(self.model.licenses, list)
        self.assertEqual(len(self.model.permits), 0)
        self.assertEqual(len(self.model.licenses), 0)

    def test_parse_permit_data_happy_path(self):
        """
        Tests the happy path for parsing permit data.
        """
        self.model.parse_permit_data(self.valid_permit_csv.getvalue())
        self.assertEqual(len(self.model.permits), 3)
        self.assertEqual(self.model.permits[0].geo_local_area, "Downtown")
        self.assertEqual(self.model.permits[1].geo_local_area, "Mount Pleasant")
        self.assertEqual(self.model.permits[2].geo_local_area, "Kitsilano")

    def test_parse_license_data_happy_path(self):
        """
        Tests the happy path for parsing license data.
        """
        self.model.parse_license_data(self.valid_license_csv.getvalue())
        self.assertEqual(len(self.model.licenses), 3)
        self.assertEqual(self.model.licenses[0].local_area, "Downtown")
        self.assertEqual(self.model.licenses[1].local_area, "Kitsilano")
        self.assertEqual(self.model.licenses[2].local_area, "Downtown")

    def test_filter_data_2024(self):
        """
        Tests filtering of data for the year 2024.
        """
        self.model.parse_permit_data(self.valid_permit_csv.getvalue())
        self.model.parse_license_data(self.valid_license_csv.getvalue())
        self.model.filter_data_2024()

        self.assertEqual(len(self.model.permits), 2)  # Only permits from 2024
        self.assertEqual(len(self.model.licenses), 2)  # Only licenses from 2024
        # Check that permits are from 2024
        for permit in self.model.permits:
            self.assertEqual(permit.year, 2024)
        # Check that licenses are from 2024
        for license in self.model.licenses:
            self.assertEqual(license.year, 2024)

    def test_count_permits_by_month(self):
        """
        Tests counting permits by month.
        """
        self.model.parse_permit_data(self.valid_permit_csv.getvalue())
        self.model.filter_data_2024()
        counts = self.model.count_permits_by_month()
        expected_counts = {
            "2024-01": 1,
            "2024-02": 1,
        }
        self.assertEqual(counts, expected_counts)

    def test_count_licenses_by_month(self):
        """
        Tests counting licenses by month.
        """
        self.model.parse_license_data(self.valid_license_csv.getvalue())
        self.model.filter_data_2024()
        counts = self.model.count_licenses_by_month()
        expected_counts = {
            "2024-01": 1,
            "2024-03": 1,
        }
        self.assertEqual(counts, expected_counts)

    def test_prepare_line_chart_data(self):
        """
        Tests preparation of line chart data.
        """
        self.model.parse_permit_data(self.valid_permit_csv.getvalue())
        self.model.parse_license_data(self.valid_license_csv.getvalue())
        self.model.filter_data_2024()

        line_chart_data = self.model.prepare_line_chart_data()
        # Verify that the data has 12 months
        self.assertEqual(len(line_chart_data), 12)
        # Verify counts for specific months
        jan_data = next(item for item in line_chart_data if item["month"] == "2024-01")
        self.assertEqual(jan_data["permits"], 1)
        self.assertEqual(jan_data["licenses"], 1)

        feb_data = next(item for item in line_chart_data if item["month"] == "2024-02")
        self.assertEqual(feb_data["permits"], 1)
        self.assertEqual(feb_data["licenses"], 0)

    def test_prepare_grouped_bar_data(self):
        """
        Tests preparation of grouped bar chart data.
        """
        self.model.parse_permit_data(self.valid_permit_csv.getvalue())
        self.model.parse_license_data(self.valid_license_csv.getvalue())
        self.model.filter_data_2024()

        grouped_bar_data = self.model.prepare_grouped_bar_data()
        self.assertEqual(grouped_bar_data["Building Permits"], 2)
        self.assertEqual(grouped_bar_data["Business Licenses"], 2)

    def test_prepare_grouped_bar_data_with_neighborhood(self):
        """
        Tests preparation of grouped bar chart data with neighborhood filter.
        """
        self.model.parse_permit_data(self.valid_permit_csv.getvalue())
        self.model.parse_license_data(self.valid_license_csv.getvalue())
        self.model.filter_data_2024()

        grouped_bar_data = self.model.prepare_grouped_bar_data(neighborhood="Downtown")
        self.assertEqual(grouped_bar_data["Building Permits"], 1)
        self.assertEqual(grouped_bar_data["Business Licenses"], 1)

    def test_parse_invalid_csv(self):
        """
        Tests parsing invalid CSV data.
        """
        # Since parse methods handle exceptions internally and print errors,
        # we need to check that no permits or licenses are added
        self.model.parse_permit_data(self.invalid_csv.getvalue())
        self.model.parse_license_data(self.invalid_csv.getvalue())
        self.assertEqual(len(self.model.permits), 0)
        self.assertEqual(len(self.model.licenses), 0)

    def test_download_data(self):
        """
        Tests the download_data method with a mock URL.
        """
        # Since we cannot perform actual network requests, we'll skip testing this method
        pass  # Alternatively, you can use mocking libraries like unittest.mock

    def test_empty_data(self):
        """
        Tests the methods with empty data.
        """
        empty_csv = StringIO("IssueDate;GeoLocalArea\n")
        self.model.parse_permit_data(empty_csv.getvalue())
        self.assertEqual(len(self.model.permits), 0)
        empty_csv = StringIO("IssuedDate;LocalArea\n")
        self.model.parse_license_data(empty_csv.getvalue())
        self.assertEqual(len(self.model.licenses), 0)

        # Test data preparation methods with empty data
        self.model.filter_data_2024()
        line_chart_data = self.model.prepare_line_chart_data()
        for entry in line_chart_data:
            self.assertEqual(entry["permits"], 0)
            self.assertEqual(entry["licenses"], 0)

        grouped_bar_data = self.model.prepare_grouped_bar_data()
        self.assertEqual(grouped_bar_data["Building Permits"], 0)
        self.assertEqual(grouped_bar_data["Business Licenses"], 0)


if __name__ == "__main__":
    unittest.main()
