#!/usr/bin/env python3
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


from os import path, listdir, makedirs, mkdir
import sys
import yaml
import time
from glob import glob
from shutil import copy2

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
                                'sitename': cfg['sitename'],
                                'license': cfg['license']})
        with open(page, 'w') as file:
            file.write(html)


def generate_posts():
    posts = []
    alltags = []

    env = Environment()
    env.loader = FileSystemLoader('templates')

    listing = glob('posts/*md')
    for post in listing:

        print('Generating {0}...'.format(post))

        raw = open(post, 'r').read()
        headers, content = raw.split('---', 1)
        headers = yaml.load(headers)
        tags = headers['tags'].split(', ')
        slug = headers['slug']
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

        shortdate = str.join('.', (year, month, day))

        postpath = path.join(year, month, day, slug)
        try:
            makedirs(postpath)
        except OSError:
            pass

        if 'files' in headers:
            files = headers['files'].split(', ')
            for file in files:
                copy2(path.join('posts/files/', file), postpath)

        link = '{0}/'.format(postpath)
        filename = '{0}index.html'.format(link)

        print('Generating HTML blog post at {0}...'.format(filename))

        post_object = dict(
            date=date,
            shortdate=shortdate,
            title=headers['title'],
            slug=headers['slug'],
            tags=tags,
            author=cfg['author'],
            sitename=cfg['sitename'],
            license=cfg['license'],
            content=content,
            link=link
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


def generate_archive(posts, tag_set):
    print('Generating blog archive...')

    env = Environment()
    env.loader = FileSystemLoader('templates')
    tpl = env.get_template('blog.html')
    html = tpl.render(dict(
        sitename=cfg['sitename'],
        license=cfg['license'],
        title='blog',
        posts=posts
    ))
    with open('blog.html', 'w') as file:
        file.write(html)

    for tag in tag_set:
        print('Generating {0} archive page...'.format(tag))
        post_list = []
        for post in posts:
            if tag in post['tags']:
                post_list.append(post)
        tpl = env.get_template('blog.html')
        html = tpl.render(dict(
            sitename=cfg['sitename'],
            title='blog: #{0}'.format(tag),
            posts=post_list
        ))
        tagpath = path.join('tag', tag)
        try:
            mkdir(tagpath)
        except OSError:
            pass
        with open('{0}/index.html'.format(tagpath), 'w') as file:
            file.write(html)


def generate_feeds(posts, tag_set):
    print('Generating atom feed...')

    env = Environment()
    env.loader = FileSystemLoader('templates')
    xml = env.get_template('feed.xml').render(
        items=posts,
        sitename=cfg['sitename'],
        author=cfg['author'],
        rooturl=cfg['rooturl'],
        license=cfg['license']
    )
    with open('feed.xml', 'w') as file:
        file.write(xml)

    for tag in tag_set:
        print('Generating {0} atom feed...'.format(tag))
        post_list = []
        for post in posts:
            if tag in post['tags']:
                post_list.append(post)
        xml = env.get_template('feed.xml').render(
            items=post_list,
            sitename=cfg['sitename'],
            author=cfg['author'],
            rooturl=cfg['rooturl'],
            tagtitle=' &bull; {0}'.format(tag)
        )
        tagpath = path.join('tag', tag)
        try:
            mkdir(tagpath)
        except OSError:
            pass
        with open('{0}/feed.xml'.format(tagpath), 'w') as file:
            file.write(xml)


def main():
    generate_pages()
    posts, tag_set = generate_posts()
    generate_archive(posts, tag_set)
    generate_feeds(posts, tag_set)


if __name__ == '__main__':
    main()
