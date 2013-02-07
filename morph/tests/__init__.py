# __init__.py - Tests for morph

"""Tests for morph"""

import sys


if sys.version_info >= (2, 7):
    # If Python itself provides an exception, use that
    import unittest
    from unittest import TestCase as _TestCase
else:
    import unittest2 as unittest
    from unittest2 import TestCase as _TestCase

class TestCase(_TestCase):
    pass

def self_test_suite():
    names = [
        'pattern',
        'patternchain',
        ]
    module_names = ['morph.tests.test_' + name for name in names]
    loader = unittest.TestLoader()
    return loader.loadTestsFromNames(module_names)

def test_suite():
    result = unittest.TestSuite()
    result.addTests(self_test_suite())
    return result
