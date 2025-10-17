import unittest
from location_utils import build_location_data, find_location_info, get_all_cities, ALL_LOCATIONS, CITY_TO_COUNTRY_MAPPING

class TestLocationUtils(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Builds the location data once for all tests in this class.
        """
        build_location_data()

    def test_build_location_data_populates_structures(self):
        """
        Tests if the global data structures are populated after calling build_location_data.
        """
        self.assertTrue(len(ALL_LOCATIONS) > 0, "ALL_LOCATIONS should not be empty.")
        self.assertTrue(len(CITY_TO_COUNTRY_MAPPING) > 0, "CITY_TO_COUNTRY_MAPPING should not be empty.")
        
        # Check a specific example
        self.assertIn("jepang", ALL_LOCATIONS)
        self.assertIn("japan", ALL_LOCATIONS) # an alias
        self.assertIn("tokyo", ALL_LOCATIONS) # a city
        self.assertEqual(CITY_TO_COUNTRY_MAPPING['Asia']['tokyo'], 'jepang')

    def test_get_all_cities(self):
        """
        Tests that get_all_cities returns a list of unique city names.
        """
        cities = get_all_cities()
        self.assertIsInstance(cities, list)
        self.assertIn("tokyo", cities)
        self.assertIn("osaka", cities)
        self.assertIn("london", cities)
        # Test for uniqueness
        self.assertEqual(len(cities), len(set(cities)))

    def test_find_location_info_exact_match(self):
        """
        Tests finding a location with an exact country name, city, and alias.
        """
        # Exact country name
        info, score = find_location_info("jepang")
        self.assertIsNotNone(info)
        self.assertEqual(info['name'], 'KBRI Tokyo')
        self.assertGreaterEqual(score, 90)

        # Exact city name
        info, score = find_location_info("osaka")
        self.assertIsNotNone(info)
        self.assertEqual(info['name'], 'KJRI Osaka')
        self.assertGreaterEqual(score, 90)

        # Exact alias
        info, score = find_location_info("uk")
        self.assertIsNotNone(info)
        self.assertEqual(info['name'], 'KBRI London')
        self.assertGreaterEqual(score, 90)

    def test_find_location_info_fuzzy_match(self):
        """
        Tests finding a location with a slightly misspelled query.
        """
        info, score = find_location_info("jepng") # Misspelled "jepang"
        self.assertIsNotNone(info)
        self.assertEqual(info['name'], 'KBRI Tokyo')
        self.assertGreater(score, 80)

    def test_find_location_info_case_insensitivity(self):
        """
        Tests that the search is case-insensitive.
        """
        info, _ = find_location_info("SINGAPURA")
        self.assertIsNotNone(info)
        self.assertEqual(info['name'], 'KBRI Singapura')
        
        info, _ = find_location_info("sInGaPoRe") # Alias
        self.assertIsNotNone(info)
        self.assertEqual(info['name'], 'KBRI Singapura')

    def test_find_location_info_with_punctuation(self):
        """
        Tests that trailing punctuation is handled correctly.
        """
        info, score = find_location_info("perth?")
        self.assertIsNotNone(info)
        self.assertEqual(info['name'], 'KJRI Perth')
        self.assertGreaterEqual(score, 90)

    def test_find_location_info_no_match(self):
        """
        Tests a query that should not match any location.
        """
        # This will now pass with the corrected find_location_info logic
        info, score = find_location_info("neverland")
        self.assertIsNone(info)
        self.assertEqual(score, 0)

    def test_find_location_info_with_low_score(self):
        """
        Tests a query that might have a low fuzzy score below the threshold.
        """
        info, score = find_location_info("palestine")
        self.assertIsNone(info, "Should not return a result if score is too low")
        self.assertEqual(score, 0)