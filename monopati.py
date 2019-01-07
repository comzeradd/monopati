#!/usr/bin/env python3
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


from glob import glob
from jinja2 import Environment, FileSystemLoader
from markdown import Markdown
from os import path, listdir, makedirs, remove
import re
from shutil import copy2, copytree, rmtree
import sys
import time
import yaml


try:
    cfg = yaml.load(open('config.yml', 'r').read())
    try:
        output = cfg['output']
    except KeyError:
        output = '.'
    else:
        if output.endswith('/'):
            output = output[:-1]
    try:
        makedirs(output)
    except OSError:
        pass
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
                                'license': cfg['license'],
                                'logo': cfg['logo'],
                                'rooturl': cfg['rooturl'],
                                'link': page})
        with open(output + '/' + page, 'w') as file:
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

        link = '{0}/'.format(path.join(year, month, day, slug))
        postpath = path.join(output, link)
        try:
            makedirs(path.join(postpath))
        except OSError:
            pass

        images = []
        if 'files' in headers:
            files = headers['files'].split(', ')
            for file in files:
                if (file.find('.png') != -1) or (file.find('.jpg') != -1):
                    images.append(file)
                copy2(path.join('posts/files/', file), postpath)

        filename = '{0}index.html'.format(postpath)

        print('Generating HTML blog post at {0}...'.format(filename))

        content = re.sub(
            r" src=[\"']([^/]+?)[\"']",
            ' src="/{0}{1}"'.format(link, r"\1"),
            content)

        content = re.sub(
            r" href=[\"'](?!mailto:)([^/]+?)[\"']",
            ' href="/{0}{1}"'.format(link, r"\1"),
            content)

        post_object = dict(
            date=date,
            shortdate=shortdate,
            title=headers['title'],
            slug=headers['slug'],
            tags=tags,
            author=cfg['author'],
            sitename=cfg['sitename'],
            license=cfg['license'],
            rooturl=cfg['rooturl'],
            logo=cfg['logo'],
            content=content,
            images=images,
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
        logo=cfg['logo'],
        title='blog',
        posts=posts
    ))
    with open(output + '/blog.html', 'w') as file:
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
            license=cfg['license'],
            logo=cfg['logo'],
            title='blog: #{0}'.format(tag),
            posts=post_list
        ))
        tagpath = path.join(output, 'tag', tag)
        try:
            makedirs(tagpath)
        except OSError:
            pass
        with open('{0}/index.html'.format(tagpath), 'w') as file:
            file.write(html)


def generate_feeds(posts, tag_set):
    print('Generating atom feed...')

    updated = str(time.strftime('%Y-%m-%dT%H:%M:%SZ'))

    env = Environment()
    env.loader = FileSystemLoader('templates')
    xml = env.get_template('feed.xml').render(
        items=posts[:10],
        sitename=cfg['sitename'],
        author=cfg['author'],
        rooturl=cfg['rooturl'],
        license=cfg['license'],
        logo=cfg['logo'],
        updated=updated
    )
    with open(output + '/feed.xml', 'w') as file:
        file.write(xml)

    for tag in tag_set:
        print('Generating {0} atom feed...'.format(tag))
        post_list = []
        for post in posts[:10]:
            if tag in post['tags']:
                post_list.append(post)
        xml = env.get_template('feed.xml').render(
            items=post_list,
            sitename=cfg['sitename'],
            author=cfg['author'],
            rooturl=cfg['rooturl'],
            tagtitle=' - {0}'.format(tag),
            updated=updated
        )
        tagpath = path.join(output, 'tag', tag)
        try:
            makedirs(tagpath)
        except OSError:
            pass
        with open('{0}/feed.xml'.format(tagpath), 'w') as file:
            file.write(xml)


def copy_static():
    dest = path.join(output, 'static')
    if path.exists(dest):
        rmtree(dest)
    copytree('static', dest)

    dest = path.join(output, 'favicon.ico')
    if path.exists(dest):
        remove(dest)
    copy2('favicon.ico', dest)




def main():
    generate_pages()
    posts, tag_set = generate_posts()
    generate_archive(posts, tag_set)
    generate_feeds(posts, tag_set)

    if output != '.':
        copy_static()


if __name__ == '__main__':
    main()
