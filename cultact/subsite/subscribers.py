from five.localsitemanager import make_objectmanager_site
from zope.interface import directlyProvides, directlyProvidedBy
from zope.location.interfaces import ISite

from cultact.subsite.browser import interfaces as customlayers

import logging
log = logging.getLogger(__name__)


def subsite_request(event):
    """Parse the request URL to set the subsite variable
    on the request, so it will be accessible for all views.

    A "subsite" is a virtual site.

    ?test_subsite is only ever used in functional tests
    """
    request = event.request
    subsite_mapping = {'sittard': customlayers.ISittardLayer,
                       'maastricht': customlayers.IMaastrichtLayer,
                       'code043': customlayers.ICode043Layer}
    chosen = request.get('test_subsite', None)
    if not chosen:
        for (subsite, customlayer) in subsite_mapping.items():
            if subsite in request.SERVER_URL:
                chosen = subsite
    # devel
    if not chosen and 'localhost' in request.SERVER_URL:
        chosen = 'sittard'
    request.set('in_subsite', chosen)
    layers = [x for x in directlyProvidedBy(request)]
    layers.insert(0, customlayer)
    directlyProvides(request, *layers)


def subsite_added(context, event):
    """When a subsite is created, turn it into a component site

    This adds:

        IObjectManagerSite(IObjectManager, ISite)
           Object manager that is also a site.

    and sets a __before_traverse__ hook for component registry resolving
    """
    if not ISite.providedBy(context):
        make_objectmanager_site(context)
