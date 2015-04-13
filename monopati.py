#!/usr/bin/env python
# Copyright (C) 2015 Nikos Roussos <nikos@roussos.cc>.
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


from os import path, listdir, makedirs
import sys
import yaml
import time

from markdown import Markdown
from jinja2 import Environment, FileSystemLoader


try:
    cfg = yaml.load(open('config.yml', 'r').read())
except IOError:
    print('No config.yml found. Copy config.yml-dist and edit it to fit your needs')
    sys.exit(0)


def generate_pages():
    env = Environment()
    env.loader = FileSystemLoader(['pages', 'templates'])
    for page in listdir('pages'):
        print('Generating page {0}...'.format(page))
        template = env.get_template(page)
        html = template.render({'page': page,
                                'author': cfg['author'],
                                'sitename': cfg['sitename']})
        with open(page, 'w') as file:
            file.write(html)


def generate_posts():
    posts = []
    alltags = []

    env = Environment()
    env.loader = FileSystemLoader('templates')

    for post in listdir('posts'):
        orig = path.join('posts', post)

        print('Generating {0}...'.format(orig))

        raw = open(orig, 'r').read()
        headers, content = raw.split('---', 1)
        headers = yaml.load(headers)
        tags = headers['tags'].split(', ')
        md = Markdown()
        content = md.convert(content)

        if 'date' in headers:
            date = headers['date']
        else:
            date = str(time.strftime('%Y-%m-%d %H:%M:%S'))

        datetime = time.strptime(str(date), '%Y-%m-%d %H:%M:%S')
        year = str(datetime.tm_year)
        month = ('0' + str(datetime.tm_mon) if datetime.tm_mon < 10 else str(datetime.tm_mon))
        day = ('0' + str(datetime.tm_mday) if datetime.tm_mday < 10 else str(datetime.tm_mday))
        postpath = path.join(year, month, day)
        try:
            makedirs(postpath)
        except OSError:
            pass
        filename = '{0}/{1}.html'.format(postpath, headers['slug'])

        print('Generating HTML blog post at {0}...'.format(filename))

        post_object = dict(
            date=date,
            title=headers['title'],
            slug=headers['slug'],
            tags=tags,
            author=cfg['author'],
            sitename=cfg['sitename'],
            content=content,
            link=filename
        )

        template = env.get_template('post.html')
        html = template.render(**post_object)
        with open(filename, 'w') as file:
            file.write(html)

        posts.append(post_object)
        for tag in tags:
            alltags.append(tag)

    posts.sort(key=lambda key: key['date'])
    posts.reverse()
    tag_set = set(alltags)

    return posts, tag_set


def generate_archive(posts):
    print('Generating blog archive...')

    env = Environment()
    env.loader = FileSystemLoader('templates')
    tpl = env.get_template('blog.html')

    html = tpl.render(dict(
        sitename=cfg['sitename'],
        page='archive',
        posts=posts
    ))

    with open('blog.html', 'w') as file:
        file.write(html)


def generate_feed(posts, tag_set):
    print('Generating atom feed...')

    env = Environment()
    env.loader = FileSystemLoader('templates')
    xml = env.get_template('feed.xml').render(
        items=posts,
        sitename=cfg['sitename'],
        author=cfg['author'],
        rooturl=cfg['rooturl']
    )
    with open('feed.xml', 'w') as file:
        file.write(xml)

    for tag in tag_set:
        post_list = posts
        print('Generating {0} atom feed...'.format(tag))
        for post in post_list:
            if 'python' not in post['tags']:
                post_list.pop()
        xml = env.get_template('feed.xml').render(
            items=post_list,
            sitename=cfg['sitename'],
            author=cfg['author'],
            rooturl=cfg['rooturl'],
            tagtitle=' &bull; {0}'.format(tag)
        )
        with open('{0}.xml'.format(tag), 'w') as file:
            file.write(xml)


def main():
    generate_pages()
    posts, tag_set = generate_posts()
    generate_archive(posts)
    generate_feed(posts, tag_set)


if __name__ == '__main__':
    main()