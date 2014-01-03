from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.dexterity import content
from plone.supermodel import model
from zope.component.interfaces import IPossibleSite
from zope.interface import implements
from zope import schema

from cultact.subsite import _


class ISubsite(model.Schema, INavigationRoot, IPossibleSite):
    """Marker interface for Subsite.
    Inspired by collective.lineage.

    INavigationRoot
      make this a navigation root

    IPossibleSite
      support local component registries

    Additional interfaces are added post-init by
    subscribers.subsite_added
    """

    title = schema.TextLine(
        title=_(u'label_title', default=u'Title'),
        description=_(u'help_title',
                      default=u'Prominente kopregel met naam of titel.'),
        required=True
    )


class ICityhub(ISubsite):
    """Marker interface for component registrations shared between
    multiple cityhub subsites, excluding non-cityhub subsites.
    """


class ISittardSite(ICityhub):
    """Dedicated marker interface for uitinsittard.nl
    Allows per-site component configuration.
    """


class IMaastrichtSite(ICityhub):
    """Dedicated marker interface for maastrichtnet.nl
    Allows per-site component configuration.
    """


class ICode043Site(ISubsite):
    """Dedicated marker interface for code043
    Allows per-site component configuration.

    Is NOT a cityhub.
    """


## We don't have a generic Subsite class
## Instead, each subsite has a dedicated class


class SittardSite(content.Container):
    """Cityhub Subsite singleton for uitinsittard.nl
    """
    implements(ISittardSite)


class MaastrichtSite(content.Container):
    """Cityhub Subsite singleton for maastrichtnet.nl
    """
    implements(IMaastrichtSite)


class Code043Site(content.Container):
    """Subsite singleton for code043.nl
    that is not a cityhub.
    """
    implements(ICode043Site)
