from interfaces import IFilterHelper
from Products.CMFCore.utils import getToolByName
from zope.interface import implements
from Products.CMFPlone import utils
from Products.Five import BrowserView
from Products.Archetypes.utils import DisplayList


class FilterHelper(BrowserView):
    implements(IFilterHelper)

    def getIndexedValues(self, index):
        """ returns the target languages indexed by the catalog """
        pc = getToolByName(self, 'portal_catalog')
        return pc.uniqueValuesFor(index)