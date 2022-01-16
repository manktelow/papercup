import srt

from model.sentence import Sentence


def get_sentences(file) -> list:
    sentences = []

    with open(file) as input_file:
        # prefer to use a library than re-invent the wheel
        parsed_file = list(srt.parse(input_file))

    for subtitle in parsed_file:
        sentences.append(
            Sentence(
                subtitle.content,
                subtitle.start,
                subtitle.end,
                len(subtitle.content.split(' '))
            )
        )

    return sentences


