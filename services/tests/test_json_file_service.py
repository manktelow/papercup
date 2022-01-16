import unittest

# In the interest of time, these test cases are only verifying the function that determines
# if a sentence should be created. Ideally would test the service and not a private function.
from constants import MAX_SENTENCE_LENGTH
from services import json_file_service


class TestJsonFileService(unittest.TestCase):

    def test_create_sentence_full_stop(self):
        actual = json_file_service.should_create_sentence("test.", 21)

        self.assertTrue(actual)

    def test_create_sentence_comma(self):
        actual = json_file_service.should_create_sentence("test,", 21)

        self.assertTrue(actual)

    def test_dont_create_sentence_comma_but_short_length(self):
        actual = json_file_service.should_create_sentence("test,", 11)

        self.assertFalse(actual)

    def test_create_sentence_max_length(self):
        actual = json_file_service.should_create_sentence("test,", MAX_SENTENCE_LENGTH)

        self.assertTrue(actual)
