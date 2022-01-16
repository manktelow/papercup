import datetime
import unittest

from constants import ACCEPTABLE_SPACING
from model.sentence import Sentence
from services import optimize_service


class TestOptimizeService(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime.timedelta(seconds=1, milliseconds=10)
        self.end_time = datetime.timedelta(seconds=1, milliseconds=50)
        self.short_sentence = Sentence(
            "This sentence is short.",
            self.start_time,
            self.end_time,
            4
        )

    def test_merge_short_sentences(self):
        end_time = self.end_time + ACCEPTABLE_SPACING
        merge_sentence = Sentence(
            "This sentence is also short and can be merged with the previous.",
            self.end_time,
            end_time,
            12
        )

        expected = [Sentence(
            f"{self.short_sentence.text} {merge_sentence.text}",
            self.start_time,
            end_time,
            self.short_sentence.length + merge_sentence.length
        )]

        actual = optimize_service.optimize_sentences([self.short_sentence, merge_sentence])

        self._assert_equals(expected, actual)

    def test_dont_merge_when_timing_too_far_apart(self):
        no_merge_sentence = Sentence(
            "This sentence is short but duration is too far away to be merged with previous.",
            self.end_time + ACCEPTABLE_SPACING + datetime.timedelta(milliseconds=10),
            datetime.timedelta(),
            14
        )

        expected = [self.short_sentence, no_merge_sentence]

        actual = optimize_service.optimize_sentences([self.short_sentence, no_merge_sentence])

        self._assert_equals(expected, actual)

    def test_dont_merge_too_long(self):
        long_sentence = Sentence(
            "This sentence is too long to be merged with the previous sentence, even if the duration between the two\
            is an appropriate amount.",
            self.end_time + ACCEPTABLE_SPACING,
            datetime.timedelta(),
            23
        )

        expected = [self.short_sentence, long_sentence]

        actual = optimize_service.optimize_sentences([self.short_sentence, long_sentence])

        self._assert_equals(expected, actual)

    def test_merge_when_orphaned_sentence(self):
        long_sentence = Sentence(
            "This sentence is long, but the next sentence will be merge to prevent \
            there being strange orphans sentences that are too short for optimal performance",
            self.start_time,
            self.end_time,
            25
        )

        orphan_sentence = Sentence(
            "of TTS system",
            self.end_time + ACCEPTABLE_SPACING,
            datetime.timedelta(),
            3
        )

        expected = [Sentence(
            f"{long_sentence.text} {orphan_sentence.text}",
            self.start_time,
            datetime.timedelta(),
            long_sentence.length + orphan_sentence.length
        )]

        actual = optimize_service.optimize_sentences([long_sentence, orphan_sentence])

        self._assert_equals(expected, actual)

    def _assert_equals(self, expected, actual):
        self.assertEqual(len(expected), len(actual))
        self.assertEqual(expected[0].text, actual[0].text)
        self.assertEqual(expected[0].start_time, actual[0].start_time)
        self.assertEqual(expected[0].end_time, actual[0].end_time)
        self.assertEqual(expected[0].length, actual[0].length)