import doctest
import unittest2 as unittest

from plone.testing import layered
from cultact.subsite.testing import CULTACT_SUBSITE_FUNCTIONAL_TESTING

optionflags = (doctest.NORMALIZE_WHITESPACE
               | doctest.ELLIPSIS
               | doctest.REPORT_NDIFF
               | doctest.REPORT_ONLY_FIRST_FAILURE)


normal_testfiles = ['subsite.txt', 'behavior.txt']


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests(
        [layered(doctest.DocFileSuite(test,
                                      optionflags=optionflags),
                 layer=CULTACT_SUBSITE_FUNCTIONAL_TESTING)
         for test in normal_testfiles])
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
