import numpy
from random import randint


MAX_PLACEMENT_ATTEMPTS = 10

class PlacementError(Exception):
    pass


def get_standard_placement(word, field_width, field_height):
    word_length = len(word)
    placement =  numpy.full((field_height, field_width), None)
    row = randint(0, field_height - 1)
    max_start_column = field_width - word_length
    start_column = randint(0, max_start_column) if max_start_column else 0
    placement[row, start_column:start_column + word_length] = [*word]
    return placement


def get_reversed_placement(word, field_width, field_height):
    reversed_word = "".join(reversed(word))
    return get_standard_placement(reversed_word, field_width, field_height)

def get_vertical_placement(word, field_width, field_height):
    word_length = len(word)
    placement = numpy.full((field_height, field_width), None)
    column = randint(0, field_width - 1)
    max_start_row = field_height - word_length
    start_row = randint(0, max_start_row) if max_start_row else 0
    placement[start_row:start_row + word_length, column] = [*word]
    return placement

def get_reversed_vertical_placement(word, field_width, field_height):
    reversed_word = "".join(reversed(word))
    return get_vertical_placement(reversed_word, field_width, field_height)


PLACEMENT_FUNCTIONS = [
    get_standard_placement,
    get_reversed_placement,
    get_vertical_placement,
    get_reversed_vertical_placement
]
NUM_PLACEMENT_FUNCTIONS = len(PLACEMENT_FUNCTIONS)

def get_placement(word, field_width, field_height):
    placement_function = PLACEMENT_FUNCTIONS[randint(0, NUM_PLACEMENT_FUNCTIONS - 1)]
    return placement_function(word, field_width, field_height)

def placement_is_valid(placement, field):
    placement_bool = placement.astype(bool)
    field_bool = field.astype(bool)
    overlaps = placement_bool & field_bool
    allowed_overlaps = placement == field
    return allowed_overlaps[numpy.where(overlaps)].all()

def validate_word_and_field(word, field_width, field_height):
    word_length = len(word)
    if word_length > field_height or word_length > field_width:
        msg = (f"Word: {word} doesn't fit in field with "
               f"width: {field_width} and height: {field_height}")
        raise AssertionError(msg)


def place_word(word, field):
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
    background = numpy.random.choice([*characters], field.shape)
    null_field_coords = numpy.where(~field.astype(bool))
    field[null_field_coords] = background[null_field_coords]
    return field



class Wordsearch:

    DEFAULT_CHARACTERS = "ABCDEFGHIJKLMNOPQRXTUVWXYZ"

    def __init__(self, words, width, height, characters=DEFAULT_CHARACTERS):
        self.words = words
        self.width = width
        self.height = height
        self.shape = (height, width)
        self.characters = characters

        # TODO: Check word chars are subset of background characters
        # TODO: Check longest word can fit in grid

        self.field = numpy.full(self.shape, None)
        for word in self.words:
            place_word(word, self.field)
        fill_field(self.field, self.characters)

    def _row_as_string(self, row):
        row_string = "| " + " | ".join(row) + " |"
        return row_string

    def as_string(self):
        row_border = "".join(["|-", "--|-" * (self.width - 1), "--|"])
        lines = [row_border]
        for row in [self._row_as_string(row) for row in self.field]:
            lines.extend([row, row_border])
        return "\n".join(lines)


w = Wordsearch(["foo", "bar"], 10, 10)
print(w.as_string())

