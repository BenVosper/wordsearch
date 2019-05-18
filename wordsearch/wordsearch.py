import numpy

from wordsearch.placements import get_placement, placement_is_valid


MAX_PLACEMENT_ATTEMPTS = 10


class WordsearchInitialisationError(Exception):
    pass


class PlacementError(Exception):
    pass


def validate_word_and_field(word, field_width, field_height):
    """Check if 'word' could be placed in field with given dimensions."""
    word_length = len(word)
    if word_length > field_height or word_length > field_width:
        msg = (f"Word: {word} doesn't fit in field with "
               f"width: {field_width} and height: {field_height}")
        raise AssertionError(msg)


def place_word(word, field):
    """Place 'word' into 'field' with a random position and orientation."""
    field_height, field_width = field.shape
    validate_word_and_field(word, field_height, field_width)

    placement_attempts = 0
    valid_placement_found = False
    while not valid_placement_found:
        placement = get_placement(word, field_width, field_height)
        valid_placement_found = placement_is_valid(placement, field)
        placement_attempts += 1
        if placement_attempts >= MAX_PLACEMENT_ATTEMPTS:
            raise PlacementError(f"Cannot place word: {word} in current field.")
    word_coords = numpy.where(placement.astype(bool))
    field[word_coords] = placement[word_coords]
    return field


def fill_field(field, characters):
    """Fill null elements of 'field' with randomly-selected 'characters'."""
    background = numpy.random.choice([*characters], field.shape)
    null_field_coords = numpy.where(~field.astype(bool))
    field[null_field_coords] = background[null_field_coords]
    return field


class Wordsearch:
    """Wrapper for a wordsearch array."""

    DEFAULT_CHARACTERS = "ABCDEFGHIJKLMNOPQRXTUVWXYZ"

    def __init__(self, field):
        self.field = field

        if self.field.ndim != 2:
            msg = "Please provide a 2D array"
            raise WordsearchInitialisationError(msg)

        if not self.field.dtype == "<U1":
            msg = "Please provide an array of dtype U1"
            raise WordsearchInitialisationError(msg)

    @classmethod
    def generate(cls, words, width, height, characters=DEFAULT_CHARACTERS):
        shape = (height, width)
        field = numpy.full(shape, None)
        for word in words:
            place_word(word, field)
        field = fill_field(field, characters)
        return cls(field.astype("U1"))

    def _row_as_string(self, row):
        row_string = "| " + " | ".join(row) + " |"
        return row_string

    def as_string(self):
        """Get a text representation of this wordsearch."""
        height, width = self.field.shape
        row_border = "".join(["|-", "--|-" * (width - 1), "--|"])
        lines = [row_border]
        for row in [self._row_as_string(row) for row in self.field]:
            lines.extend([row, row_border])
        return "\n".join(lines)
