# Run 'setup.py sdist register upload' to upload new version

import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-tokenapi',
    version='1.1',
    description='Add an API to your Django app using token-based authentication.',
    long_description=read('README.md'),
    author='Julian Pulgarin',
    author_email='julian@pulgarin.co',
    url='https://github.com/jpulgarin/django-tokenapi',
    packages=['tokenapi'],
    license='Apache License, Version 2.0',
)
