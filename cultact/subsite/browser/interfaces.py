from zope.interface import Interface


class ICultactSubsiteLayer(Interface):
    """Generic shared browser Layer for cultact.subsite"""


class ISubsiteLayer(ICultactSubsiteLayer):
    """browser Layer for cultact.subsite"""


class ICityhubLayer(ISubsiteLayer):
    """browser Layer for cultact.subsite"""


class ISittardLayer(ICityhubLayer):
    """browser Layer for cultact.subsite"""


class IMaastrichtLayer(ICityhubLayer):
    """browser Layer for cultact.subsite"""


class ICode043Layer(ISubsiteLayer):
    """browser Layer for cultact.subsite"""
