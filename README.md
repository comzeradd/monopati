# monopati

A minimalistic static content generator.

You can read the [relevant post](https://www.roussos.cc/2016/01/11/monopati/) on why I started building this. Monopati is inspired by other great minimalistic content generators, like [bucket3](https://github.com/vrypan/bucket3/) and [habu](https://github.com/botherder/habu).

[![license](https://img.shields.io/badge/license-AGPL%203.0-6672D8.svg)](LICENSE)

## Usage

Install from pypi:

```
sudo pip install monopati
```

On first run create the website folder:

```
monopati --path=mywebsite init
```

This will create a folder named `mywebsite`. Inside that folder there is a
configuration example file that you should copy and edit to meet your needs.

```
cd mywebsite
cp config.yml.dist config.yml
```

Finally, build your website:

```
monopati render
```

This will generate all necessary files for serving the website, under the
folder you picked as output in your configuration file.

### Structure

Use `posts`, `pages` folders for blog and static content respectively.

Use templates for adjusting UI to fit your needs.
[Jinja2](http://jinja.pocoo.org/) template engine is being used for
both templates and pages. [Markdown](https://en.wikipedia.org/wiki/Markdown)
for blog posts.

### Example

The code comes with one example post (under the `posts`) folder. You can check
how the metadata header is being user and some basic syntax and how images can be
added to a post. Under the `pages` folder there is a static template example
which serves as the landing and about page of your site.

## Support

[![Liberapay receiving](https://img.shields.io/liberapay/receives/comzeradd)](https://liberapay.com/comzeradd/donate)
