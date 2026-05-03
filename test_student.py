import unittest

from proj2 import Row, Node, parse_row, recursive_func, read_csv_lines, listlen, filter_rows


class TestProj2(unittest.TestCase):

    def test_parse_row_converts_types_and_missing_values(self):
        fields = ["USA", "2020", "", "0.3", "200.0", "0.6", "500.0", "1.5"]
        row = parse_row(fields)

        self.assertEqual(row.country, "USA")
        self.assertEqual(row.year, 2020)
        self.assertIsNone(row.electricity_and_heat_co2_emissions)
        self.assertAlmostEqual(row.energy_co2_emissions, 200.0)

    def test_recursive_func_builds_linked_list(self):
        row1 = Row("A", 2000, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0)
        row2 = Row("B", 2001, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0)

        linked = recursive_func([row1, row2])

        self.assertIsInstance(linked, Node)
        self.assertEqual(linked.value, row1)
        self.assertEqual(linked.next.value, row2)
        self.assertIsNone(linked.next.next)

    def test_read_csv_lines_returns_linked_list(self):
        data = read_csv_lines("sample.csv")

        self.assertIsInstance(data, Node)
        self.assertEqual(data.value.country, "USA")
        self.assertEqual(listlen(data), 5)

    def test_read_csv_lines_missing_file_returns_none(self):
        data = read_csv_lines("does_not_exist.csv")
        self.assertIsNone(data)

    def test_listlen_empty(self):
        self.assertEqual(listlen(None), 0)

    def test_listlen_nonempty(self):
        data = read_csv_lines("sample.csv")
        self.assertEqual(listlen(data), 5)

    def test_filter_rows_equal_country(self):
        data = read_csv_lines("sample.csv")
        filtered = filter_rows(data, "country", "equal", "USA")

        self.assertEqual(listlen(filtered), 2)
        self.assertEqual(filtered.value.country, "USA")
        self.assertEqual(filtered.next.value.country, "USA")

    def test_filter_rows_greater_than_numeric(self):
        data = read_csv_lines("sample.csv")
        filtered = filter_rows(data, "energy_co2_emissions", "greater_than", 150.0)

        self.assertEqual(listlen(filtered), 3)

    def test_filter_rows_less_than_numeric(self):
        data = read_csv_lines("sample.csv")
        filtered = filter_rows(data, "total_co2_emissions_excluding_lucf", "less_than", 400.0)

        self.assertEqual(listlen(filtered), 2)

    def test_filter_rows_skips_missing_values(self):
        data = read_csv_lines("sample.csv")
        filtered = filter_rows(data, "electricity_and_heat_co2_emissions", "greater_than", 80.0)

        self.assertEqual(listlen(filtered), 2)

    def test_filter_rows_invalid_country_comparison(self):
        data = read_csv_lines("sample.csv")

        with self.assertRaises(ValueError):
            filter_rows(data, "country", "greater_than", "Canada")


if __name__ == "__main__":
    unittest.main()
