import unittest

from pipeline.company_panel import company_key, map_panel


class CompanyPanelTests(unittest.TestCase):
    def test_normalizes_known_historical_aliases(self):
        self.assertEqual(company_key("Intel Corporation"), company_key("Intel"))
        self.assertEqual(company_key("Bosch Global Software Technologies"), company_key("Bosch Group"))
        self.assertEqual(company_key("JPMorgan Chase & Co."), company_key("JPMorgan Chase"))

    def test_maps_connected_and_unresolved_historical_companies(self):
        result = map_panel(
            ["Intel Corporation", "Bosch Global Software Technologies", "A Company"],
            [{"company": "Intel"}, {"company": "Bosch Group"}],
        )

        self.assertEqual(result["connected_count"], 2)
        self.assertEqual(result["unresolved_count"], 1)
        self.assertEqual(result["connected"][0]["historical_company"], "Bosch Global Software Technologies")
        self.assertEqual(result["unresolved"], ["A Company"])


if __name__ == "__main__":
    unittest.main()
