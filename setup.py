from setuptools import setup, find_packages
import os

version = '0.1'

long_description = (
    open('README.txt').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(name='mooball.plone.spreedlycore',
      version=version,
      description="Plone Configuration Wrapper for Spreedly Core API",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Alex Stevens',
      author_email='alex@mooball.net',
      url='http://www.mooball.com/',
      license='zpl',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['mooball', 'mooball.plone'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'spreedly-core-python',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
  	  [z3c.autoinclude.plugin]
  	  target = plone
      """,
      )
