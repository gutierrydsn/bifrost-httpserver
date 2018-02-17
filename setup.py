import os
from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='bifrost-httpserver',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    #license='BSD License', 
    description='A simple server http with configurated in maping routes.',
    #long_description=README,
    author='gutierrydsn',
    author_email='gutierrydsn@hotmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ],
)