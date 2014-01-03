from collections import OrderedDict


from plone.autoform.interfaces import IFormFieldProvider
from plone.directives import form
from plone.supermodel import model
from cultact.types.behaviors.core import ICultactCore  # FIXME
from rwproperty import getproperty, setproperty
from zope import schema
from zope.component import adapts
from zope.interface import alsoProvides
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from cultact.subsite import _

subsites = OrderedDict([('--', u'--'),
                        ('maastricht', u'Maastricht'),
                        ('sittard', u'Sittard'),
                        ('other', u'Overig')])

subsite_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value=k, token=k, title=v)
        for (k, v) in subsites.items()
    ]
)


class ISubsiteAssignment(model.Schema):
    """Metadata field for cultural content.
    """

    subsite = schema.Choice(
        vocabulary=subsite_vocabulary,
        title=_(
            u'label_subsite',
            default=u'Stadsregio'
        ),
        description=_(u'help_subsite',
                      default=(u'Bepaalt in welke lokale website'
                               u' dit item getoond wordt.')),
        required=True,
        missing_value=subsites.keys()[0],
    )

    form.order_before(subsite='ICultactCore.subjects')


@form.default_value(field=ISubsiteAssignment['subsite'])
def default_subsite(data):
    return data.request.subsite


alsoProvides(ISubsiteAssignment, IFormFieldProvider)


class SubsiteAssignment(object):
    implements(ISubsiteAssignment)
    adapts(ICultactCore)

    def __init__(self, context):
        self.context = context

    @getproperty
    def subsite(self):
        return getattr(self.context, 'subsite', None)

    @setproperty  # flake8: noqa
    def subsite(self, value):
        self.context.subsite = value



#EOF
