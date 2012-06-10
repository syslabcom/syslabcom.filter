from Acquisition import aq_base
from plone.memoize.instance import memoize
from Products.Archetypes.utils import DisplayList
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from syslabcom.filter.browser.interfaces import IFilterHelper
from zope.interface import implements


class FilterHelper(BrowserView):
    implements(IFilterHelper)

    def getIndexedValues(self, index):
        """ returns the remote languages indexed by the catalog """
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

    @memoize
    def listWFStatesByWorkflowname(self, wfname, filter_similar=False):
        """Returns the states of the denoted workflow, optionally filtering
           out states with matching title and id"""
        states = []
        dup_list = {}
        wtool = getToolByName(self, 'portal_workflow')
        if not hasattr(aq_base(wtool), wfname):
            return list()
        else:
            wf = getattr(wtool, wfname)
            state_folder = getattr(wf, 'states', None)
            if state_folder is not None:
                if not filter_similar:
                    states.extend(state_folder.objectValues())
                else:
                    for state in state_folder.objectValues():
                        key = '%s:%s' % (state.id, state.title)
                        if not key in dup_list:
                            states.append(state)
                        dup_list[key] = 1
        return [(s.title, s.getId()) for s in states]

    @memoize
    def getCreators(self):
        """ See interface"""
        pc = getToolByName(self, 'portal_catalog')
        mtool = getToolByName(self, 'portal_membership')
        names = pc.uniqueValuesFor('Creator')
        nicenames = list()
        for name in names:
            if name.strip() == '':
                continue
            nice = mtool.getMemberInfo(name)
            nicenames.append((name, nice and nice['fullname'] or name))
        nicenames.sort(lambda x, y: cmp(x[1].lower(), y[1].lower()))
        return nicenames

    @memoize
    def getRemotelanguages(self):
        """ See interface """
        pc = getToolByName(self, 'portal_catalog')
        langtool = getToolByName(self, 'portal_languages')
        langs = pc.uniqueValuesFor('getRemoteLanguage')
        nicelangs = list()
        langinfo = langtool.getAvailableLanguageInformation()
        for lang in langs:
            li = langinfo.get(lang, None)
            if not li: continue
            nice = li.get('native', li.get('name', None))
            if nice:
                nicelangs.append((lang, nice))
        return nicelangs


def _appendToDisplayList(displaylist, vdict, valueparent, mykey='', add=0):
    """ append subtree to flat display list
    """
    if not vdict:
        return
    for key in vdict.keys():
        if type(vdict[key]) == type((1, 2)):
            value  = vdict[key][0]
            subdict = vdict[key][1] or None
        else:
            value = vdict[key]
            subdict = None
        # if valueparent:
        #     value = '%s - %s' % (valueparent, value)

        # if there is no mykey (e.g. because form was called without
        # local_keyword), just return top level
        if add == 1 or not mykey:
            displaylist.add(key, value)
        if subdict and mykey:
            if key == mykey:
                _appendToDisplayList(displaylist, subdict, value,
                                     mykey=mykey, add=1)
            else:
                _appendToDisplayList(displaylist, subdict, value,
                                     mykey=mykey, add=0)
