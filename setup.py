# Run 'python setup.py sdist bdist_wheel && twine upload dist/*' to upload new version

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='django-tokenapi',
    version='1.4',
    description='Add an API to your Django app using token-based authentication.',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    author='Julian Pulgarin',
    author_email='julian@pulgarin.co',
    url='https://github.com/jpulgarin/django-tokenapi',
    packages=['tokenapi'],
    install_requires=['six'],
    license='Apache License, Version 2.0',
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
    ],
)
