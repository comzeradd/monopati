# monopati

A minimalistic static content generator.

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
cp config.yml-dist config.yml
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
how the metadata header is being user and some basic syntax. Under the `pages`
folder there is a static template example which serves as the landing and about
page of your site.

## LICENSE

Licensed under the [GPLv3](LICENSE).
