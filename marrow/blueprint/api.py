# encoding: utf-8

from __future__ import unicode_literals, print_function

from marrow.util.bunch import Bunch
from pprint import pprint
from getpass import getpass

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
            self.prepare()
            self.process()
            self.post()
        
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
                    value = option.default
                    break
                
                prompt = "\033[2K\033[1m%s%s%s: \033[m" % (option.title, (" [%s]" % ", ".join([(i if i else "<none>") for i in option.values])) if option.values else "", (" [default: %s]" % (option.default, )) if option.default else "")
                
                if option.hidden:
                    value = getpass(prompt)
                
                else:
                    value = raw_input(prompt).strip()
                
                if option.required and not value:
                    print("\033[2KValue is required.\r\033[1A", end="")
                    continue
                
                if not value:
                    value = option.default
                    break
                
                if value and not option.validator(value):
                    print("\033[2KInput fails validation, please try again.\r\033[1A", end="")
                    continue
                
                break
            
            settings[option.target] = option.cast(value)
            
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
                
                if hasattr(part.source, '__call__'):
                    part.source = part.source(options)
                
                if hasattr(part.target, '__call__'):
                    part.target = part.target(options)
                
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
                        data = dict(settings=options)
                        
                        if hasattr(part.data, '__call__'):
                            data.update(part.data(options))
                        else:
                            data.update(part.data)
                        
                        _, content = self.engines(source + '/' + part.source, data)
                    
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
    
    def prepare(self):
        pass
    
    def post(self):
        pass


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
    def __init__(self, target, source=None, condition=None, data=dict()):
        self.target = target
        self.source = path.join(*source) if isinstance(source, (tuple, list)) else source if source else target
        self.condition = condition if condition is not None else lambda s: True
        self.data = data
        
        super(File, self).__init__()


class Setting(object):
    """Define a configuration option which delares data to pass to the templates."""
    def __init__(self, target, title, help=None, required=False, validator=None, condition=None, values=None, default="", cast=None, hidden=False):
        self.target = target
        self.title = title
        self.help = help
        self.required = required
        self.validator = validator if validator is not None else lambda s: (True if values is None else s in values)
        self.condition = condition if condition is not None else lambda s: True
        self.values = values
        self.default = default
        self.cast = cast if cast is not None else lambda v: v
        self.hidden = hidden
        
        super(Setting, self).__init__()
