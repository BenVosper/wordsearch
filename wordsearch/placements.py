import numpy

from numpy.random import randint, choice


def get_standard_placement(word, field_width, field_height):
    word_length = len(word)
    placement = numpy.full((field_height, field_width), None)
    row = randint(0, field_height - 1)
    max_start_column = field_width - word_length
    start_column = randint(0, max_start_column) if max_start_column else 0
    placement[row, start_column:start_column + word_length] = [*word]
    return placement


def get_reversed_placement(word, field_width, field_height):
    reversed_word = "".join(reversed(word))
    return get_standard_placement(reversed_word, field_width, field_height)


def get_vertical_placement(word, field_width, field_height):
    placement = get_standard_placement(word, field_height, field_width)
    return placement.T


def get_reversed_vertical_placement(word, field_width, field_height):
    placement = get_reversed_placement(word, field_height, field_width)
    return placement.T


PLACEMENT_FUNCTIONS = [
    get_standard_placement,
    get_reversed_placement,
    get_vertical_placement,
    get_reversed_vertical_placement
]


def get_placement(word, field_width, field_height):
    placement_function = choice(PLACEMENT_FUNCTIONS)
    return placement_function(word, field_width, field_height)


def placement_is_valid(placement, field):
    placement_bool = placement.astype(bool)
    field_bool = field.astype(bool)
    overlaps = placement_bool & field_bool
    allowed_overlaps = placement == field
    return allowed_overlaps[numpy.where(overlaps)].all()
