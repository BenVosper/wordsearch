## `wordsearch`

Simple wordsearch generator using numpy.

#### Usage

```python
from wordsearch.wordsearch import Wordsearch

my_wordsearch = Wordsearch(
    words=["HIDE", "THESE", "WORDS", "FOR", "ME"],
    width=10,
    height=8
)

print(my_wordsearch.as_string())
```

If you encounter a `PlacementError`, try using fewer words or larger dimensions.

By default, your words will be hidden in a field of randomly-selected upper-case letters. To change the characters used for the field, use the `characters` kwarg.

The raw character-array of your wordsearch can be accessed via `Wordsearch.field`.

#### Example output

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
