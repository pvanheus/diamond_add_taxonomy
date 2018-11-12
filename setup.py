#!/usr/bin/env python

from distutils.core import setup

setup(name='ncbi_taxid',
      version='0.1.0',
      description='Tools for working with the NCBI taxonomy database (and DIAMOND output)',
      author='Peter van Heusden',
      author_email='pvh@sanbi.ac.za',
      url='https://github.com/pvanheus/diamond_add_annotation',
      packages=['ncbi_taxid'],
      requires=['ete3', 'click', 'six'],
      entry_points={
          'console_scripts': ['diamond_add_taxonomy=ncbi_taxid.cli:annotate_diamond']
      },
      classifiers=["Development Status :: 3 - Alpha"])
