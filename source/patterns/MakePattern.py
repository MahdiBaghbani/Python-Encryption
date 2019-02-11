import os

from lib.WordPatternMaker import make_word_pattern

base = os.path.dirname(__file__)


def make_pattern(input_path: str, output_name: str, title: bool):
    make_word_pattern(input_path, os.path.join(base, output_name), title)
