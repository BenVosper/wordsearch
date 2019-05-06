import numpy
import pytest

from unittest.mock import patch

from tests.utils import fix_random_seed
from wordsearch.wordsearch import (
    Wordsearch,
    validate_word_and_field,
    place_word,
    PlacementError,
    MAX_PLACEMENT_ATTEMPTS,
    fill_field
)

get_placement = "wordsearch.wordsearch.get_placement"


def test_validate_word_and_field():
    with pytest.raises(AssertionError):
        validate_word_and_field("12345", 4, 4)


def test_place_word():
    word = "FOO"
    field = numpy.full((5, 5), None)

    placement = field.copy()
    placement[2, :3] = [*word]

    with patch(get_placement, return_value=placement):
        field = place_word(word, field)

    assert "".join(field[2, :3]) == word


def test_place_word_placement_error():
    word = "FOO"
    field = numpy.full((5, 5), "A", object)

    placement = field.copy()
    placement[2, :3] = [*word]

    with patch(get_placement, return_value=placement) as mock_get_placement:
        with pytest.raises(PlacementError):
            place_word(word, field)

    assert mock_get_placement.call_count == MAX_PLACEMENT_ATTEMPTS


def test_fill_field():
    field = numpy.full((5, 5), None)
    field[2, 2] = "X"

    field = fill_field(field, "ABC")

    assert {*field.flat}.issubset({"A", "B", "C", "X"})


@fix_random_seed()
def test_wordsearch():
    wordsearch = Wordsearch(["FOO", "BAR", "BAZ"], 5, 5)

    assert wordsearch.field.tolist() == [
        ["R", "A", "B", "O", "Q"],
        ["F", "Q", "J", "O", "P"],
        ["X", "Q", "M", "F", "C"],
        ["G", "Z", "A", "B", "A"],
        ["J", "L", "Q", "D", "C"]
    ]

    assert wordsearch.as_string() == "\n".join([
        "|---|---|---|---|---|",
        "| R | A | B | O | Q |",
        "|---|---|---|---|---|",
        "| F | Q | J | O | P |",
        "|---|---|---|---|---|",
        "| X | Q | M | F | C |",
        "|---|---|---|---|---|",
        "| G | Z | A | B | A |",
        "|---|---|---|---|---|",
        "| J | L | Q | D | C |",
        "|---|---|---|---|---|"
    ])
