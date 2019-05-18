## `wordsearch`  [![CircleCI](https://circleci.com/gh/BenVosper/wordsearch/tree/master.svg?style=shield)](https://circleci.com/gh/BenVosper/wordsearch/tree/master)

Simple wordsearch generator and solver using `numpy` and regex.

### Installation

```
git clone git@github.com:BenVosper/wordsearch.git
cd wordsearch
pip install .
```

This will also install `numpy` if you don't have it in your current environment.

### Usage

#### Wordsearch generation

```python
from wordsearch.wordsearch import Wordsearch

my_wordsearch = Wordsearch.generate(
    words=["HIDE", "THESE", "WORDS", "FOR", "ME"],
    width=10,
    height=8
)

print(my_wordsearch.as_string())
```

If you encounter a `PlacementError`, try using fewer words or larger dimensions.

By default, your words will be hidden in a field of randomly-selected upper-case letters. To change the characters used for the field, use the `characters` kwarg.

The raw character-array of your wordsearch can be accessed via `Wordsearch.field`.

###### Example output

```
|---|---|---|---|---|---|---|---|---|---|
| U | G | E | N | E | R | A | T | O | R |
|---|---|---|---|---|---|---|---|---|---|
| I | I | N | W | O | K | N | G | V | G |
|---|---|---|---|---|---|---|---|---|---|
| Y | V | N | K | O | E | D | E | V | Z |
|---|---|---|---|---|---|---|---|---|---|
| N | W | O | H | U | X | H | V | O | C |
|---|---|---|---|---|---|---|---|---|---|
| E | T | N | E | B | I | A | E | S | J |
|---|---|---|---|---|---|---|---|---|---|
| V | N | O | R | X | R | I | Q | P | N |
|---|---|---|---|---|---|---|---|---|---|
| N | F | T | U | Q | D | H | Y | E | J |
|---|---|---|---|---|---|---|---|---|---|
| K | L | F | L | Y | E | R | Y | R | X |
|---|---|---|---|---|---|---|---|---|---|
| N | W | O | L | W | N | Y | C | O | B |
|---|---|---|---|---|---|---|---|---|---|
| H | C | R | A | E | S | D | R | O | W |
|---|---|---|---|---|---|---|---|---|---|
```


#### Wordsearch solving

```python
from numpy import array

from wordsearch.wordsearch import Wordsearch

field = array(
    [
        ["C", "H", "Y", "K", "A", "M", "H", "I"],
        ["R", "E", "V", "E", "N", "I", "I", "W"],
        ["L", "X", "B", "O", "K", "E", "D", "B"],
        ["L", "L", "U", "O", "Y", "N", "D", "J"],
        ["V", "F", "I", "N", "D", "K", "E", "E"],
        ["C", "Y", "T", "I", "I", "A", "N", "M"],
        ["L", "K", "E", "M", "C", "Q", "B", "W"],
        ["B", "D", "U", "F", "B", "D", "M", "G"]
    ], 
    dtype="U1"
)
my_wordsearch = Wordsearch(field)

solutions = my_wordsearch.solve(
    ["IM", "HIDDEN", "YOULL", "NEVER", "FIND", "ME"],
)

print(solutions)
```
Instantiate a wordsearch object with the field you'd like to search.

Provided fields must be 2-dimensional arrays of dtype "U1".

Calling the `solve` method with target words provides you with a list of zero or more `WordMatch` objects. Each `WordMatch` is a `namedtuple` containing the found word as well as its position in the field. 

###### Example output
```python
[
    WordMatch(word="IM",     start=(5, 3), end=(6, 3)),
    WordMatch(word="IM",     start=(1, 5), end=(0, 5)),
    WordMatch(word="HIDDEN", start=(0, 6), end=(5, 6)),
    WordMatch(word="YOULL",  start=(3, 4), end=(3, 0)),
    WordMatch(word="NEVER",  start=(1, 4), end=(1, 0)),
    WordMatch(word="FIND",   start=(4, 1), end=(4, 4)),
    WordMatch(word="ME",     start=(6, 3), end=(6, 2)),
    WordMatch(word="ME",     start=(5, 7), end=(4, 7))
 ]
```
