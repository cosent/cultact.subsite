from plone import api
from zope.interface import Interface, implements


class ISubsiteAware(Interface):

    def getSubsiteObject():
        """Resolve the subsite string into the actual Subsite."""

    def getURL():
        """Inject the Subsite path into the absolute_url."""


class SubsiteAware(object):
    """Mixin class for subsite-aware URL faking."""
    implements(ISubsiteAware)

    def getSubsiteObject(self):
        portal = api.portal.get()
        subsite = getattr(self.request, 'subsite', None)
        if subsite:
            return getattr(portal, subsite, None)

    def subsite_aware_url(self):
        # See ZPublisher/HTTPRequest.py
        subsiteobj = self.getSubsiteObject()
        if not subsiteobj:
            return self.context.absolute_url()

        subsite_path = subsiteobj.getPhysicalPath()
        path = [x for x in subsite_path]
        path.extend([x for x in self.context.getPhysicalPath()
                     if x not in subsite_path])
        return self.request.physicalPathToURL(path)
