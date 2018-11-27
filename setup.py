#!/usr/bin/env python

from distutils.core import setup

setup(name='diamond_add_taxonomy',
      version='0.1.2',
      description='Tools for working with the NCBI taxonomy database (and DIAMOND output)',
      author='Peter van Heusden',
      author_email='pvh@sanbi.ac.za',
      url='https://github.com/pvanheus/diamond_add_annotation',
      packages=['diamond_add_taxonomy'],
      requires=['ete3', 'click', 'six'],
      entry_points={
          'console_scripts': ['diamond_add_taxonomy=diamond_add_taxonomy.cli:annotate_diamond']
      },
      classifiers=["Development Status :: 3 - Alpha"])
