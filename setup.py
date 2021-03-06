from setuptools import setup, find_packages
from codecs import open
from os import path, environ

here = path.abspath(path.dirname(__file__)) #

with open(path.join(here, 'README.md'), encoding='utf-8') as f: # open readme
    long_description = f.read()

setup(
    name='PyRedisCache', 
    version='1.0.0', #
    description='Redis Python Implementation',
    long_description=long_description, 
    author='Bruce', 
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['gevent', 'loguru', "Flask"], 
    entry_points={
        'console_scripts': [
            'pyredis=src.pyredis:main', 
        ],
    }
)