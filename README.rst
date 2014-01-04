Introduction
============

This package provides a subsite implementation for Plone.
It contains hardcoded configuration specific to our use case, but
may still be relevant for other Plonistas hunting for solutions.

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

In the future, some content needs to be able to be syndicated to chosen
"other" subsites.

Implementation
--------------

This implementation uses elements from plone.theme and collective.lineage
witout requiring either of those.

From plone.theme we take the approach of marking the request with a browser
layer that is specific for each subsite. This allows us to register views
and css/js resources for a specific subsite. Layer interface inheritance
is set up in such a way that we can also register browser components for
a group of subsites. 

Having a browser layer per subsite requires hardcoding the subsites in python.

Subsite request marking is based on virtual URL structure.
See cultact/subsite/tests/subsite.txt for browser layer tests.

From collective.lineage we take the approach of having subsite containers
which provide INavigationRoot and ISite i.e. local component registries.

On top of that we mirror the per-subsite browser layer interfaces into
per-subsite content interfaces, effectively providing a singleton class
specific to each subsite for maximally future-proof flexibility.

Since all of this is hardcoded anyway, a 'subsites' global provides
a listing of implemented subsites and a setuphandler ensures the creation
of the configured subsite instances.

A dexterity behavior makes it possible to assign any content object to
any subsite, even if it's outside any subsite containment (as most of our
content is). The assigned subsite defaults to a request.subsite convenience
attribute set by the before_traverse hook that marks the browser layer.

A catalog index enables querying for assigned subsites on content, hence
filtering content for a specific subsite.

Not implemented yet, but foreseen in the design, is a syndication behavior
that allows for targeted syndication of content to more than just the
assigned "home" subsite.

See docs/design.jpg for a sketch.

Credits
-------

Author: Guido A.J. Stevens
Thanks: Clayton Parker


|Cosent|_

This package is maintained by Cosent_.

.. _Cosent: http://cosent.nl
.. |Cosent| image:: http://cosent.nl/images/logo-external.png 
                    :alt: Cosent
