#!/usr/bin/python2

'''Setup.'''

from setuptools import setup, find_packages
import glob

setup(
    name='spotexp',
    version='1.0',
    description='Spotify playlist exporter.',
    author='Cyker Way',
    license='MIT',
    url='http://projects.cykerway.com/afp',
    packages=find_packages(),
    scripts=glob.glob('scripts/*'),
)
