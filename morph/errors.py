# errors.py -- Errors

"""batch-rename related exception classes"""


class PatternModeError(TypeError):
    """Indicates an invalid pattern mode"""

    def __init__(self, mode, *args, **kwargs):
        TypeError.__init__(self, "%s is not a valid pattern mode" % mode)
