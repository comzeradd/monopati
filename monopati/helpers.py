# Copyright (C) 2015-2020 Nikos Roussos <nikos@roussos.cc>.
# This file is part of Monopati - https://github.com/comzeradd/monopati

# Monopati is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Monopati is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# See the file 'LICENSE' for more information.

import http.server
import socketserver
from os import path, mkdir, listdir, makedirs, chdir
from shutil import copy2, copytree
import sys
import yaml


def config():
    """
    Parse the configuration yaml file.
    """
    try:
        cfg = yaml.load(open('config.yml', 'r').read(), Loader=yaml.BaseLoader)
    except IOError:
        print('No config.yml found. Copy config.yml-dist and edit it to fit your needs')
        sys.exit(0)

    try:
        output = cfg['output']
    except KeyError:
        cfg['output'] = '.'
        return cfg

    if output.endswith('/'):
        output = output[:-1]

    try:
        makedirs(output)
    except OSError:
        pass

    return cfg


def kickstart(folder):
    dest = path.abspath(folder)

    if not path.isdir(dest):
        mkdir(dest)
        print('Creating website folder...')
    else:
        print('Folder already exists')
        sys.exit()

    skel = path.join(path.dirname(path.abspath(__file__)), 'skel')

    for item in listdir(skel):
        s = path.join(skel, item)
        d = path.join(dest, item)
        if path.isdir(s):
            copytree(s, d)
        else:
            copy2(s, d)


def serve(port):
    cfg = config()
    Handler = http.server.SimpleHTTPRequestHandler
    chdir(cfg['output'])
    with socketserver.TCPServer(('', port), Handler) as httpd:
        print('Serving at http://localhost:{0}'.format(port))
        httpd.serve_forever()
