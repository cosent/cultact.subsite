from plone.dexterity.interfaces import IDexterityContent
from plone.rfc822.interfaces import IPrimaryFieldInfo
from Products.CMFPlone.interfaces.syndication import IFeed
from Products.CMFPlone.browser.syndication.adapters import BaseItem
from zope.component import adapts


# https://dev.plone.org/ticket/13632
# 4.3.? -> 4.3.2 backport
# https://github.com/plone/Products.CMFPlone/
# commit/a85dfe267071d4e3d6e8d5845460e1847b378a84


class DexterityItem(BaseItem):
    adapts(IDexterityContent, IFeed)

    def __init__(self, context, feed):
        super(DexterityItem, self).__init__(context, feed)
        self.dexterity = IDexterityContent.providedBy(context)
        try:
            self.primary = IPrimaryFieldInfo(self.context, None)
        except TypeError:
            self.primary = None
