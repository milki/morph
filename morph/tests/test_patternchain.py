# test_patternchain.py -- Tests for Pattern Chains

"""Tests for Pattern Chain objects"""

from morph import (
    pattern,
    patternchain
)

from morph.pattern import (
    LiteralPattern,
    NumericCounterPattern,
)

from morph.patternchain import (
    generateFullReplaceChain,
    PatternChain,
    FilePatternChain,
)

from morph.errors import (
    PatternModeError
)

from morph.tests import TestCase


class PatternChainTestCase(TestCase):

    def testGenFullReplace(self):
        chain = patternchain.generateFullReplaceChain([
            'abc_',
            '###'])
        litpat = LiteralPattern('abc_', mode = pattern.MODE_REPLACE)
        numcountpat = NumericCounterPattern(1, 3)

        self.assertEqual(PatternChain([litpat, numcountpat]), chain)

    def testStr(self):
        chain = patternchain.generateFullReplaceChain([
            'abc_',
            '###'])

        self.assertEqual("\tLiteral (replace, abc_)\n"
                         "\tNumericCounter (append, 1, 1, 3)\n",
                         str(chain))

    def testAppendApply(self):
        appendPat0 = LiteralPattern('abc')
        appendPat1 = LiteralPattern('123')

        chain = PatternChain([appendPat0, appendPat1])

        self.assertEqual(['fileabc123'],
                         chain.apply_to_strings(['file']))

        self.assertEqual(['file0abc123', 'file1abc123', 'file2abc123'],
                         chain.apply_to_strings(['file0', 'file1', 'file2']))

    def testReplaceApply(self):
        appendPat0 = LiteralPattern('abc_', mode = pattern.MODE_REPLACE)
        appendPat1 = NumericCounterPattern(1, 2)

        chain = PatternChain([appendPat0, appendPat1])

        self.assertEqual(['abc_01'],
                         chain.apply_to_strings(['file']))

        chain.reset()

        self.assertEqual(['abc_01', 'abc_02', 'abc_03'],
                         chain.apply_to_strings(['file0', 'file1', 'file2']))


class FilePatternChainTestCase(TestCase):

    def testApply(self):
        chain = FilePatternChain()

        chain.insert_file('file5', 5)
        chain.insert_file('file1.5', 2)
        chain.delete_file(0)
        chain.move_file(0, 2)
        chain.delete_file(2)

        self.assertEqual(
                ['file1.5', 'file2', 'file3', 'file4', 'file5'],
                chain.apply_to_strings(
                    ['file0', 'file1', 'file2', 'file3', 'file4'])
                )

    def testMap(self):
        chain = FilePatternChain()

        chain.insert_file('file5', 5)
        chain.insert_file('file1.5', 2)
        chain.delete_file(0)
        chain.move_file(0, 2)
        chain.delete_file(2)

        self.assertEqual(
                [(None, 'file1.5'),
                 ('file2', 'file2'),
                 ('file3', 'file3'),
                 ('file4', 'file4'),
                 (None, 'file5'),
                 ('file0', None),
                 ('file1', None)],
                chain.map_to_strings(
                    ['file0', 'file1', 'file2', 'file3', 'file4'])
                )

    def testStr(self):
        chain = FilePatternChain()

        chain.insert_file('file5', 4)
        chain.insert_file('file1.5', 2)
        chain.delete_file(0)
        chain.move_file(0, 2)
        chain.delete_file(2)

        self.assertEqual("\t('insert', 'file5', 4)\n"
                         "\t('insert', 'file1.5', 2)\n"
                         "\t('delete', 0)\n"
                         "\t('move', 0, 2)\n"
                         "\t('delete', 2)\n",
                         str(chain))
