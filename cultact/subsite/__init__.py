from collections import OrderedDict
from plone import api
from zope.i18nmessageid import MessageFactory

_ = MessageFactory("cultact.subsite")

# the ids here have to match interface and type names!
# browser layer:     IMaastrichtLayer
# content interface: IMaastrichtSite
# content type:      cultact.maastrichtsite  < derived from id in setuphandlers
subsite_config = OrderedDict([('maastricht', u'Maastrichtnet'),
                              ('sittard', u'Uit In Sittard'),
                              ('code043', u'Code 043')])


def get_subsites():
    portal = api.portal.get()
    return [portal[k] for k in subsite_config.keys()]


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
