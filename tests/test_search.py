import numpy
import pytest

from unittest.mock import Mock, patch

from wordsearch.search import (
    WordMatch,
    match_is_valid,
    find_standard,
    find_reversed,
    find_vertical,
    find_reversed_vertical,
    find_all
)


# Field width = 3
valid_match_test_cases = (
    ((0, 2), True),   # First row
    ((1, 2), True),   # First row
    ((3, 4), True),   # Second row
    ((1, 4), False),  # Spans first and second row. Reject!
)


@pytest.mark.parametrize(("span", "is_valid"), valid_match_test_cases)
def test_valid_match(span, is_valid):
    match = Mock(span=Mock(return_value=span))

    assert match_is_valid(match, 3) == is_valid


# Word = "FOO"
find_standard_test_cases = (
    (
        numpy.array(
            [
                ["A", "F", "A"],
                ["F", "O", "O"],
                ["A", "O", "A"]
            ],
            dtype="U1"
        ),
        (
            WordMatch(word="FOO", start=(1, 0), end=(1, 2)),
        )
    ),
    (
        numpy.array(
            [
                ["A", "F", "A"],
                ["F", "O", "O"],
                ["F", "O", "O"]
            ],
            dtype="U1"
        ),
        (
            WordMatch(word="FOO", start=(1, 0), end=(1, 2)),
            WordMatch(word="FOO", start=(2, 0), end=(2, 2))
        )
    ),
    (
        numpy.array(
            [
                ["A", "F", "A"],
                ["A", "O", "A"],
                ["A", "O", "A"]
            ],
            dtype="U1"
        ),
        ()
    )
)


@pytest.mark.parametrize(("field", "expected_matches"), find_standard_test_cases)
def test_find_standard(field, expected_matches):
    matches = [*find_standard("FOO", field)]

    assert len(matches) == len(expected_matches)

    for match, expected_match in zip(matches, expected_matches):
        assert match == expected_match


# Word = "BAR"
find_reversed_test_cases = (
    (
        numpy.array(
            [
                ["A", "A", "A"],
                ["R", "A", "B"],
                ["A", "A", "A"]
            ],
            dtype="U1"
        ),
        (
            WordMatch(word="BAR", start=(1, 2), end=(1, 0)),
        )
    ),
    (
        numpy.array(
            [
                ["A", "A", "A"],
                ["R", "A", "B"],
                ["R", "A", "B"]
            ],
            dtype="U1"
        ),
        (
            WordMatch(word="BAR", start=(1, 2), end=(1, 0)),
            WordMatch(word="BAR", start=(2, 2), end=(2, 0))
        )
    ),
    (
        numpy.array(
            [
                ["A", "A", "A"],
                ["A", "A", "A"],
                ["A", "A", "A"]
            ],
            dtype="U1"
        ),
        ()
    )
)


@pytest.mark.parametrize(("field", "expected_matches"), find_reversed_test_cases)
def test_find_reversed(field, expected_matches):
    matches = [*find_reversed("BAR", field)]

    assert len(matches) == len(expected_matches)

    for match, expected_match in zip(matches, expected_matches):
        assert match == expected_match


# Word = "JIM"
find_vertical_test_cases = (
    (
        numpy.array(
            [
                ["A", "J", "A"],
                ["R", "I", "B"],
                ["A", "M", "A"]
            ],
            dtype="U1"
        ),
        (
            WordMatch(word="JIM", start=(0, 1), end=(2, 1)),
        )
    ),
    (
        numpy.array(
            [
                ["J", "A", "J"],
                ["I", "A", "I"],
                ["M", "A", "M"]
            ],
            dtype="U1"
        ),
        (
            WordMatch(word="JIM", start=(0, 0), end=(2, 0)),
            WordMatch(word="JIM", start=(0, 2), end=(2, 2))
        )
    ),
    (
        numpy.array(
            [
                ["M", "A", "A"],
                ["I", "A", "A"],
                ["J", "A", "A"]
            ],
            dtype="U1"
        ),
        ()
    )
)


@pytest.mark.parametrize(("field", "expected_matches"), find_vertical_test_cases)
def test_find_vertical(field, expected_matches):
    matches = [*find_vertical("JIM", field)]

    assert len(matches) == len(expected_matches)

    for match, expected_match in zip(matches, expected_matches):
        assert match == expected_match


# Word = "BZZ"
find_reversed_vertical_test_cases = (
    (
        numpy.array(
            [
                ["Z", "J", "A"],
                ["Z", "I", "B"],
                ["B", "M", "A"]
            ],
            dtype="U1"
        ),
        (
            WordMatch(word="BZZ", start=(2, 0), end=(0, 0)),
        )
    ),
    (
        numpy.array(
            [
                ["Z", "Z", "J"],
                ["Z", "Z", "I"],
                ["B", "B", "M"]
            ],
            dtype="U1"
        ),
        (
            WordMatch(word="BZZ", start=(2, 0), end=(0, 0)),
            WordMatch(word="BZZ", start=(2, 1), end=(0, 1))
        )
    ),
    (
        numpy.array(
            [
                ["M", "B", "B"],
                ["I", "Z", "A"],
                ["J", "Z", "Z"]
            ],
            dtype="U1"
        ),
        ()
    )
)


@pytest.mark.parametrize(("field", "expected_matches"), find_reversed_vertical_test_cases)
def test_find_reversed_vertical(field, expected_matches):
    matches = [*find_reversed_vertical("BZZ", field)]

    assert len(matches) == len(expected_matches)

    for match, expected_match in zip(matches, expected_matches):
        assert match == expected_match


def test_find_all():
    word = "BLAH"
    field = numpy.ones((1, 1))

    mock_find_func = Mock(return_value=(match for match in ()))
    with patch("wordsearch.search.FIND_FUNCS", (mock_find_func,)):
        matches = [*find_all(word, field)]

    assert mock_find_func.called_once_with(word, field)
    assert len(matches) == 0
