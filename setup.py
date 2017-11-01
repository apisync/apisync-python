# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='apisync',
    version='0.1.0',
    description='Python package for Apisync services',
    long_description=readme,
    author='Andre Tessmann',
    author_email='andre@apisync.io',
    url='https://github.com/apisync/apisync-python',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
