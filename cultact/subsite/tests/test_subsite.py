import unittest2 as unittest

from Products.Five.component.interfaces import IObjectManagerSite
from zope.location.interfaces import ISite

from cultact.subsite import content
from cultact.subsite.testing import CULTACT_SUBSITE_INTEGRATION_TESTING


class TestSubsiteIntegration(unittest.TestCase):
    """Integration tests for subsite.

    For functional tests, see: subsite.txt doctest.
    """

    layer = CULTACT_SUBSITE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_installed(self):
        """Setuphandlers should install some subsites."""
        self.assertTrue('maastricht' in self.portal)
        mnet = self.portal['maastricht']
        self.assertTrue(content.ISubsite.providedBy(mnet))
        self.assertTrue(content.ICityhub.providedBy(mnet))
        self.assertTrue(content.IMaastrichtSite.providedBy(mnet))
        self.assertFalse(content.ISittardSite.providedBy(mnet))

    def test_enable_site(self):
        """Event handler should have configured local sitemanager."""
        mnet = self.portal['maastricht']
        self.assertTrue(ISite.providedBy(mnet))
        self.assertTrue(IObjectManagerSite.providedBy(mnet))
        self.assertNotEquals(self.portal.getSiteManager(),
                             mnet.getSiteManager())
