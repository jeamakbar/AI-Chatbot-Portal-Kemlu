import unittest
import re
from constants import (
    ADDRESS_KEYWORDS_PATTERN, GREETING_PATTERN, LOST_DOCUMENT_PATTERN,
    KEYWORDS_ID, KEYWORDS_EN, STATIC_FALLBACKS, LLM_SYSTEM_PROMPTS,
    PERWAKILAN_DATA
)

class TestConstants(unittest.TestCase):

    def test_regex_patterns_are_valid(self):
        """
        Tests that all defined regex patterns compile successfully.
        """
        try:
            re.compile(ADDRESS_KEYWORDS_PATTERN)
            re.compile(GREETING_PATTERN)
            re.compile(LOST_DOCUMENT_PATTERN)
        except re.error as e:
            self.fail(f"Regex compilation failed: {e}")

    def test_address_keywords_pattern_matching(self):
        """
        Tests the ADDRESS_KEYWORDS_PATTERN against various valid and invalid strings.
        """
        valid_queries = [
            "di mana alamat kbri di jepang?",
            "lokasi kedutaan untuk singapura",
            "where is the embassy in the united kingdom"
        ]
        invalid_queries = [
            "apa itu kbri?",
            "di mana saya bisa makan?",
            "alamat rumah saya"
        ]

        for query in valid_queries:
            self.assertIsNotNone(re.search(ADDRESS_KEYWORDS_PATTERN, query, re.IGNORECASE), f"Pattern should match: '{query}'")
        
        for query in invalid_queries:
            self.assertIsNone(re.search(ADDRESS_KEYWORDS_PATTERN, query, re.IGNORECASE), f"Pattern should not match: '{query}'")

        # Test capturing group
        match = re.search(ADDRESS_KEYWORDS_PATTERN, "alamat konsulat di jerman", re.IGNORECASE)
        self.assertIsNotNone(match)
        self.assertEqual(match.groups()[-1].strip(), "jerman")

    def test_greeting_pattern_matching(self):
        """
        Tests the GREETING_PATTERN for matching greetings correctly.
        """
        self.assertIsNotNone(re.search(GREETING_PATTERN, "halo", re.IGNORECASE))
        self.assertIsNotNone(re.search(GREETING_PATTERN, "  selamat pagi  ", re.IGNORECASE))
        self.assertIsNone(re.search(GREETING_PATTERN, "halo, ada yang bisa dibantu?", re.IGNORECASE))

    def test_keyword_data_structure(self):
        """
        Ensures that all items in KEYWORDS_ID and KEYWORDS_EN have the required keys.
        """
        required_keys = {"pattern", "priority", "context", "answer", "follow_up"}
        all_keywords = KEYWORDS_ID + KEYWORDS_EN

        for item in all_keywords:
            self.assertTrue(required_keys.issubset(item.keys()), f"Item missing keys: {item}")
            self.assertIsInstance(item['priority'], int)
            self.assertIsInstance(item['follow_up'], list)
            # Ensure pattern is a valid regex
            try:
                re.compile(item['pattern'])
            except re.error:
                self.fail(f"Invalid regex pattern in keywords: {item['pattern']}")

    def test_fallback_and_prompt_languages(self):
        """
        Checks that centralized messages have both 'id' and 'en' keys.
        """
        self.assertIn("id", STATIC_FALLBACKS)
        self.assertIn("en", STATIC_FALLBACKS)
        self.assertIn("id", LLM_SYSTEM_PROMPTS)
        self.assertIn("en", LLM_SYSTEM_PROMPTS)

    def test_perwakilan_data_structure(self):
        """
        Verifies the nested structure of the PERWAKILAN_DATA dictionary.
        """
        self.assertIsInstance(PERWAKILAN_DATA, dict)
        required_keys = {"name", "link", "address", "telepon"} # Check for a sample of required keys

        for continent, countries in PERWAKILAN_DATA.items():
            self.assertIsInstance(countries, dict, f"Continent '{continent}' should be a dict.")
            for country_key, details in countries.items():
                self.assertIsInstance(details, dict, f"Country '{country_key}' should be a dict.")
                self.assertTrue(required_keys.issubset(details.keys()), f"Missing keys in '{country_key}' details.")

if __name__ == '__main__':
    unittest.main()