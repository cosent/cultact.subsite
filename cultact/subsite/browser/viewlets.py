import urlparse

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from plone import api
from plone.memoize import view
from plone.app.layout.viewlets.common import ViewletBase
from zope.component import getMultiAdapter

from cultact.subsite import subsite_base


class CanonicalSubsiteURL(ViewletBase):
    """Overrides plone.app.layout.links.viewlets.CanonicalURL"""

    @view.memoize
    def render(self):
        context_state = getMultiAdapter(
            (self.context, self.request), name=u'plone_context_state')
        canonical_url = context_state.canonical_object_url()

        # override canonical url if context is shown in non-home subsite
        subsite_home = getattr(self.context, 'subsite_home', None)
        in_subsite = self.request.get('in_subsite', None)
        if subsite_home and in_subsite and subsite_home != in_subsite:
            base = subsite_base.get(subsite_home)
            if base:
                parts = urlparse.urlparse(canonical_url)
                canonical_url = urlparse.urljoin(base, parts.path)

        return u'    <link rel="canonical" href="%s" />' % canonical_url


class DoormatViewlet(ViewletBase):

    def available(self):
        return self.doormat is not None

    @property
    def doormat(self):
        context = aq_inner(self.context)
        cat = getToolByName(context, 'portal_catalog')
        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        navigation_root_path = portal_state.navigation_root_path()
        portal = api.portal.get()
        in_subsite = self.request.get('in_subsite', None)
        if in_subsite and in_subsite in portal:
            subsite_root = portal[in_subsite]
            navigation_root_path = '/'.join(subsite_root.getPhysicalPath())
        doormats = cat(portal_type='Doormat', path=navigation_root_path,
                       sort_on='created')
        if doormats:
            return doormats[0].getObject()
