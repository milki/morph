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
