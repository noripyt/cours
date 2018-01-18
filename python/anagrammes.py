#!/usr/bin/env python3

from argparse import ArgumentParser, FileType
from collections import defaultdict
from string import punctuation
from unicodedata import normalize

__author__ = 'Bertrand Bordage'
__copyright__ = '© 2018 NoriPyt'

parser = ArgumentParser(
    description='Finds anagrams for a given word or expression.')
parser.add_argument('expression', help='Word or expression for which '
                                       'to search for an anagram.')
parser.add_argument('-m', '--min-word-length', type=int, default=3,
                    help='Minimum length of each word of the anagram.')
parser.add_argument('-l', '--max-words', type=int,
                    help='Maximum number of words per anagram.')
parser.add_argument('-d', '--dictionary', type=FileType('r'),
                    default='/usr/share/dict/words',
                    help='Path to a dictionary file '
                         'containing a word per line.')
args = parser.parse_args()
MIN_WORD_LENGTH = args.min_word_length
MAX_WORDS = args.max_words


def remove_diacritics(text):
    return normalize('NFKD', text).encode('ASCII', 'ignore')

REMOVED_CHARS = punctuation.encode() + b' '

def simplify(text):
    return remove_diacritics(text.lower()).translate(
        None, REMOVED_CHARS).decode()


class SkipWord(Exception):
    pass


class WordCounter:
    def __init__(self, text=None, counts=None, size=None):
        if text is None:
            self.counts = counts
            self.size = size
        else:
            self.text = text
            simplified_text = simplify(text)
            self.counts = defaultdict(int)
            for c in simplified_text:
                self.counts[c] += 1
            self.size = len(simplified_text)

    def narrow_words(self, words):
        chars = set(self.counts)
        for word in words:
            if MIN_WORD_LENGTH <= word.size <= self.size \
                    and set(word.counts) <= chars:
                yield word

    def __sub__(self, other):
        new_counts = self.counts.copy()
        for c, n in other.counts.items():
            if new_counts[c] > n:
                new_counts[c] -= n
            elif new_counts[c] == n:
                del new_counts[c]
            else:
                raise SkipWord
        return WordCounter(counts=new_counts,
                           size=self.size - other.size)

    def find_anagrams(self, words, anagram_words=()):
        if MAX_WORDS is not None and len(anagram_words) > MAX_WORDS:
            return
        if self.size == 0:
            yield ' '.join(anagram_words)
            return
        remaining_length = self.size
        words = list(self.narrow_words(words))
        for word in words:
            try:
                counter = self - word
            except SkipWord:
                continue
            yield from counter.find_anagrams(
                words, anagram_words + (word.text,))


all_words = [WordCounter(word[:-1]) for word in args.dictionary]

for anagram in WordCounter(args.expression).find_anagrams(all_words):
    print(anagram)
