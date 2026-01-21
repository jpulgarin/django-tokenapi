# Run 'python setup.py sdist bdist_wheel && twine upload dist/*' to upload new version

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='django-tokenapi',
    version='2.1',
    description='Add an API to your Django app using token-based authentication.',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    author='Julián Pulgarín',
    url='https://github.com/jpulgarin/django-tokenapi',
    packages=['tokenapi'],
    install_requires=['Django>=2.0'],
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
