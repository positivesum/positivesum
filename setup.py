from setuptools import setup, find_packages
import sys, os

version = '0.1.2'

setup(name='positivesum',
      version=version,
      description='Package of tools that make Positive Sum process easier.',
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='wordpress joomla drupal database migration deployment package generation',
      author='Taras Mankovski',
      author_email='taras@positivesum.org',
      url='http://positivesum.org',
      license='GPLv2',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
