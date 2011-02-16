# encoding: utf-8

from __future__ import unicode_literals, print_function

from marrow.util.bunch import Bunch
from pprint import pprint

try:
    import readline

except ImportError:
    pass

import os
from os import path

from alacarte.core import Engines


__all__ = ['Blueprint', 'Folder', 'File', 'Setting']



class Blueprint(object):
    """Blueprint uses a declarative style for defining structure."""
    
    base = None
    inherits = None
    engine = 'mako'
    
    settings = []
    manifest = []
    
    def __init__(self, target, **options):
        self.target = target
        self.cmdopts = options
        self.engines = Engines(self.engine)
        super(Blueprint, self).__init__()
    
    def __call__(self, required_only=False):
        try:
            self.questions(self.cmdopts, required_only)
            self.process()
        
        except KeyboardInterrupt:
            pass
    
    def questions(self, cmdopts, required_only=False):
        settings = Bunch()
        
        for option in self.settings:
            if option.help:
                print("\n\033[2K\033[2m%s\33[m\r\033[1A" % option.help, end="")
            
            while True:
                if option.target in cmdopts:
                    print("\033[2K\033[1m", option.title, (" [%s]" % ", ".join([(i if i else "<none>") for i in option.values])) if option.values else "", end=": \033[m", sep="")
                    print(cmdopts[option.target])
                    value = cmdopts[option.target]
                    break
                
                elif (required_only and not option.required) or not option.condition(settings):
                    value = u''
                    break
                
                value = raw_input("\033[2K\033[1m%s%s: \033[m" % (option.title, (" [%s]" % ", ".join([(i if i else "<none>") for i in option.values])) if option.values else "")).strip()
                
                if option.required and not value:
                    print("\033[2KValue is required.\r\033[1A", end="")
                    continue
                
                if value and not option.validator(value):
                    print("\033[2KInput fails validation, please try again.\r\033[1A", end="")
                    continue
                
                break
            
            settings[option.target] = value
            
            print("\033[J", end="")
        
        self.options = settings
    
    def process(self):
        print("\nExpanding into %s...\n" % (self.target, ))
        options = self.options
        
        # pprint(dict(options))
        # print()
        
        def recurse(parts, target, source, indent=0):
            parts = list(parts)
            
            while parts:
                part = parts.pop(0)
                
                if isinstance(part, (Folder, File)) and not part.condition(options):
                    # print("%sSkipping source %s %s..." % ("    " * indent, part.__class__.__name__.lower(), part.source))
                    continue
                
                if isinstance(part, Folder):
                    print("%sEntering %s..." % ("    " * indent, part.target))
                    
                    newtarget = path.join(target, part.target) if part.target else target
                    if not path.exists(newtarget):
                        os.makedirs(newtarget)
                    
                    recurse(part.children, newtarget, (source + '/' + part.source) if part.source else source, indent+1)
                
                elif isinstance(part, File):
                    print("%sConstructing %s%s..." % ("    " * indent, part.target, (" from %s" % (part.source, )) if part.source != part.target else ""))
                    # print("%s -> %s" % (source + '/' + part.source, path.join(target, part.target)))
                    try:
                        _, content = self.engines(source + '/' + part.source, dict(settings=options))
                    
                    except:
                        print("\nError constructing %s%s.\n" % (part.target, (" from %s" % (part.source, )) if part.source != part.target else ""))
                        raise
                    
                    with open(path.join(target, part.target), 'w') as fh:
                        fh.write(content)
                
                elif hasattr(part, '__call__'):
                    additional = part(self.options)
                    parts.extend(additional)
        
        recurse(self.manifest, self.target, self.base)
        
        print("\nConstruction finished.")


class Folder(object):
    """"""
    def __init__(self, target, source=None, children=None, condition=None):
        self.target = target
        self.source = source
        self.children = children if children is not None else []
        self.condition = condition if condition is not None else lambda s: True
        
        super(Folder, self).__init__()


class File(object):
    """"""
    def __init__(self, target, source=None, condition=None):
        self.target = target
        self.source = path.join(*source) if isinstance(source, (tuple, list)) else source if source else target
        self.condition = condition if condition is not None else lambda s: True
        
        super(File, self).__init__()


class Setting(object):
    """Define a configuration option which delares data to pass to the templates."""
    def __init__(self, target, title, help=None, required=False, validator=None, condition=None, values=None):
        self.target = target
        self.title = title
        self.help = help
        self.required = required
        self.validator = validator if validator is not None else lambda s: (True if values is None else s in values)
        self.condition = condition if condition is not None else lambda s: True
        self.values = values
        
        super(Setting, self).__init__()
