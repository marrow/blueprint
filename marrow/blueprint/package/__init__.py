# encoding: utf-8

from __future__ import unicode_literals

import sys
import pkg_resources

from marrow.blueprint.api import Blueprint, Folder, File, Setting


__all__ = ['PackageBlueprint']



def package(settings):
	def recurse(name):
		head, _, tail = name.partition('.')
		init = [File('__init__.py', ('namespace.py' if tail else 'init.py'))]
		return [Folder(head, children=(init + (recurse(tail) if tail else [])))]
	
	return recurse(settings.package)


def ls(base, prefix=None):
	return [i for i in pkg_resources.resource_listdir(*base.split('/', 1)) if (True if prefix is None else i.startswith(prefix))]


def extensions(base, prefix):
	return [i.rpartition('.')[2] for i in ls(base, prefix)]


def oneof(base, prefix, choice, ext=None):
	def inner(settings):
		selection = getattr(settings, choice)
		if not selection:
			return []
		
		return [File(prefix + '.' + (selection if ext is None else ext), prefix + '.' + selection)]
	
	return inner



class PackageBlueprint(Blueprint):
	"""Create an installable Python package."""
	
	base = 'marrow.blueprint.package/files'
	inherits = None
	
	settings = [
			Setting('name', "Project Name", "The name to appear on the Python Package Index, e.g. CluComp.", required=True),
			Setting('package', "Package Name",
				"The name of the Python package, periods indicating namespaces, e.g. clueless.compiler.", required=True),
			Setting('version', "Package Version"),
			Setting('descrip', "Package Description"),
			Setting('license', "LICENSE Format", values=[''] + extensions(base, 'LICENSE')),
			Setting('author', "Author", "Name, email\033K", validator=lambda s: ',' in s and '@' in s),
			Setting('readme', "README Format", values=[''] + extensions(base, 'README')),
			Setting('tests', "Use py.test?", "Include py.test test runner configuration? (Default: y)",
				values=['', 'y', 'n']),
			Setting('tox', "Use tox?", "Test across multiple runtimes using tox? (Default: n)",
				values=['', 'n', 'y'], condition=lambda s: s.tests in ('', 'y')),
			Setting('travis', "Use Travis CI?",
				"Include configuration and support for test execution on Travis? (Default: n)", values=['', 'n', 'y'],
				condition=lambda s: s.tests in ('', 'y', 'n')),
			Setting('url', "Project URL"),
			Setting('scm_kind', "SCM System (First Commit)", values=['', 'hg', 'git']),
			Setting('scm_url', "SCM Repository",
				"(Optional) Path to the repository, e.g. git@github.com:fahrvergnugen/clueless.git.",
				condition=lambda s: s.scm_kind),
			Setting('requires', "Required Packages", "Packages required for installation."),
		]
	
	manifest = [
			File('.gitignore', 'scmignore', condition=lambda s: s.scm_kind == 'git'),
			File('.hgignore', 'scmignore', condition=lambda s: s.scm_kind == 'hg'),
			
			File('.travis.yml', condition=lambda s: s.tests in ('', 'y') and s.travis == 'y'),
			File('tox.ini', condition=lambda s: s.tests in ('', 'y') and s.tox == 'y'),
			
			File('setup.py'),
			File('setup.cfg'),
			File('MANIFEST.in', 'keep'),
			
			Folder('.packaging'),
			Folder('test', children=[
					File('.keep', 'keep'),
				], condition=lambda s: s.tests in ('', 'y')),
			
			oneof(base, 'LICENSE', 'license', 'txt'),
			oneof(base, 'README', 'readme'),
			package
		]

