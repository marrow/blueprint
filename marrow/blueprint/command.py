#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

import pkg_resources

from marrow.script.util import wrap, partitionhelp


__all__ = ['Blueprint']



class Blueprint(object):
    """Blueprint: create directory trees based on manifest templates.
    
    Blueprint is a utility that lets you quickly create directory trees using manifests.  Each Python package that is installed can declare manifests.
    
    Manifests can interactively (or via the command line) accept arguments, allowing for variable substitution and more.
    
    Examples include: Python packages, web framework applications, configuration files.
    """
    
    def __init__(self, verbose=False, quiet=False):
        pass
    
    def list(self):
        """List available templates."""
        
        print("Available blueprints:\n")
        
        blueprints = dict([(i.name, i.load()) for i in pkg_resources.iter_entry_points('marrow.blueprint')])
        
        mlen = max([len(i) for i in blueprints])
        
        for name in sorted(blueprints):
            doc = partitionhelp(getattr(blueprints[name], '__doc__', ''))[0][0]
            print(" %-*s  %s" % (mlen, name, wrap(doc).replace("\n", "\n" + " " * (mlen + 3))))
        
        print("\nIf the last segment of the name is unambiguous you can omit the namespace.")
    
    def create(self, template, target, **kw):
        """Create a directory tree based on a template.
        
        For a listing of avaiable templates, use the "list" command.
        """
        pass


def main():
    from marrow.script import execute
    execute(Blueprint)


if __name__ == '__main__':
    main()
