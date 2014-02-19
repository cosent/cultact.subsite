Introduction
============

This package provides a subsite implementation for Plone.
It contains hardcoded configuration specific to our use case, but
may still be relevant for other Plonistas hunting for solutions.
Either fork and reconfigure, or else pick the parts you like.

Use Case
--------

A set of related cultural agenda websites:
- common user database
- generic content sharing (code-driven)
- targeted content sharing (human-driven)
- some view logic and theming shared
- some view logic and theming site-specific


Constraints
-----------

Most of our content lives outside any subsite in the membrane user folders
which are in a profile container in the Plone SiteRoot.

Some content is subsite-specific and resides within a subsite.

All content, also the stuff outside subsites, needs to be assigned to
a "preferred" subsite.

See docs/design.jpg for an overview.


Implementation
==============

This implementation uses elements from plone.theme and collective.lineage
witout requiring either of those.

This package provides the following features:


Request marking
---------------

From plone.theme we take the approach of marking the request with a browser
layer that is specific for each subsite. This allows us to register views
and css/js resources for a specific subsite. Layer interface inheritance
is set up in such a way that we can also register browser components for
a group of subsites. 

Having a browser layer per subsite requires hardcoding the subsites in python.

A request.in_subsite convenience attribute is set by the before_traverse hook
that also marks the browser layer. This attribute is used by the subsite_assigment
behavior to provide a default setting for the subsite_home attribute.

See cultact/subsite/tests/subsite.txt for browser layer tests.

Subsite request marking is based on virtual URL structure, derived from
SERVER_NAME. The assumption is that VirtualHostMonster is used to anchor
a virtual host on a subsite, and then URL rewrites to access the userprofiles
that are located outside the subsite. VHM is needed to ensure that
absolute_url() plays nice with such acquisition. See example config below.

Set up this way, items that are not themselves contained in a subsite
will show up "as if" they were contained in the requested subsite.


Content containers
------------------

From collective.lineage we take the approach of having subsite containers
which provide INavigationRoot and ISite i.e. local component registries.

On top of that we mirror the per-subsite browser layer interfaces into
per-subsite content interfaces, effectively providing a singleton class
specific to each subsite for maximally future-proof flexibility.

Since all of this is hardcoded anyway, 'subsite_config' and 'get_subsites()'
provide a listing of implemented subsites. A setuphandler ensures the creation
of the configured subsite instances.


Assignment behavior
-------------------

subsite_home: A dexterity behavior makes it possible to assign any content object to
any subsite, even if it's outside any subsite containment (as most of our
content is). The assigned subsite id defaults to request.in_subsite.
The assigned "home" subsite can be assigned by any user
with the edit permission on content.

subsite_show: Content may be syndicated to other subsites by users with the reviewer
permission. The behavior enforces that the assigned home subsite will always be
included in the subsite_show set.


Catalog indexes
---------------

Two catalog indexes enable querying for assigned subsites on content, hence
filtering content for a specific subsite.

subsite_home: assigned subsite
subsite_show: all subsites in which this content should be shown

This allows you to query for:
1) all content for which this is the "home" subsite (or not)
2) all content that should be shown in this subsite (or not)
3) all content from other subsites syndicated to this subsite

Note that typically 2) will be a superset of 1).


Collection criteria
-------------------

Genericsetup registry records are created to enable using the
subsite_home and subsite_show indexes as criteria on any Collection.


MultisiteCollection behavior
----------------------------

The default Collection behavior from plone.app.contenttypes forces a
path query, that is then rewritten by plone.app.querystring to force 
containment within a INavigationRoot.

For our use case, we want to be able to query outside the current
INavigationRoot in order to syndicate content from other subsites,
and from the shared user profiles.

To make this possible, a MultisiteCollection behavior is provided
which does not inject a path query. This behavior overrides
the normal Collection behavior (via overrides.zcml).

You can now use subsite_home, subsite_show to set up any Collection 
search you'd like across multiple subsites.


Canonical URL SEO
-----------------

A viewlet that overrides plone.app.layout.links.CanonicalURL is provided
for SEO purposes, pointing to the canonical URL for objects that are shown
in a different subsite than their "home" subsite.


Gotchas
=======

Anything that is INavigationRoot aware in Plone will require customization
if you want to be able to access content outside a subsite (=INavigationRoot).

Typically, you'll want to provide custom search and navigation logic.

For Collections, the MultisiteCollection behavior only works as expected
if you do not use path queries. If you do need multisite path queries you'll
have to monkeypatch plone.app.querystring.queryparser.

For livesearch, you can either search across all subsites, inject extra query
variables via URL rewriting, or customize the livesearch view.

There may be other parts of Plone you might need to customize for your use case.


URL rewrites
============

For all of this to work you'll need a URL rewriting frontend config
that projects shared content outside of the subsite, into the subsite.

Example nginx configuration::


    # localhost development only!

    # This adds security headers
    add_header X-Frame-Options "SAMEORIGIN";
    add_header Strict-Transport-Security "max-age=15768000; includeSubDomains";
    add_header X-XSS-Protection "1; mode=block";
    add_header X-Content-Type-Options "nosniff";
    add_header Content-Security-Policy-Report-Only "default-src 'self'; img-src *; style-src 'unsafe-inline'; script-src 'unsafe-inline' 'unsafe-eval'";

    server {
        listen 80;
        server_name maastricht.localhost;
        # shared user folders
        rewrite ^/profielen/$  /profielen permanent;
        rewrite ^/profielen(.*)  /VirtualHostBase/http/$server_name:80/ka/VirtualHostRoot/profielen$1 last;
        # livesearch all content
        rewrite ^/livesearch(.*)  /VirtualHostBase/http/$server_name:80/ka/VirtualHostRoot/livesearch$1 last;
        # serve subsite
        rewrite ^/(.*)  /VirtualHostBase/http/$server_name:80/ka/maastricht/VirtualHostRoot/$1 last;
        location / {
            proxy_set_header Host $server_name;
            proxy_pass http://127.0.0.1:9933;
        }
    }

    server {
        listen 80;
        server_name sittard.localhost;
        # shared user folders
        rewrite ^/profielen/$  /profielen permanent;
        rewrite ^/profielen(.*)  /VirtualHostBase/http/$server_name:80/ka/VirtualHostRoot/profielen$1 last;
        # livesearch all content
        rewrite ^/livesearch(.*)  /VirtualHostBase/http/$server_name:80/ka/VirtualHostRoot/livesearch$1 last;
        # serve subsite
        rewrite ^/(.*)  /VirtualHostBase/http/$server_name:80/ka/sittard/VirtualHostRoot/$1 last;
        location / {
            proxy_set_header Host $server_name;
            proxy_pass http://127.0.0.1:9933;
        }

    }

YMMV.


Credits
=======

Author: Guido A.J. Stevens
Thanks: Clayton Parker


|Cosent|_

This package is maintained by Cosent_.

.. _Cosent: http://cosent.nl
.. |Cosent| image:: http://cosent.nl/images/logo-external.png 
                    :alt: Cosent
