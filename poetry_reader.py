"""Functions for reading the pronouncing dictionary and the poetry forms files
"""
from typing import TextIO

from poetry_constants import (
    # CLEAN_POEM, WORD_PHONEMES, LINE_PRONUNCIATION, POEM_PRONUNCIATION,
    PRONOUNCING_DICTIONARY, POETRY_FORM, POETRY_FORMS)

SAMPLE_POETRY_FORM_FILE = '''Limerick
8 A
8 A
5 B
5 B
8 A

Haiku
5 *
7 * 
5 *
'''
EXPECTED_POETRY_FORMS = {
    'Haiku': ([5, 7, 5], ['*', '*', '*']),
    'Limerick': ([8, 8, 5, 5, 8], ['A', 'A', 'B', 'B', 'A'])
}

SAMPLE_DICTIONARY_FILE = ''';;; Comment line
ABSINTHE  AE1 B S IH0 N TH
HEART  HH AA1 R T
FONDER  F AA1 N D ER0
'''

EXPECTED_DICTIONARY = {
    'ABSINTHE': ['AE1', 'B', 'S', 'IH0', 'N', 'TH'],
    'HEART': ['HH', 'AA1', 'R', 'T', ],
    'FONDER': ['F', 'AA1', 'N', 'D', 'ER0']
}

SAMPLE_POEM_FILE = '''  Is this mic on?

Get off my lawn.
'''


def read_and_trim_whitespace(poem_file: TextIO) -> str:
    """Return a string containing the poem in poem_file, with
     blank lines and leading and trailing whitespace removed.

    >>> import io
    >>> poem_file = io.StringIO(SAMPLE_POEM_FILE)
    >>> read_and_trim_whitespace(poem_file)
    'Is this mic on?\\nGet off my lawn.'
    """
    result = ''
    for line in poem_file:
        result += line.strip()
        if line != '\n':
            result += '\n'
    result = result[:-1]
    return result


def read_pronouncing_dictionary(
        pronunciation_file: TextIO) -> PRONOUNCING_DICTIONARY:
    """Read pronunciation_file, which is in the format of the CMU Pronouncing
    Dictionary, and return the pronunciation dictionary.

    >>> import io
    >>> dict_file = io.StringIO(SAMPLE_DICTIONARY_FILE)
    >>> result = read_pronouncing_dictionary(dict_file)
    >>> result == EXPECTED_DICTIONARY
    True
    """
    words_to_phoneme = {}
    
    for line in pronunciation_file:
        words = []
        if not line.startswith(';'):
            word = ''
            for char in line:
                if char not in ' \n':
                    word += char
                elif char == ' ' and word != '':
                    words.append(word)
                    word = ''
            words.append(word)    
        
        if words != []:
            words_to_phoneme[words[0]] = words[1:]
    return words_to_phoneme


def read_poetry_form_descriptions(
        poetry_forms_file: TextIO) -> POETRY_FORMS:
    """Return a dictionary of poetry form name to poetry pattern for the poetry
    forms in poetry_forms_file.

    >>> import io
    >>> form_file = io.StringIO(SAMPLE_POETRY_FORM_FILE)
    >>> result = read_poetry_form_descriptions(form_file)
    >>> result == EXPECTED_POETRY_FORMS
    True
    """
    result = {}
    nums = []
    scheme = []
    
    key = ''
    for line in poetry_forms_file:
        if line[:-1].isalpha() and key == '':
            key = line[:-1]
           
        elif not line[:-1].isalpha():
            for char in line:
                if char.isnumeric():
                    nums.append(int(char))
                elif char.isalpha() or char == '*':
                    scheme.append(char)   
        elif key != '':
            result[key] = nums, scheme
            key = line[:-1]
            nums = []
            scheme = []   
    result[key] = nums, scheme

    return result

if __name__ == '__main__':
    import doctest

    doctest.testmod()