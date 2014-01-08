from plone.autoform.interfaces import IFormFieldProvider
from plone.directives import form
from plone.supermodel import model
from rwproperty import getproperty, setproperty
from z3c.form.browser.checkbox import CheckBoxFieldWidget
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

    subsite_home = schema.Choice(
        vocabulary=subsite_vocabulary,
        title=_(
            u'label_subsite_home',
            default=u'Subsite toewijzing'
        ),
        description=_(u'help_subsite_home',
                      default=(u'Bepaalt in welke lokale website'
                               u' dit item thuishoort.')),
        required=False,
        missing_value=None
    )

    form.widget(subsite_show=CheckBoxFieldWidget)
    subsite_show = schema.Set(
        value_type=schema.Choice(vocabulary=subsite_vocabulary),
        title=_(
            u'label_subsite_show',
            default=u'Subsite syndicatie'
        ),
        description=_(u'help_subsite_show',
                      default=(u'Bepaalt in welke lokale websites'
                               u' dit item getoond wordt.')),
        required=False,
    )

    form.order_after(subsite_home='ICultactCore.expires')
    form.order_after(subsite_show='ISubsiteAssignment.subsite_home')
    form.read_permission(subsite_show='cmf.ReviewPortalContent')
    form.write_permission(subsite_show='cmf.ReviewPortalContent')


@form.default_value(field=ISubsiteAssignment['subsite_home'])
def default_subsite_home(data):
    return data.request.get('in_subsite', None)


@form.default_value(field=ISubsiteAssignment['subsite_show'])
def default_subsite_show(data):
    return set(data.request.get('in_subsite', None))


alsoProvides(ISubsiteAssignment, IFormFieldProvider)


class SubsiteAssignment(object):

    def __init__(self, context):
        self.context = context

    @getproperty
    def subsite_home(self):
        return getattr(self.context, 'subsite_home', None)

    @setproperty  # flake8: noqa
    def subsite_home(self, value):
        self.context.subsite_home = value
        # sync subsite_show
        home = value and [value] or []
        show = getattr(self.context, 'subsite_show', set())
        self.context.subsite_show = show.union(home)

    @getproperty
    def subsite_show(self):
        home = self.subsite_home and [self.subsite_home] or []
        show = getattr(self.context, 'subsite_show', set())
        # always includes subsite_home (if not None)
        return show.union(home)

    @setproperty  # flake8: noqa
    def subsite_show(self, value):
        home = self.subsite_home and [self.subsite_home] or []
        show = value or set()
        # always includes subsite_home (if not None)
        self.context.subsite_show = show.union(home)

#EOF
