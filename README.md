# monopati

A minimalistic static content generator.

You can read the [relevant post](https://www.roussos.cc/2016/01/11/monopati/) on why. Monopati is inspired by other great minimalistic content generators, like [bucket3](https://github.com/vrypan/bucket3/) and [habu](https://github.com/botherder/habu).

[![license](https://img.shields.io/badge/license-AGPL%203.0-6672D8.svg)](LICENSE)

## Usage

Clone the repository:

```
git clone https://github.com/comzeradd/monopati.git
```

Install dependencies:

```
pip install -r requirements.txt
```

Use `posts`, `pages` folders for blog and static content respectively.

Use templates for adjusting UI to fit your needs.
[Jinja2](http://jinja.pocoo.org/) template engine is being used for
both templates and pages. [Markdown](https://en.wikipedia.org/wiki/Markdown)
for blog posts.

Copy configuration example and edit it to fit your site specifics.

```
cp config.yml.dist config.yml
```

Run monopati:

```
./monopati.py
```

This will generate all necessary files for serving the website.
Monopati doesn't create any subfolder for generating the files,
so it should be fairly easy to deploy it by just uploading the whole folder.

### Example

The code comes with one example post (under the `posts`) folder. You can check
how the metadata header is being user and some basic syntax and how images can be
added to a post. Under the `pages` folder there is a static template example
which serves as the landing and about page of your site.
