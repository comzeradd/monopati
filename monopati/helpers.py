# Copyright (C) 2015-2019 Nikos Roussos <nikos@roussos.cc>.
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

from os import path, mkdir, listdir
from shutil import copy2, copytree
import sys


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
