# encoding: utf-8

from marrow.blueprint.api import Blueprint, Folder, File


__all__ = ['PackageBlueprint']



class PackageBlueprint(object):
    """Create an installable Python package."""
    
    base = 'marrow.blueprint.project/files'
    inherits = None
    engine = 'mako'
    
    def package(self, settings):
        def recurse(name):
            head, _, tail = name.partition('.')
            
            return [
                    Folder(head if head else tail, 'package', [
                            File('__init__.py', '__namespace__.py' if head else '__init__.py')
                        ] + recurse(tail) if head else [])
                ]
        
        return recurse(settings.package)
    
    manifest = [
            File('.gitignore', 'scmignore', condition=lambda s: s.scm == 'git'),
            File('.hgignore', 'scmignore', condition=lambda s: s.scm == 'hg'),
            File('LICENSE', 'LICENSE.gpl', condition=lambda s: s.license == 'gpl'),
            File('LICENSE', 'LICENSE.lgpl', condition=lambda s: s.license == 'lgpl'),
            File('LICENSE', 'LICENSE.mit', condition=lambda s: s.license == 'mit'),
            File('README', condition=lambda s: s.readme == ''),
            File('README.rest', condition=lambda s: s.readme == 'rest'),
            File('README.textile', condition=lambda s: s.readme == 'textile'),
            File('setup.py'),
            File('setup.cfg'),
            package
        ]
