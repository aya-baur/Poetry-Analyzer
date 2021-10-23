"""Helper functions for the poetry.py program.
"""

from typing import List
from typing import Tuple
from typing import Dict

from poetry_constants import (
    CLEAN_POEM, WORD_PHONEMES, LINE_PRONUNCIATION, POEM_PRONUNCIATION,
    PRONOUNCING_DICTIONARY)


# ===================== Helper Functions =====================


def clean_word(s: str) -> str:
    """Return a new string based on s in which all letters have been converted
    to uppercase and whitespace and punctuation characters have been stripped
    from both ends. Inner punctuation and whitespace is left untouched.

    >>> clean_word('Birthday!!!')
    'BIRTHDAY'
    >>> clean_word('  "Quoted?"\\n\\n\\n')
    'QUOTED'
    """

    punctuation = """!"'`@$%^&_-+={}|\\/,;:.-?)([]<>*#\n\t\r """
    result = s.upper().strip(punctuation)
    return result


def get_word(s: List[str]) -> List[str]:
    ''' Return a list of capitalized words separated from each other, from s
    
    >>> get_word(['The first line leads off'])
    ['THE', 'FIRST', 'LINE', 'LEADS', 'OFF']
    '''
        
    s1 = ', '.join(s)
    
    word = ''
    result = []
    for char in s1:
        if char != ' ':
            word += char
        else:
            result.append(word)
            word = ''
    
    if word != ' ':
        result.append(word)
    
    result1 = []
    for word in result:
        if word != '':
            result1.append(clean_word(word))
    return result1

# we have to keep in word punctuation like Don't !!!!!!!!!!!!!!
#are these types of words going to be given in a correct format?

def clean_poem(raw_poem: str) -> CLEAN_POEM:
    """Return the non-blank, non-empty lines of poem, with whitespace removed
    from the beginning and end of each line and all words capitalized.

    >>> clean_poem('The first line leads off,\n\n\nWith a gap before the next.\n    Then the poem ends.\n')
    [['THE', 'FIRST', 'LINE', 'LEADS', 'OFF'], ['WITH', 'A', 'GAP', 'BEFORE', 'THE', 'NEXT'], ['THEN', 'THE', 'POEM', 'ENDS']]
    """
    result = []
    indeces = []
    for i in range(len(raw_poem)):
        if raw_poem[i] == '\n':
            indeces.append(i)
            if len(indeces) == 1:
                result.append([raw_poem[:i]])
            else:
                r = indeces.index(i)
                result.append([raw_poem[indeces[r - 1]:i]])
   
    result1 = []
    for lst in result:
            result1.append(get_word(lst))
    
    result2 = []
    for lst in result1:
        if lst != ['']:
            result2.append(lst)
        
        for char in lst:
            if char == '':
                lst.remove(char)
    
    
    return result2    



def extract_phonemes(
        cleaned_poem: CLEAN_POEM,
        word_to_phonemes: PRONOUNCING_DICTIONARY) -> POEM_PRONUNCIATION:
    """Return a list where each inner list contains the phonemes for the
    corresponding line of cleaned_poem, based on the word_to_phonemes
    pronouncing dictionary.

    >>> word_to_phonemes = {'YES': ['Y', 'EH1', 'S'], 'NO': ['N', 'OW1']}
    >>> extract_phonemes([['YES'], ['NO', 'YES']], word_to_phonemes)
    [[['Y', 'EH1', 'S']], [['N', 'OW1'], ['Y', 'EH1', 'S']]]
    """
    result = []
    final = []
    for line in cleaned_poem:
        for word in line:
            s = word_to_phonemes[word]
            result.append(s)
        final.append(result)
        result = []

    return final

def phonemes_to_str(poem_pronunciation: POEM_PRONUNCIATION) -> str:
    """Return a string containing all the phonemes in each word in each line in
    poem_pronunciation. The phonemes are separated by spaces, the words are
    separated by ' | ', and the lines are separated by '\n'.

    >>> phonemes_to_str([[['Y', 'EH1', 'S']], [['N', 'OW1'], ['Y', 'EH1', 'S']]])
    'Y EH1 S\\nN OW1 | Y EH1 S'
    
    >>> phonemes_to_str([[['IH0', 'N']], [['S', 'IH0', 'N']]])
    'IH0 N\\nS IH0 N'
    
    >>> phonemes_to_str([[['Y', 'OW1'], ['Y', 'AE1', 'N']], [['EY1', 'B']]]) 
    'Y OW1 | Y AE1 N\\nEY1 B'
    
    
    """
    result = ''
    
    for line in poem_pronunciation:
        for word in line:
            one_word = ''
            for char in word:
                if char != "'" and word[-1] != char:
                    one_word += char + ' '
                elif word[-1] == char:
                    one_word += char
            if line[-1] != word:
                result += one_word + ' | '
            else:
                result += one_word
        if poem_pronunciation[-1] != line:
            result += '\n'
    return result    


def last_syllables(poem_pronunciation: POEM_PRONUNCIATION) -> List[List[str]]:
    '''Return a list of last syllables of each word in poem_pronounciation
    
    >>> last_syllables([[['IH0', 'N']], [['S', 'IH0', 'N']]])
    [['IH0', 'N'], ['IH0', 'N']]
    
    >>> last_syllables([[['Y', 'EH1', 'S']], [['N', 'OW1'], ['F', 'IH0', 'N', 'EH1', 'S']]])
    [['EH1', 'S'], ['OW1'], ['EH1', 'S']]
    '''   
    last_syll = [] 
    
    for line in poem_pronunciation:
        for word in line:
            vowel = []
            for char in word:
                if not char.isalpha():
                    vowel.append(char)
        
            s = word.index(vowel[-1]) 
            last_syll.append(word[s:])
           
    return last_syll

def get_rhyme_scheme(poem_pronunciation: POEM_PRONUNCIATION) -> List[str]:
    """Return a list of last syllables from the poem described by
    poem_pronunction.

    Precondition: poem_pronunciation is not empty and each PHONEMES list
    contains at least one vowel phoneme.

    >>> get_rhyme_scheme([[['IH0', 'N']], [['S', 'IH0', 'N']]])
    ['A', 'A']
    
    >>> get_rhyme_scheme([[['Y', 'EH1', 'S']], [['N', 'OW1'], ['F', 'IH0', 'N', 'EH1', 'S']]])
    ['A', 'A']
    
    >>> get_rhyme_scheme([[['IH0', 'N']], [['P', 'L', 'EY1']], [['S', 'IH0', 'N']], [['EH1', 'N', 'IY0', 'W', 'EY2']]])
    ['A', 'B', 'A', 'B']
    
    >>> get_rhyme_scheme([[['IH0', 'N']], [['P', 'L', 'EY1']]])
    ['*', '*']
    """
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' 
    
    last_word = []
    for line in poem_pronunciation:
        last_word.append([line[-1]])
    
    s = last_syllables(last_word)
    
    scheme = []
    i = 0
    syllable_to_letter = {}
    for lst in s:    
        lst = str(lst)
        # below loop removes the stress
        lst1 = ''
        for char in lst:
            if char.isalpha():
                lst1 += char
        
        if lst1 in syllable_to_letter:
            scheme.append(syllable_to_letter[lst1])
        else:
            syllable_to_letter[lst1] = alphabet[i]
            scheme.append(alphabet[i])
            i += 1
            
    scheme = check_rhymes(scheme)
    return scheme

def check_rhymes(scheme: List[str]) -> List[str]:
    ''' Check if there are rhymes in scheme, if no replace letters with *
    

    >>> check_rhymes(['A', 'B', 'C'])
    ['*', '*', '*']
    '''
    num = 0
    for lst in scheme:
        num += scheme.count(lst)
    for i in range(num):
        if num == len(scheme):
            scheme[i] = '*'
        
    return scheme    


def get_num_syllables(poem_pronunciation: POEM_PRONUNCIATION) -> List[int]:
    """Return a list of the number of syllables in each poem_pronunciation
    line.
    
    >>> get_num_syllables([[['IH0', 'N']], [['S', 'IH0', 'N']]])
    [1, 1]
    
    >>> get_num_syllables([[['Y', 'EH1', 'S']], [['N', 'OW1'], ['F', 'IH0', 'N', 'EH1', 'S']]])
    [1, 3]
    """
    num_syllables = [] 
    
    for line in poem_pronunciation:
        line_syllables = 0
        for word in line:
            for char in word:
                if not char.isalpha():
                    line_syllables += 1
        num_syllables.append(line_syllables)
                
            
    
    return num_syllables



if __name__ == '__main__':
    import doctest

    doctest.testmod()