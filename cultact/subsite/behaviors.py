from plone.app.contenttypes.behaviors import collection
from plone.autoform.interfaces import IFormFieldProvider
from plone.directives import form
from plone.supermodel import model
from rwproperty import getproperty, setproperty
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.component import getMultiAdapter
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
        self.context.subsite_home = value and value or 'None'
        # sync subsite_show
        home = value and [value] or ['None']
        show = getattr(self.context, 'subsite_show', set())
        self.context.subsite_show = show.union(home)

    @getproperty
    def subsite_show(self):
        home = self.subsite_home and [self.subsite_home] or ['None']
        show = getattr(self.context, 'subsite_show', set())
        # always includes subsite_home (if not None)
        return show.union(home)

    @setproperty  # flake8: noqa
    def subsite_show(self, value):
        home = self.subsite_home and [self.subsite_home] or ['None']
        show = value or set()
        # always includes subsite_home (if not None)
        self.context.subsite_show = show.union(home)


class IMultisiteCollection(collection.ICollection):
    """A collection behavior that searches outside INavigationRoot.
    """


class MultisiteCollection(collection.Collection):
    """A collection behavior that searches outside INavigationRoot.

    This is not added as a separate behavior but overrides the
    upstream Collection behavior via overrides.zcml.
    """

    def results(self, batch=True, b_start=0, b_size=None,
                sort_on=None, limit=None, brains=False):
        querybuilder = getMultiAdapter((self.context, self.context.REQUEST),
                                       name='querybuilderresults')
        sort_order = 'reverse' if self.sort_reversed else 'ascending'
        if not b_size:
            b_size = self.item_count
        if not sort_on:
            sort_on = self.sort_on
        if not limit:
            limit = self.limit

        # path insertion removed
        # this basically reverts plone.app.contenttypes b4551ec2f2598

        # NB if you DO use path queries, INavigationRoot will be forced anyway
        # by plone.app.querystring.queryparser _path + _relativePath

        return querybuilder(
            query=self.query, batch=batch, b_start=b_start, b_size=b_size,
            sort_on=sort_on, sort_order=sort_order,
            limit=limit, brains=brains
        )

#EOF
