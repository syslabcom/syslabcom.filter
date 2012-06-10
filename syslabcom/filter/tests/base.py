from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.testing import z2


class SyslabcomFilter(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import syslabcom.filter
        self.loadZCML('configure.zcml', package=syslabcom.filter)

        z2.installProduct(app, 'syslabcom.filter')

    def setUpPloneSite(self, portal):
        # Needed to make skins work
        applyProfile(portal, 'Products.CMFPlone:plone')

        applyProfile(portal, 'syslabcom.filter:default')

    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'syslabcom.filter')


SYSLABCOM_FILTER_FIXTURE = SyslabcomFilter()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(SYSLABCOM_FILTER_FIXTURE,),
    name="SyslabcomFilter:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(SYSLABCOM_FILTER_FIXTURE,),
    name="SyslabcomFilter:Functional")
