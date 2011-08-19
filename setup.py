#!/usr/bin/env python
# encoding: utf-8

import os
import sys

from setuptools import setup, find_packages


if sys.version_info < (2, 6):
    raise SystemExit("Python 2.6 or later is required.")

exec(open(os.path.join("marrow", "blueprint", "release.py")))



setup(
        name = "marrow.blueprint",
        version = version,
        
        description = "Flexible manifest-driven file and folder creation.",
        long_description = '''\
For full documentation, see the README.textile file present in the package,
or view it online on the GitHub project page:

https://github.com/marrow/marrow.blueprint''',
        
        author = "Alice Bevan-McGregor",
        author_email = "alice+marrow@gothcandy.com",
        url = "https://github.com/marrow/marrow.blueprint",
        license = "MIT",
        
        install_requires = [
            'marrow.util < 2.0',
            'marrow.script < 3.0',
            'marrow.templating < 2.0'
        ],
        
        test_suite = 'nose.collector',
        tests_require = [
            'nose',
            'coverage',
            'mako'
        ],
        
        classifiers = [
                "Development Status :: 1 - Planning",
                "Environment :: Console",
                "Intended Audience :: Developers",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
                "Programming Language :: Python",
                "Topic :: Internet :: WWW/HTTP :: WSGI",
                "Topic :: Software Development :: Libraries :: Python Modules"
            ],
        
        packages = find_packages(exclude=['examples', 'tests']),
        include_package_data = True,
        package_data = {'': ['README.textile', 'LICENSE']},
        zip_safe = True,
        
        namespace_packages = ['marrow'],
        
        entry_points = {
                'console_scripts': [
                        'blueprint = marrow.blueprint.command:main'
                    ],
                'marrow.blueprint': [
                        'python.package = marrow.blueprint.package:PackageBlueprint',
                        'marrow.project = marrow.blueprint.project:ProjectBlueprint'
                    ]
            }
    )
