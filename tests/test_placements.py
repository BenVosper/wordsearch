import numpy
import pytest

from unittest.mock import patch

from wordsearch.placements import (
    get_standard_placement,
    get_reversed_placement,
    get_vertical_placement,
    get_reversed_vertical_placement,
    get_placement,
    placement_is_valid
)

randint = "wordsearch.placements.randint"
standard_placement = "wordsearch.placements.get_standard_placement"
reversed_placement = "wordsearch.placements.get_reversed_placement"


@pytest.mark.parametrize("word", ["1", "TU", "TRE", "FOUR", "FIIVE"])
def test_standard_placement(word):
    with patch(randint, side_effect=[2, 0]):
        placement = get_standard_placement(word, 5, 5)

    assert "".join(placement[2, :len(word)]) == word


def test_reversed_placement():
    word = "FOO"

    with patch(standard_placement) as mock_standard_placement:
        get_reversed_placement(word, 5, 5)

    assert mock_standard_placement.call_args[0] == ("OOF", 5, 5)


def test_vertical_placement():
    word = "FOO"

    with patch(standard_placement) as mock_standard_placement:
        placement = get_vertical_placement(word, 5, 5)

    assert mock_standard_placement.call_args[0] == (word, 5, 5)
    assert placement == mock_standard_placement.return_value.T


def test_reversed_vertical_placement():
    word = "FOO"

    with patch(reversed_placement) as mock_reversed_placement:
        placement = get_reversed_vertical_placement(word, 5, 5)

    assert mock_reversed_placement.call_args[0] == ("FOO", 5, 5)
    assert placement == mock_reversed_placement.return_value.T


def test_get_placement():
    placement = get_placement("FOO", 5, 5)

    assert {*placement.flat} == {None, "F", "O"}


def test_placement_is_valid():
    assert placement_is_valid(
        numpy.array([None, "F", "O", "O", None]),
        numpy.array([None, None, None, None, None]),
    )

    assert placement_is_valid(
        numpy.array([None, "F", "O", "O", None]),
        numpy.array([None, None, "O", "O", None]),
    )

    assert not placement_is_valid(
        numpy.array([None, "F", "O", "O", None]),
        numpy.array([None, None, "F", "O", "O"]),
    )

    assert not placement_is_valid(
        numpy.array([None, "F", "O", "O", None]),
        numpy.array(["A", "A", "A", "A", "A"], object),
    )

    assert placement_is_valid(
        numpy.array([None, None, None, None, None]),
        numpy.array([None, None, None, None, None]),
    )
