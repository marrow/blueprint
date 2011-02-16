# encoding: utf-8

from __future__ import unicode_literals, print_function

from marrow.blueprint.api import Blueprint, Folder, File, Setting


__all__ = ['PackageBlueprint']



def package(settings):
    def recurse(name):
        head, _, tail = name.partition('.')
        
        return [
                Folder(head, children=[
                        File('__init__.py', 'namespace.py' if tail else 'init.py')
                    ] + (recurse(tail) if tail else []))
            ]
    
    return recurse(settings.package)


class PackageBlueprint(Blueprint):
    """Create an installable Python package."""
    
    base = 'marrow.blueprint.package/files'
    inherits = None
    engine = 'mako'
    
    settings = [
            Setting('name', "Project Name", "The name to appear on the Python Package Index, e.g. CluComp.", required=True),
            Setting('package', "Package Name", "The name of the Python package, periods indicating namespaces, e.g. clueless.compiler.", required=True),
            Setting('version', "Package Version"),
            Setting('descrip', "Package Description"),
            Setting('license', "License", values=['', 'gpl', 'lgpl', 'mit']),
            Setting('author', "Author (Name, email)", validator=lambda s: ',' in s and '@' in s),
            Setting('readme', "README Format", values=['', 'rest', 'textile']),
            Setting('url', "Project URL"),
            Setting('scm.kind', "SCM System (First Commit)", values=['', 'hg', 'git']),
            Setting('scm.url', "SCM Repository", "Path to the repository, e.g. git@github.com:fahrvergnugen/clueless.git.", condition=lambda s: s.scm.kind),
            Setting('requires', "Required Packages", "Packages required for installation."),
        ]
    
    manifest = [
            File('.gitignore', 'scmignore', condition=lambda s: s.scm.kind == 'git'),
            File('.hgignore', 'scmignore', condition=lambda s: s.scm.kind == 'hg'),
            File('LICENSE', 'LICENSE.gpl', condition=lambda s: s.license == 'gpl'),
            File('LICENSE', 'LICENSE.lgpl', condition=lambda s: s.license == 'lgpl'),
            File('LICENSE', 'LICENSE.mit', condition=lambda s: s.license == 'mit'),
            File('README', condition=lambda s: s.readme == ''),
            File('README.rest', condition=lambda s: s.readme == 'rest'),
            File('README.textile', condition=lambda s: s.readme == 'textile'),
            File('setup.py'),
            File('setup.cfg'),
            Folder('tests', children=[
                    File('.keep', 'keep')
                ]),
            package
        ]
