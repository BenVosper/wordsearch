import numpy

from numpy.random import randint, choice


def get_standard_placement(word, field_width, field_height):
    """Get a traditional, left-right, reading word placement."""
    word_length = len(word)
    placement = numpy.full((field_height, field_width), None)
    row = randint(0, field_height - 1)
    max_start_column = field_width - word_length
    start_column = randint(0, max_start_column) if max_start_column else 0
    placement[row, start_column:start_column + word_length] = [*word]
    return placement


def get_reversed_placement(word, field_width, field_height):
    """Get a horizontal placement, but with word reading from right-left."""
    reversed_word = "".join(reversed(word))
    return get_standard_placement(reversed_word, field_width, field_height)


def get_vertical_placement(word, field_width, field_height):
    """Get a placement with word reading vertically."""
    placement = get_standard_placement(word, field_height, field_width)
    return placement.T


def get_reversed_vertical_placement(word, field_width, field_height):
    """Get a placement with word reading vertically, from bottom-top."""
    placement = get_reversed_placement(word, field_height, field_width)
    return placement.T


PLACEMENT_FUNCTIONS = [
    get_standard_placement,
    get_reversed_placement,
    get_vertical_placement,
    get_reversed_vertical_placement
]


def get_placement(word, field_width, field_height):
    """Get a randomly-chosen placement for given 'word'."""
    placement_function = choice(PLACEMENT_FUNCTIONS)
    return placement_function(word, field_width, field_height)


def placement_is_valid(placement, field):
    """Check if given 'placement' is compatible with 'field'.

    A placement is compatible if:
        - All non-null elements overlap with null-elements of field
    OR
        - Any non-null elements match their corresponding element in the field.

    NB. A placement will be valid if the word it contains exists in exactly
    the same location in the field.
    """
    placement_bool = placement.astype(bool)
    field_bool = field.astype(bool)
    overlaps = placement_bool & field_bool
    allowed_overlaps = placement == field
    return allowed_overlaps[numpy.where(overlaps)].all()
