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


class FilePatternChain(PatternChain):

    def insert_file(self, filename, position):
        self.append(('insert',filename, position))

    def delete_file(self, position):
        self.append(('delete', position))

    def move_file(self, original, new):
        self.append(('move', original, new))

    def apply_to_strings(self, strings):
        nstrings = list(strings)
        for change in self:
            if change[0] == 'insert':
                nstrings.insert(change[2], change[1])
            elif change[0] == 'delete':
                del nstrings[change[1]]
            elif change[0] == 'move':
                nstrings.insert(change[2], nstrings.pop(change[1]))
        return nstrings

    def map_to_strings(self, strings):
        file_map = zip(strings, strings)
        for change in self:
            if change[0] == 'insert':
                file_map.insert(change[2], (None, change[1]))
            elif change[0] == 'delete':
                filename =  file_map.pop(change[1])[0]
                file_map.append((filename, None))
            elif change[0] == 'move':
                file_map.insert(change[2], file_map.pop(change[1]))

        return file_map

    def reset(self):
        pass

    def __str__(self):
        repr = ''
        for change in self:
            repr += "\t%s\n" % (change,)
        return repr
