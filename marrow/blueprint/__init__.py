#!/usr/bin/env python
# encoding: utf-8



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
        pass
    
    def create(self, template, target, **kw):
        """Create a directory tree based on a template.
        
        For a listing of avaiable templates, use the "list" command.
        """
        pass


if __name__ == '__main__':
    from marrow.script import execute
    execute(Blueprint)
