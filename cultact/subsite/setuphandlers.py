import logging
import transaction

from plone import api

from cultact.subsite import subsite_config

log = logging.getLogger(__name__)


def importVarious(context):
    if context.readDataFile('cultact.subsite.marker.txt') is None:
        return
    log.info('importVarious')
    site = context.getSite()
    setup_subsites(site)
    transaction.commit()


def setup_subsites(site):
    # create default content - NOT via (archetypes) collective.setuphelpers
    for (id, title) in subsite_config.items():
        if not api.content.get(path='/%s' % id):
            log.info('Creating subsite: %s', id)
            obj = api.content.create(
                type='cultact.%ssite' % id,
                id=id,
                title=title,
                container=site)
            # cultact.types test will fail if not published
            if id in ('sittard', 'maastricht'):  # not: code043
                try:
                    api.content.transition(obj=obj, transition='publish')
                except:
                    log.error("Cannot publish %s (%s)",
                              id, "happens in policy testing")
