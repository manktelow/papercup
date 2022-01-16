import json
import os
import sys

from services import srt_file_service, json_file_service
from services.optimize_service import optimize_sentences


def main():
    file_name = sys.argv[1:][0]

    try:
        sentences = []
        if file_name.endswith('.json'):
            sentences = json_file_service.get_sentences(file_name)
        elif file_name.endswith('.srt'):
            sentences = srt_file_service.get_sentences(file_name)

        sentences = optimize_sentences(sentences)
        _create_output_file(sentences)

    except FileNotFoundError:
        print(f"file {file_name} not found")


def _create_output_file(sentences: list):
    with open('assets/output.json', 'w') as output_file:
        json.dump([ob.to_json() for ob in sentences], output_file)

        print(f"output is here: {os.getcwd()}/assets/output.json")


if __name__ == '__main__':
    main()
