"""A setuptools based setup module."""


from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
try:
    f = open(path.join(here, 'README.md'), encoding='utf-8')
    long_description = f.read()
except:
    pass
finally:
    long_description = "(n/a)"


setup(
    name='pyschemes',
    version='1.0.0',
    description='A Pythonic data-structure validator',
    long_description=long_description,
    url='https://github.com/shivylp/pyschemes',
    author='Shivaprasad',
    author_email='shiv.ylp@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Beta',
        'Intended Audience :: Developers',
    ],
    keywords='validator schema',
    packages=find_packages(exclude=['tests']),
    install_requires=[]
)
