from setuptools import setup, find_packages
import sys, os

version = '0.0.1'

setup(
    name='ckanext-ogcpreview',
    version=version,
    description="Functionality for previewing OGC services",
    long_description='''
    ''',
    classifiers=[],
    keywords='',
    author='Arizona Geological Survey',
    author_email='adrian.sonnenschein@azgs.az.gov',
    url='http://geothermaldata.org',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.ogcpreview'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    entry_points=\
    """
    [ckan.plugins]
    ogc_preview=ckanext.ogcpreview.plugin:OGCPreview
    """,
)