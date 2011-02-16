#!/usr/bin/env python
# encoding: utf-8

import sys, os

try:
    from distribute_setup import use_setuptools
    use_setuptools()

except ImportError:
    pass

from setuptools import setup, find_packages


setup(
        name = "${settings.name}",
        version = "${settings.version}",
        
        description = "${settings.descrip}",
        long_description = """""",
% if settings.author:
        author = "${settings.author.partition(',')[0].strip()}",
        author_email = "${settings.author.partition(',')[2].strip()}",
% endif
% if settings.url:
        url = url,
% else:
#       url = url,
% endif
#       download_url = "",
        license = license,
        keywords = '',
        
        install_requires = [
% if settings.requires:
%   for pkg in [i.strip() for i in settings.requires.split(',')]:
                '${pkg}',
%   endfor
% endif
            ],
        
        test_suite = 'nose.collector',
        tests_require = ['nose', 'coverage'],
        
        classifiers = [
                "Development Status :: 1 - Planning",
% if settings.license == 'gpl':
                "License :: OSI Approved :: GNU General Public License (GPL)",
% elif settings.license == 'lgpl':
                "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
% elif settings.license == 'mit':
                "License :: OSI Approved :: MIT License",
% endif
                "Operating System :: OS Independent",
                "Programming Language :: Python",
                "Topic :: Software Development :: Libraries :: Python Modules"
            ],
        
        packages = find_packages(exclude=['examples', 'tests', 'tests.*', 'docs', 'third-party']),
        include_package_data = True,
        package_data = {
                '': ['README${("." + settings.readme) if settings.readme else ""}', 'LICENSE'],
            },
        zip_safe = True,
        
        namespace_packages = [
% for i in range(len(settings.package.split('.')[:-1])):
                "${'.'.join(settings.package.split('.')[:i + 1])}",
% endfor
            ],
        
        entry_points = { }
    )
