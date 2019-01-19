from setuptools import setup
from monopati import __version__

setup(
    name='monopati',
    version=__version__,
    author='Nikos Roussos',
    author_email='nikos@roussos.cc',
    url='https://github.com/comzeradd/monopati/',
    description='a minimalistic static content generator',
    long_description=open('README.md').read(),
    include_package_data=True,
    zip_safe=False,
    license='LICENSE',
    install_requires=[
        'docopt',
        'Jinja2',
        'Markdown',
        'PyYAML'
    ],
    packages=['monopati'],
    scripts=['bin/monopati'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
    ]
)
