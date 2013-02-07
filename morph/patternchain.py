# patternchain.py -- Rename pattern chain

"""Pattern Chain module"""

from morph import (
    pattern,
)

from morph.pattern import (
    generatePattern,
)

TYPE_REPLACE = 'replace'

TYPES = [TYPE_REPLACE]


def generateFullReplaceChain(pats):
    if len(pats) == 0:
        return None
    patterns = []

    patterns.append(generatePattern(pats[0], mode=pattern.MODE_REPLACE))
    for pat in pats[1:]:
        patterns.append(generatePattern(pat))

    return PatternChain(patterns)


class PatternChain(list):
    """A Rename Pattern Chain"""

    def __eq__(self, other):
        return isinstance(other, PatternChain) and \
               len(self) == len(other) and \
               all(self[i] == other[i] for i in range(len(self)))

    def apply_to_strings(self, strings):
        newstrings = []
        for (index, string) in enumerate(strings):
            new = string
            for pattern in self:
                new = pattern.apply_to_string(string, new, index)
            newstrings.append(new)
        return newstrings

    def reset(self):
        for pattern in self:
            pattern.reset()

    def __str__(self):
        repr = ''
        for pattern in self:
            repr += "\t%s\n" % pattern
        return repr
