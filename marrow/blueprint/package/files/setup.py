: yield '#!/usr/bin/env python\n'
: yield '# encoding: utf-8\n\n'

import os

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


setup(
		name = "${settings.name}",
		version = "${settings.version}",
		
		description = "${settings.descrip}",
		long_description = "",
		: if settings.url
		url = "${settings.url}",
		: end
		: if settings.author
		
		author = "${settings.author.partition(',')[0].strip()}",
		author_email = "${settings.author.partition(',')[2].strip()}",
		: end
		
		license = "${settings.license}",
		keywords = [],
		
		packages = find_packages(exclude=['test', 'example', 'conf', 'benchmark', 'tool', 'doc']),
		include_package_data = True,
		package_data = {'': [
				: if settings.readme
				'README.${settings.readme}',
				: end
				: if settings.license
				'LICENSE.txt'
				: end
			]},
		
		namespace_packages = [
				: for i in range(len(settings.package.split('.')[:-1]))
				'${'.'.join(settings.package.split('.')[:i + 1])}',
				: end
			],
		
		setup_requires = [
				: if settings.tests in ('', 'y')
				'pytest-runner',
				: end
			],
		
		tests_require = [
				: if settings.tests in ('', 'y')
				'pytest-runner',
				'coverage',
				'pytest',
				'pytest-cov',
				'pytest-spec',
				'pytest-flakes',
				: end
			],
		
		install_requires = [
			: if settings.requires
				: for pkg in (i.strip() for i in settings.requires.split(','))
				'#{pkg}',
				: end
			: end
			],
		
		extras_require = dict(
				development = [
						: if settings.tests in ('', 'y')
						'pytest-runner',
						'coverage',
						'pytest',
						'pytest-cov',
						'pytest-spec',
						'pytest-flakes',
						: end
					],
			),
		
		zip_safe = True,
		
		entry_points = {
				}
	)

: flush
