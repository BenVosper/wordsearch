import re

from collections import namedtuple
from functools import partial


WordMatch = namedtuple("WordMatch", ("word", "start", "end"))


def match_is_valid(match, field_width):
    """Determine whether an re.Match object represents a valid WordMatch."""
    start, end = match.span()
    return (start // field_width) == ((end - 1) // field_width)


def find_standard(word, field):
    """Find any left-to-right oriented occurrences of 'word' in 'field'."""
    _, width = field.shape
    flat_field = "".join(field.flat)
    is_valid = partial(match_is_valid, field_width=width)
    for match in filter(is_valid, re.finditer(word, flat_field)):
        start, end = match.span()
        end = end - 1  # We want the final index
        start_row, end_row = map(lambda i: i // width, (start, end))
        start_column, end_column = map(lambda i: i % width, (start, end))
        yield WordMatch(
            word=word,
            start=(start_row, start_column),
            end=(end_row, end_column)
        )


def find_reversed(word, field):
    """Find any right-to-left oriented occurrences of 'word' in 'field'."""
    reversed_word = "".join(reversed(word))
    for word_match in find_standard(reversed_word, field):
        yield WordMatch(
            word=word,
            start=word_match.end,
            end=word_match.start
        )


def find_vertical(word, field):
    """Find any top-to-bottom oriented occurrences of 'word' in 'field'."""
    transposed_field = field.T
    for word_match in find_standard(word, transposed_field):
        start_column, start_row = word_match.start
        end_column, end_row = word_match.end
        yield WordMatch(
            word=word,
            start=(start_row, start_column),
            end=(end_row, end_column)
        )


def find_reversed_vertical(word, field):
    """Find any bottom-to-top oriented occurrences of 'word' in 'field'."""
    transposed_field = field.T
    for word_match in find_reversed(word, transposed_field):
        start_column, start_row = word_match.start
        end_column, end_row = word_match.end
        yield WordMatch(
            word=word,
            start=(start_row, start_column),
            end=(end_row, end_column)
        )


FIND_FUNCS = (
    find_standard,
    find_reversed,
    find_vertical,
    find_reversed_vertical
)


def find_all(word, field):
    """Find all occurrences of 'word' in 'field'."""
    for find_func in FIND_FUNCS:
        yield from find_func(word, field)
