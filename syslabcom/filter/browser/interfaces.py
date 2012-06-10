from zope.interface import Interface


class IFilterHelper(Interface):
    """Interface that holds verious methods for working with vocaularies"""

    def getIndexedValues(index):
        """ returns the target languages indexed by the catalog """

    def getVocabularySubpath(vocabulary, key):
        """ returns a Display List with exactly one level of a tree Vocabulary
            given by key
        """
    def listWFStatesByWorkflowname(wfname, filter_similar=False):
        """Returns the states of the denoted workflow, optionally filtering
           out states with matching title and id"""

    def getCreators():
        """ Return list of Creators (from the catalog index), looked up in the
        membership tool """

    def getRemotelanguages():
        """ Return all target languages from the catalog that are available
        in the portal language tool """


class IVocabularyHelper(Interface):
    """ """

    def getDisplayListFor(vocabularyName=''):
        """ """

    def getCountryList():
        """ """

    def getNaceList():
        """ """

    def getSubjectList():
        """ """
