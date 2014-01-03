from setuptools import setup, find_packages

version = '0.1'

setup(
    name='cultact.subsite',
    version=version,
    description="Subsite implementation for Plone",
    long_description=open("README.txt").read(),
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='',
    author='Guido Stevens',
    author_email='guido.stevens@cosent.net',
    url='http://cosent.nl',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['cultact'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
    ],
    extras_require={
        'test': ['plone.app.testing']
    },
    entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
)
