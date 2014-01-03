from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.testing import z2
from zope.configuration import xmlconfig


def setUpZope(app, configurationContext):
    # load dependencies

    # Load self
    import cultact.subsite
    xmlconfig.file(
        'configure.zcml',
        cultact.subsite,
        context=configurationContext
    )
    xmlconfig.file(
        'tests.zcml',
        cultact.subsite.tests,
        context=configurationContext
    )


def tearDownZope(app):
    # Uninstall products installed above
    pass


class CultactSubsiteLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        setUpZope(app, configurationContext)

    def tearDownZope(self, app):
        tearDownZope(app)

    def setUpPloneSite(self, portal):
        # Installs all the Plone stuff. Workflows etc.
        applyProfile(portal, 'Products.CMFPlone:plone')
        # our stuff
        applyProfile(portal, 'cultact.subsite:default')


CULTACT_SUBSITE_FIXTURE = CultactSubsiteLayer()
CULTACT_SUBSITE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CULTACT_SUBSITE_FIXTURE,),
    name="CultactSubsiteLayer:Integration"
)
CULTACT_SUBSITE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CULTACT_SUBSITE_FIXTURE, z2.ZSERVER_FIXTURE),
    name="CultactSubsiteLayer:Functional"
)
