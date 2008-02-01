from plone.theme.interfaces import IDefaultPloneLayer
from zope.interface import Interface, Attribute
from plone.portlets.interfaces import IPortletManager


class IFilterHelper(Interface):
    """Interface that holds verious methods for working with vocaularies"""

    def getIndexedValues(index):
        """ returns the target languages indexed by the catalog """

