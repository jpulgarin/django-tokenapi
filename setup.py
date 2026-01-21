# Run 'python setup.py sdist bdist_wheel && twine upload dist/*' to upload new version

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='django-tokenapi2',
    version='2.1',
    description='A fork from Julian Pulgarin django-tokenapi with Django 4+ support.',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    author='Stanislas Guerra',
    author_email='stan@slashdev.fr',
    url='https://github.com/Starou/django-tokenapi',
    packages=['tokenapi'],
    install_requires=['six'],
    license='Apache License, Version 2.0',
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
