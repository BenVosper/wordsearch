from wordsearch.wordsearch import Wordsearch

from tests.utils import fix_random_seed


@fix_random_seed()
def test_wordsearch():
    wordsearch = Wordsearch(["FOO", "BAR", "BAZ"], 5, 5)

    assert wordsearch.field.tolist() == [
        ['R', 'A', 'B', 'O', 'Q'],
        ['F', 'Q', 'J', 'O', 'P'],
        ['X', 'Q', 'M', 'F', 'C'],
        ['G', 'Z', 'A', 'B', 'A'],
        ['J', 'L', 'Q', 'D', 'C']
    ]
