from plone.autoform.interfaces import IFormFieldProvider
from plone.directives import form
from plone.supermodel import model
from rwproperty import getproperty, setproperty
from zope import schema
from zope.interface import alsoProvides
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from cultact.subsite import _
from cultact.subsite import subsite_config


subsite_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value=k, token=k, title=v)
        for (k, v) in subsite_config.items()
    ]
)


class ISubsiteAssignment(model.Schema):
    """Metadata field for cultural content.
    """

    subsite = schema.Choice(
        vocabulary=subsite_vocabulary,
        title=_(
            u'label_subsite',
            default=u'Subsite'
        ),
        description=_(u'help_subsite',
                      default=(u'Bepaalt in welke lokale website'
                               u' dit item getoond wordt.')),
        required=False,
        missing_value=None
    )


@form.default_value(field=ISubsiteAssignment['subsite'])
def default_subsite(data):
    return data.request.get('in_subsite', None)


alsoProvides(ISubsiteAssignment, IFormFieldProvider)


class SubsiteAssignment(object):

    def __init__(self, context):
        self.context = context

    @getproperty
    def subsite(self):
        return getattr(self.context, 'subsite', None)

    @setproperty  # flake8: noqa
    def subsite(self, value):
        self.context.subsite = value



#EOF
