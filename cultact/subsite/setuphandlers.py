import logging
import transaction

from plone import api

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
    if not api.content.get(path='/maastricht'):
        log.info('Creating subsite: maastricht')
        api.content.create(
            type='cultact.maastrichtsite',
            title='Maastrichtnet',
            container=site)
        api.content.rename(obj=site['maastrichtnet'],
                           new_id='maastricht')
    if not api.content.get(path='/sittard'):
        log.info('Creating subsite: sittard')
        api.content.create(
            type='cultact.sittardsite',
            title='Uit In Sittard',
            container=site)
        api.content.rename(obj=site['uit-in-sittard'],
                           new_id='sittard')
    if not api.content.get(path='/code043'):
        log.info('Creating subsite: code043')
        api.content.create(
            type='cultact.code043site',
            title='Code 043',
            container=site)
        api.content.rename(obj=site['code-043'],
                           new_id='code043')
