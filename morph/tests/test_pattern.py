# test_pattern.py -- Tests for Pattern

"""Tests for Pattern objects"""

from morph import (
    pattern
)

from morph.pattern import (
    LiteralPattern,
    NumericCounterPattern,
)

from morph.errors import (
    PatternModeError
)

from morph.tests import TestCase


class PatternTestCase(TestCase):

    def gen(self, pat, mode = pattern.MODE_APPEND):
        return pattern.generatePattern(pat, mode)

    def testGenerate(self):
        litPat = self.gen('abc')
        self.assertTrue(isinstance(litPat, LiteralPattern))
        self.assertEqual(LiteralPattern('abc'), litPat)

        litPat = self.gen('abc', mode = pattern.MODE_REPLACE)
        self.assertTrue(isinstance(litPat, LiteralPattern))
        self.assertEqual(LiteralPattern('abc', mode = pattern.MODE_REPLACE),
                        litPat)

        numcountpat = self.gen('###')
        self.assertTrue(isinstance(numcountpat, NumericCounterPattern))
        self.assertEqual(NumericCounterPattern(1, 3), numcountpat)

        numcountpat = self.gen('###', mode = pattern.MODE_REPLACE)
        self.assertTrue(isinstance(numcountpat, NumericCounterPattern))
        self.assertEqual(
                NumericCounterPattern(1, 3, mode = pattern.MODE_REPLACE),
                numcountpat)


class LiteralPatternTestCase(TestCase):

    def testApply(self):
        appendPat = LiteralPattern('abc')

        self.assertEqual('fileabc',
                         appendPat.apply_to_string('file', 'file', 0))

        replacePat = LiteralPattern('abc', pattern.MODE_REPLACE)
        self.assertEqual('abc',
                         replacePat.apply_to_string('file', 'file', 0))

        insertPat = LiteralPattern('abc', pattern.MODE_INSERT, 1)
        self.assertEqual('fabcile',
                         insertPat.apply_to_string('file', 'file', 0))

    def testStr(self):
        appendPat = LiteralPattern('abc')
        self.assertEqual('Literal (append, abc)', str(appendPat))

        replacePat = LiteralPattern('abc', pattern.MODE_REPLACE)
        self.assertEqual('Literal (replace, abc)', str(replacePat))

        insertPat = LiteralPattern('abc', pattern.MODE_INSERT, 1)
        self.assertEqual('Literal (insert, 1, abc)', str(insertPat))


class NumericCounterPatternTestCase(TestCase):

    def testApply(self):
        appendPat = NumericCounterPattern()

        self.assertEqual('file01',
                         appendPat.apply_to_string('file', 'file', 0))
        self.assertEqual('file02',
                         appendPat.apply_to_string('file', 'file', 0))

        appendPat1 = NumericCounterPattern(50, 3)

        self.assertEqual('file050',
                         appendPat1.apply_to_string('file', 'file', 0))
        self.assertEqual('file051',
                         appendPat1.apply_to_string('file', 'file', 0))

        replacePat = NumericCounterPattern(mode=pattern.MODE_REPLACE)

        self.assertEqual('01',
                         replacePat.apply_to_string('file', 'file', 0))
        self.assertEqual('02',
                         replacePat.apply_to_string('file', 'file', 0))

        insertPat = NumericCounterPattern(mode = pattern.MODE_INSERT,
                                          position=1)
        self.assertEqual('f01ile',
                         insertPat.apply_to_string('file', 'file', 0))
        self.assertEqual('f02ile',
                         insertPat.apply_to_string('file', 'file', 0))

    def testReset(self):
        replacePat = NumericCounterPattern(mode=pattern.MODE_REPLACE)

        self.assertEqual('01',
                         replacePat.apply_to_string('file', 'file', 0))
        self.assertEqual('02',
                         replacePat.apply_to_string('file', 'file', 0))

        replacePat.reset()

        self.assertEqual('01',
                         replacePat.apply_to_string('file', 'file', 0))
        self.assertEqual('02',
                         replacePat.apply_to_string('file', 'file', 0))

    def testStr(self):
        appendPat = NumericCounterPattern()
        self.assertEqual('NumericCounter (append, 1, 1, 2)', str(appendPat))

        replacePat = NumericCounterPattern(mode=pattern.MODE_REPLACE)
        self.assertEqual('NumericCounter (replace, 1, 1, 2)', str(replacePat))

        insertPat = NumericCounterPattern(mode=pattern.MODE_INSERT,
                                          position=1)
        self.assertEqual('NumericCounter (insert, 1, 1, 1, 2)', str(insertPat))
