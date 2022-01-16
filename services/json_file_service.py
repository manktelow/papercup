import datetime
import json

from constants import MAX_SENTENCE_LENGTH
from model.sentence import Sentence


def get_sentences(file) -> list:
    with open(file) as input_file:
        transcript = json.loads(input_file.read())

    word_list = _extract_words(transcript['results'])
    sentences = []
    text = ""
    start_time = None
    length = 0

    for word in word_list:
        if start_time is None:
            start_time = _format_time(word['startTime'])

        text = f"{text} {word['word']}"
        length += 1

        if should_create_sentence(word['word'], length):
            sentences.append(
                Sentence(
                    text.lstrip(),
                    start_time,
                    _format_time(word['endTime']),
                    length
                )
            )

            text = ""
            start_time = None
            length = 0

    return sentences


# Creates complete sentences - a complete sentence is considered
# - ending with . regardless of length
# - ending with , and length is close to the maximum sentence length
# - length is greater than the max sentence length
# this function should be private - only made public to support limited test cases
def should_create_sentence(word: str, length: int) -> bool:
    return word.endswith('.') \
        or (word.endswith(',') and length > MAX_SENTENCE_LENGTH - 5) \
        or length > MAX_SENTENCE_LENGTH


def _extract_words(transcript: list) -> list:
    words = []

    for result in transcript:
        # assumption made form example input that only one object in alternative array
        words.extend(result['alternatives'][0]['words'])

    return words


# Takes a string and converts to timedelta
# timedelta chosen for consistency with srt module, and for calculating duration
def _format_time(time: str) -> datetime.timedelta:
    split_time = time.split(".")

    if len(split_time) == 1:
        return datetime.timedelta(seconds=float(split_time[0][:-1]))  # remove 's' from string

    return datetime.timedelta(
        seconds=float(split_time[0]),
        milliseconds=float(split_time[1][:-1])  # remove 's' from string
    )