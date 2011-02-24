import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-api',
    version='0.1.0',
    description='Add an API to your Django app using token-based authentication.',
    long_description=read('README.md'),
    author='Julian Pulgarin',
    author_email='jp@julianpulgarin.com',
    url='https://github.com/jpulgarin/django-api',
    packages=['api'],
)
