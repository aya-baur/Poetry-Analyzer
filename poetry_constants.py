"""
A list of type definitions used in the Poetry Checker.
"""

from typing import List
from typing import Tuple
from typing import Dict

"""
A poetry pattern: a two-item tuple of (List[int], List[str])
  - first item is a list of the number of syllables required in each line
  - second item is a list describing the rhyme scheme rule for each line
  - the two items are parallel lists

For example, a limerick has this poetry form:
([8, 8, 5, 5, 8], ['A', 'A', 'B', 'B', 'A'])
"""
POETRY_FORM = Tuple[List[int], List[str]]

"""
Poetry patterns
  - The keys are poetry form names
  - The values are decriptions of the poetry forms

Here is an example:
{'Haiku': ([5, 7, 5], ['*', '*', '*']),
 'Limerick': ([8, 8, 5, 5, 8], ['A', 'A', 'B', 'B', 'A'])}
"""
POETRY_FORMS = Dict[str, POETRY_FORM]

"""
A poem: a list of lines in a poem where empty lines and whitespace-only lines
are removed and leading/trailing space is not included, and all words are
uppercase.

Here is an example:
[['YES'], ['NO', 'YES']]
"""
CLEAN_POEM = List[List[str]]

"""
The pronunciation for a single word or part of a word: the list of phonemes.

For example:
['G', 'UW1', 'F', 'IY0']
"""
WORD_PHONEMES = List[str]

"""
The pronunciation for a line of poetry: a list of word pronunciations.

For example (for "Daniel is goofy"):
[['D', 'AE1', 'N', 'Y', 'AH0', 'L'], ['IH1', 'Z'], ['G', 'UW1', 'F', 'IY0']]
"""
LINE_PRONUNCIATION = List[WORD_PHONEMES]

"""
A poem: a list of lines in a poem, where each line is a list of the word
pronunciations on that line.

For example, for the two lines "Little Jack Horner // Sat in the corner"):
[
[['L', 'IH1', 'T', 'AH0', 'L',], ['JH', 'AE1', 'K',], ['HH', 'AO1', 'R', 'N', 'ER0',]],
[['S', 'AE1', 'T',], ['IH0', 'N',], ['AH0',], ['K', 'AO1', 'R', 'N', 'ER0']]
]
"""
POEM_PRONUNCIATION = List[LINE_PRONUNCIATION]

"""
A pronunciation dictionary: Dict[str, List[str]]
  - each key is a word
  - each value is the list of phonemes for that word's pronunciation

For example, here is a (small) pronunciation dictionary:
{'DANIEL': ['D', 'AE1', 'N', 'Y', 'AH0', 'L'],
 'IS': ['IH1', 'Z'],
 'GOOFY': ['G', 'UW1', 'F', 'IY0']}
"""
PRONOUNCING_DICTIONARY = Dict[str, WORD_PHONEMES]
