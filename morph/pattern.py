# pattern.py -- Rename pattern

"""Pattern base module"""

import re
import os

from morph.errors import (
    PatternModeError,
)

MODE_APPEND = "append"
MODE_REPLACE = "replace"
MODE_INSERT = "insert"

MODES = [MODE_APPEND, MODE_REPLACE, MODE_INSERT]

def generatePattern(pat, mode=MODE_APPEND):
    if isinstance(pat, str):
        if re.match('^#+$', pat):
            return NumericCounterPattern(padding=len(pat), mode=mode)
        else:
            return LiteralPattern(pat, mode=mode)
    else:
        raise TypeError(pat)


class Pattern(object):
    """A Rename Pattern"""

    def apply_to_string(self, original, new, position):
        raise NotImplementedError()

    def reset(self):
        raise NotImplementedError()


class LiteralPattern(Pattern):

    def __init__(self, literal=None, mode=MODE_APPEND, position=0):
        super(LiteralPattern, self).__init__()

        if literal is None:
            raise ValueError('literal needed')

        self.literal = literal
        self.mode = mode
        self.position = int(position)

    def __eq__(self, other):
        return isinstance(other, LiteralPattern) and \
               self.literal == other.literal and \
               self.mode == other.mode

    def apply_to_string(self, original, new, position):
        dirname, basename = os.path.split(new)

        if self.mode == MODE_APPEND:
            name = basename + self.literal
        elif self.mode == MODE_INSERT:
            name = basename[:self.position] + \
                   self.literal + basename[self.position:]
        elif self.mode == MODE_REPLACE:
            name = self.literal
        else:
            raise PatternModeError(self.mode)

        return os.path.join(dirname, name)

    def reset(self):
        pass

    def __str__(self):
        if self.mode == MODE_APPEND:
            return 'Literal (%s, %s)' % (self.mode, self.literal)
        elif self.mode == MODE_INSERT:
            return 'Literal (%s, %d, %s)' % (self.mode, self.position, self.literal)
        elif self.mode == MODE_REPLACE:
            return 'Literal (%s, %s)' % (self.mode, self.literal)
        else:
            raise PatternModeError(self.mode)


class NumericCounterPattern(Pattern):

    def __init__(self, start=1, padding=2, mode=MODE_APPEND, position=0):
        super(NumericCounterPattern, self).__init__()
        self.start = int(start)
        self.counter = int(start)
        self.padding = int(padding)
        self.mode = mode
        self.position = int(position)

    def __eq__(self, other):
        return isinstance(other, NumericCounterPattern) and \
               self.start == other.start and \
               self.padding == other.padding and \
               self.mode == other.mode

    def apply_to_string(self, original, new, position):
        dirname, basename = os.path.split(new)
        self.counter += 1

        counterstr = ('%%0%dd' % self.padding) % (self.counter - 1) 

        if self.mode == MODE_APPEND:
            name = basename + counterstr
        elif self.mode == MODE_INSERT:
            name = basename[:self.position] + \
                   counterstr + basename[self.position:]
        elif self.mode == MODE_REPLACE:
            name = counterstr
        else:
            raise PatternModeError(self.mode)

        return os.path.join(dirname, name)

    def reset(self):
        self.counter = self.start

    def __str__(self):
        if self.mode == MODE_APPEND:
            return 'NumericCounter (%s, %d, %d, %d)' % (self.mode, self.start, self.counter, self.padding)
        elif self.mode == MODE_INSERT:
            return 'NumericCounter (%s, %d, %d, %d, %d)' % (self.mode, self.position,
                    self.start, self.counter, self.padding)
        elif self.mode == MODE_REPLACE:
            return 'NumericCounter (%s, %d, %d, %d)' % (self.mode, self.start, self.counter, self.padding)
        else:
            raise PatternModeError(self.mode)

patternmap = {
    'literal': LiteralPattern,
    'numericcounter' : NumericCounterPattern,
}


