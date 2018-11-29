import os

from lib.WordPatternMaker import make_word_pattern

base = os.path.abspath(__file__)


def make_pattern(input_path: str, output_name: str):
    make_word_pattern(input_path, os.path.join(base, output_name))
