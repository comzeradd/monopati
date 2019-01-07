from setuptools import find_packages, setup


setup(
    name='monopati',
    packages=find_packages(),
    version='0.2.0',
    author='Nikos Roussos',
    author_email='nikos@roussos.cc',
    url='https://github.com/comzeradd/monopati/',
    description='a minimalistic static content generator',
    include_package_data=True,
    zip_safe=False,
    license='LICENSE',
    install_requires=[
        'docopt',
        'Jinja2',
        'Markdown',
        'PyYAML'
    ],
    scripts=['monopati.py'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
    ]
)
