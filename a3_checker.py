import unittest
import checker_generic
import io
import poetry_functions
import poetry_reader
from poetry_constants import (
    POEM_PRONUNCIATION, PRONOUNCING_DICTIONARY, POETRY_FORMS, CLEAN_POEM)
import copy

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

SAMPLE_DICTIONARY_FILE = ''';;; Comment line
ABSINTHE  AE1 B S IH0 N TH
HEART  HH AA1 R T
FONDER  F AA1 N D ER0
'''

SAMPLE_POEM_FILE = '''Is this mic on?
Get off my lawn.
'''

SMALL_PRONOUNCING_DICTIONARY = {
    'HOW': ['HH', 'AW1'],
    'NOW': ['N', 'AW1'],
    'BROWN': ['B', 'R', 'AW1', 'N'],
    'COW': ['C', 'AW1'],
    'CHOWDER': ['CH', 'AW1', 'D', 'ER0'],
    'SHOW': ['SH', 'OW1'],
    'TOWN': ['T', 'AW1', 'N'],
    'TOUT': ['T', 'AW1', 'T'],
    'THEMISTOCLES': ['DH', 'EH1', 'M', 'AH0', 'S', 'T', 'OW1', 'K', 'L', 'IY0',
                     'Z'],
    'THERMOPYLAE': ['TH', 'ER2', 'M', 'AA1', 'P', 'IH1', 'L', 'AY1'],
    'THE': ['DH', 'AH0'],
    'PELOPONESSIAN': ['P', 'EH1', 'L', 'OW1', 'P', 'OW1', 'N', 'IY2', 'ZH',
                      'EH1', 'N'],
    'WAR': ['W', 'AO1', 'R'],
    'X': ['IH0', 'K', 'S'],
    'SQUARED': ['S', 'K', 'W', 'EH1', 'R', 'D'],
    'Y': ['W', 'AY1'],
    'WHY': ['W', 'AY1'],
    'H2SO4': ['EY1', 'CH', 'T', 'UW1', 'EH2', 'S', 'OW1', 'F', 'AO1', 'R'],
    'SOFTWOOD': ['S', 'AO1', 'F', 'T', 'W', 'UH2', 'D'],
    'ORBER': ['AO1', 'R', 'B', 'ER0'],
    'ACCELERATING': ['AE0', 'K', 'S', 'EH1', 'L', 'ER0', 'EY2', 'T', 'IH0',
                     'NG'],
    'THINKING': ['TH', 'IH1', 'NG', 'K', 'IH0', 'NG'],
    'SARONG': ['S', 'ER0', 'AO1', 'NG'],
}

SMALL_POETRY_FORMS = {'Haiku': ([5, 7, 5], ['*', '*', '*']),
                      'Limerick': ([8, 8, 5, 5, 8], ['A', 'A', 'B', 'B', 'A'])}


class CheckTest(unittest.TestCase):
    """Sanity checker for assignment functions."""

    def setUp(self):
        super().setUp()
        self.pronouncing_dictionary = copy.deepcopy(
            SMALL_PRONOUNCING_DICTIONARY)
        self.poetry_forms = copy.deepcopy(
            SMALL_POETRY_FORMS)
        self.poetry_form_file = io.StringIO(SAMPLE_POETRY_FORM_FILE)
        self.dictionary_file = io.StringIO(SAMPLE_DICTIONARY_FILE)
        self.poem_file = io.StringIO(SAMPLE_POEM_FILE)

    def test_00_clean_poem(self):
        """Function clean_poem.
        """

        result = poetry_functions.clean_poem(
            SAMPLE_POEM_FILE[:])
        error_message = checker_generic.type_error_message(
            'clean_poem', 'CLEAN_POEM', str(result))
        self._is_clean_poem(result, error_message)

    def test_01_extract_phonemes(self):
        """Function extract_phonemes.
        """

        dictionary = {'YES': ['Y', 'EH1', 'S'], 'NO': ['N', 'OW1']}
        result = poetry_functions.extract_phonemes(
            [['YES'], ['NO', 'YES']], dictionary)
        error_message = checker_generic.type_error_message(
            'extract_phonemes', 'POEM_PRONUNCIATION', str(result))
        self._is_poem_pronunciation(result, error_message)

    def test_02_phonemes_to_str(self):
        """Function phonemes_to_str.
        """

        checker_generic.type_check_simple(
            poetry_functions.phonemes_to_str,
            [['YES'], ['NO', 'YES']], str)

    def test_03_get_rhyme_scheme(self):
        """Function get_rhyme_scheme.
        """

        result = poetry_functions.get_rhyme_scheme(
            [[['IH0', 'N']], [['S', 'IH0', 'N']]])
        error_message = checker_generic.type_error_message(
            'get_rhyme_scheme', 'List[str]', str(result))

        self.assertIsInstance(result, list, error_message)
        for value in result:
            self.assertIsInstance(value, str, error_message)

    def test_04_get_num_syllables(self):
        """Function get_num_syllables.
        """

        result = poetry_functions.get_num_syllables(
            [[['S', 'IH0', 'N']]])
        error_message = checker_generic.type_error_message(
            'get_num_syllables', 'List[int]', str(result))

        self.assertIsInstance(result, list, error_message)
        for value in result:
            self.assertIsInstance(value, int, error_message)

    def test_05_read_and_trim_whitespace(self):
        """Function read_and_trim_whitespace.
        """

        result = poetry_reader.read_and_trim_whitespace(
            self.poem_file)
        self.assertIsInstance(result, str, str(result))

    def test_06_read_pronouncing_dictionary(self):
        """Function read_pronouncing_dictionary.
        """

        result = poetry_reader.read_pronouncing_dictionary(
            self.dictionary_file)

        error_message = checker_generic.type_error_message(
            'read_pronouncing_dictionary',
            'PRONOUNCING_DICTIONARY',
            str(result))
        self._is_pronouncing_dictionary(result, error_message)

    def test_07_read_poetry_form_descriptions(self):
        """Function read_poetry_form_descriptions.
        """

        result = poetry_reader.read_poetry_form_descriptions(
            self.poetry_form_file)

        error_message = checker_generic.type_error_message(
            'read_poetry_form_descriptions',
            'POETRY_FORM',
            str(result))
        self._is_poetry_form_description(result, error_message)

    def _is_clean_poem(self, poem: CLEAN_POEM,
                               error_message: str):
        """Check whether poem is a CLEAN_POEM.
        """

        self.assertIsInstance(poem, list, error_message)
        for line in poem:
            self.assertIsInstance(line, list, error_message)
            for word in line:
                self.assertIsInstance(word, str, error_message)

    def _is_poem_pronunciation(self, poem: POEM_PRONUNCIATION,
                               error_message: str):
        """Check whether poem is a POEM_PRONUNCIATION.
        """

        self.assertIsInstance(poem, list, error_message)
        for line in poem:
            self.assertIsInstance(line, list, error_message)
            for word in line:
                self.assertIsInstance(word, list, error_message)
                for phoneme in word:
                    self.assertIsInstance(phoneme, str, error_message)

    def _is_pronouncing_dictionary(self, dictionary: PRONOUNCING_DICTIONARY,
                                   error_message: str):
        """Check whether dictionary is a PRONOUNCING_DICTIONARY.
        """

        self.assertIsInstance(dictionary, dict, error_message)
        for key, value in dictionary.items():
            self.assertIsInstance(key, str, error_message)
            self.assertIsInstance(value, list, error_message)
            for phoneme in value:
                self.assertIsInstance(phoneme, str, error_message)

    def _is_poetry_form_description(self, dictionary: POETRY_FORMS,
                                   error_message: str):
        """Check whether dictionary is a POETRY_FORMS.
        """

        self.assertIsInstance(dictionary, dict, error_message)
        for key, poetry_form in dictionary.items():
            self.assertIsInstance(key, str, error_message)
            self.assertIsInstance(poetry_form, tuple, error_message)
            self.assertEqual(len(poetry_form), 2, error_message)
            self.assertIsInstance(poetry_form[0], list, error_message)
            for v in poetry_form[0]:
                self.assertIsInstance(v, int)
            self.assertIsInstance(poetry_form[1], list, error_message)
            for v in poetry_form[1]:
                self.assertIsInstance(v, str)


if __name__ == '__main__':
    TARGET_LEN = 79
    print(''.center(TARGET_LEN, "="))
    print(' Start: checking coding style '.center(TARGET_LEN, "="))
    # checker_generic.run_pyta('poetry.py', 'pyta/a3_pyta.txt')
    checker_generic.run_pyta('poetry_reader.py', 'pyta/a3_pyta.txt')
    checker_generic.run_pyta('poetry_functions.py', 'pyta/a3_pyta.txt')
    print(' End checking coding style '.center(TARGET_LEN, "="))

    print(' Start: checking type contracts '.center(TARGET_LEN, "="))
    unittest.main(exit=False)
    print(' End checking type contracts '.center(TARGET_LEN, "="))

    print('\nScroll up to see ALL RESULTS:')
    print('  - checking coding style')
    print('  - checking type contract\n')
