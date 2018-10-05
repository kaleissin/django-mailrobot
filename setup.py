#!/usr/bin/env python

import sys

from distutils.core import setup
from setuptools import find_packages

sys.path.append('./src')
import mailrobot

README_FILE = open('README.rst')
try:
    long_description = README_FILE.read()
finally:
    README_FILE.close()

setup(
        name='django-mailrobot',
        version=mailrobot.__version__,
        packages=['mailrobot'],
        package_dir = {'': 'src',},
        include_package_data=True,
        zip_safe=False,
        platforms=['any'],
        description='Stores and sends canned email responses.',
        author_email='kaleissin@gmail.com',
        author='kaleissin',
        long_description=long_description,
        classifiers=[
                'Development Status :: 4 - Beta',
                'Environment :: Web Environment',
                'Framework :: Django',
                'Intended Audience :: Developers',
                'License :: OSI Approved :: MIT License',
                'Operating System :: OS Independent',
                'Programming Language :: Python',
                'Programming Language :: Python :: 2',
                'Programming Language :: Python :: 2.7',
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.5',
                'Programming Language :: Python :: 3.6',
                'Programming Language :: Python :: 3.7',
                'Topic :: Communications :: Email',
                'Topic :: Software Development :: Libraries :: Application Frameworks',
                'Topic :: Software Development :: Libraries :: Python Modules',
                'Framework :: Django',
                'Framework :: Django :: 1.8',
                'Framework :: Django :: 1.11',
        ]
)
