from constants import MAX_SENTENCE_LENGTH, ACCEPTABLE_SPACING
from model.sentence import Sentence


# used to optimize output from json & srt file services
def optimize_sentences(sentences: list) -> list:
    results = []
    prev_sentence = None

    for sentence in sentences:
        results = _validate_sentence_and_append(results, sentence, prev_sentence)
        prev_sentence = results[-1]

    return results


def _validate_sentence_and_append(results: list, sentence: Sentence, prev: Sentence) -> list:
    if prev and sentence.length < MAX_SENTENCE_LENGTH \
            and _can_merge_sentences(sentence, prev):
        combined = Sentence(
            f"{prev.text} {sentence.text}",
            prev.start_time,
            sentence.end_time,
            sentence.length + prev.length
        )

        results[-1] = combined
    else:
        results.append(sentence)

    return results


# In order to prevent very short sentences if the sentence length is less than 4 assumption is made sentence can
# be combined with the previous as long as the duration is not too far apart
def _can_merge_sentences(sentence: Sentence, prev: Sentence) -> bool:
    combined_length = sentence.length + prev.length
    duration_between = sentence.start_time - prev.end_time

    return (combined_length <= MAX_SENTENCE_LENGTH or sentence.length < 4) \
        and duration_between <= ACCEPTABLE_SPACING
