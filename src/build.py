#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    markitup-hoard build script
    ~~~~~~

    :copyright: (c) 2012 by ytjohn
    :license: BSD, see LICENSE for more details.

USAGE:

build.py

Flow

 - iterates over files in modules like so: markitup-module.html
 - prepends templates/top.html
 - inserts modules/marktiup-module.html
 - addends templates/bottom.hml
 - outputs to tmp/markitup-module.html
 - compares tmp/markitup-module.html with ../markitup-module.html
    - if difference, mv tmp/markitup-module.html to ..
    - if not, discard tmp/markitup-module.html
"""

from mako.template import Template
from mako.lookup import TemplateLookup
import os


config = {
    'templates': 'templates/',
    'modules': 'modules/',
    'output': '../',
    'top': 'top.template.html',
    'bottom': 'bottom.template.html'
}
module = 'default'

def GetModules(config):
    files = os.listdir(config['modules'])
    return files

def FindModule(config, module):
    """
    Allows one to input several variants of a module name and returns the
    correct one. This is here for future expansion (specify an individual
    module as an argument).
    """
    modules = config['modules']
    variants = [
        module,
        "%s.html" % module,
        "markitup-%s" % module,
        "markitup-%s.html" % module
        ]

    for variant in variants:
        filename = "%s%s" % (modules, variant)
        if os.access(filename, os.R_OK):
            return variant

    # no variant found
    print "not found!"

def MakeModule(config, module):
    """
    Generates the output html from templates.
    """
    mylookup = TemplateLookup(directories=[config['templates'],
                                           config['modules']])
    top = mylookup.get_template(config['top']).render_unicode()
    bottom = mylookup.get_template(config['bottom']).render_unicode()
    set = mylookup.get_template(module).render_unicode()
    return ''.join([top, set, bottom])

def UpdateModule(config, module):
    thismodule = FindModule(config, module)
    new = MakeModule(config, thismodule)
    old = ReadModule(config, thismodule)
    if not(new == old):
        print "%s updating" % thismodule
        WriteModule(config, module, new)
    else:
        print "%s no change" % thismodule

def ReadModule(config, module):
    fullpath = ''.join([config['output'], module])
    try:
        f = open(fullpath, 'r')
        content = f.read()
        return content
    except:
        return None



def WriteModule(config, module, new):
    fullpath = ''.join([config['output'], module])
    with open(fullpath, 'w') as f:
        f.write(new)



modules = GetModules(config)
for module in modules:
    UpdateModule(config, module)
