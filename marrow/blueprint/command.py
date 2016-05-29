#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

import os
import pkg_resources

from marrow.script import script, describe
from marrow.script.util import wrap, partitionhelp

from marrow.blueprint import release


__all__ = ['Blueprint']



class Blueprint(object):
    """Blueprint: create directory trees based on manifest templates.
    
    Blueprint is a utility that lets you quickly create directory trees using manifests.  Each Python package that is installed can declare manifests.
    
    Manifests can interactively (or via the command line) accept arguments, allowing for variable substitution and more.
    
    Examples include: Python packages, web framework applications, configuration files.
    """
    
    _cmd_script = dict(
            title = "blueprint",
            version = release.version,
            copyright = "Copyright 2011 Alice Bevan-McGregor"
        )
    
    @describe(verbose="Increase logging level to DEBUG.", quiet="Reduce logging level to WARN.")
    def __init__(self, verbose=False, quiet=False):
        pass
    
    def list(self):
        """List available templates."""
        
        print("Available blueprints:\n")
        
        # Load Python plugins.
        blueprints = dict([(i.name, i.load()) for i in pkg_resources.iter_entry_points('marrow.blueprint')])
        
        # Get the length of the longest plugin name.
        mlen = max([len(i) for i in blueprints])
        
        # Output one line per blueprint: name, then the first line of documentation (if available).
        for name in sorted(blueprints):
            doc = partitionhelp(getattr(blueprints[name], '__doc__', 'No description available.'))[0][0]
            print(" %-*s  %s" % (mlen, name, wrap(doc).replace("\n", "\n" + " " * (mlen + 3))))
        
        print("\nIf the last segment of the name is unambiguous you can omit the namespace.")
    
    @describe(blueprint="The blueprint to construct.", target="The path to construct the blueprint within.", required="Only prompt for required arguments.")
    def create(self, blueprint, target, required=False, **kw):
        """Create a directory tree based on a template.
        
        For a listing of avaiable templates, use the "list" command.
        """
        
        # Load Python plugins.
        blueprints = dict([(i.name, i.load()) for i in pkg_resources.iter_entry_points('marrow.blueprint')])
        for name in list(blueprints.keys()):
            short = name.partition('.')[2]
            
            if short in blueprints:
                blueprints[short] = False
                continue
            
            blueprints[short] = blueprints[name]
        
        blueprint = blueprints.get(blueprint, None)
        
        if blueprint is None:
            print("Unknown blueprint.  ", end='')
            self.list()
            return 1
        
        if blueprint is False:
            print("Ambiguous blueprint.  ", end='')
            self.list()
            return 2
        
        target = os.path.abspath(target)
        blueprint = blueprint(target, **kw)
        
        return blueprint(required)


def main():
    from marrow.script import execute
    execute(Blueprint)


if __name__ == '__main__':
    main()
