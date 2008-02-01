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
        
        
        
        
    def getVocabularySubpath(self, vocabulary, key):
        """ returns a Display List with exactly one level of a tree Vocabulary
            given by key
        """
        pvt = getToolByName(self.context, 'portal_vocabularies')
        vocab = getattr(pvt, vocabulary)
        
        dl = DisplayList()
                
        _appendToDisplayList(dl, vocab.getVocabularyDict(vocab), None, key)
        
        return dl
        
        
def _appendToDisplayList(displaylist, vdict, valueparent, mykey='', add=0):
    """ append subtree to flat display list
    """
    if not vdict:
        return
    for key in vdict.keys():
        if type(vdict[key]) == type((1,2)):
            value  = vdict[key][0]
            subdict= vdict[key][1] or None
        else:
            value  = vdict[key]
            subdict= None
#        if valueparent:
#            value = '%s - %s' % (valueparent, value)
        if add==1:
            displaylist.add(key,value)
        if subdict:
            if key==mykey:
                _appendToDisplayList(displaylist, subdict, value, mykey=mykey, add=1)        
            else:
                _appendToDisplayList(displaylist, subdict, value, mykey=mykey, add=0)        
                  