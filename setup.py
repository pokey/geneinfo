#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'pubmedasync>=0.4.2',
]

test_requirements = [
]

setup(
    name='geneinfo',
    version='0.1.0',
    description="Get papers and info about genes",
    long_description=readme + '\n\n' + history,
    author="Pokey Rule",
    author_email='pokey.rule@gmail.com',
    url='https://github.com/pokey/geneinfo',
    packages=[
        'geneinfo',
    ],
    package_dir={'geneinfo':
                 'geneinfo'},
    entry_points={
        'console_scripts': [
            'geneinfo=geneinfo.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='geneinfo',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
