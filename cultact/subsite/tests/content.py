import logging

from plone.dexterity import content
from plone.supermodel import model
from zope.interface import implements

log = logging.getLogger(__name__)


class ITestDocument(model.Schema):
    """Test content interface.
    """


class TestDocument(content.Item):
    """Test content item
    """
    implements(ITestDocument)
