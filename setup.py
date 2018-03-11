#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pathlib
import re
import subprocess

from setuptools import find_packages, setup
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools.command.test import test

__author__ = 'Paweł Zadrożny'
__copyright__ = 'Copyright (c) 2018, Pawelzny'
__requires__ = ['pipenv']

base_dir = pathlib.Path(__file__).parent

with open('README.rst', encoding='utf-8') as readme_file:
    readme = readme_file.read()


def get_version(*file_paths):
    """Retrieves the version from project/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


class PostDevelopCommand(develop):
    """Post-installation for development mode."""

    def run(self):
        subprocess.check_call(['pipenv', 'install', '--dev', '--deploy', '--system'])
        develop.run(self)


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        subprocess.check_call(['pipenv', 'install', '--deploy', '--system'])
        install.run(self)


class TestCommand(test):
    """Run tests"""

    def run(self):
        subprocess.check_call(['pytest'])
        test.run(self)


setup(
    name='eeee',
    version=get_version('eeee', '__init__.py'),
    description='Extremely Ease Event Emitter. Pub-Sub implementation.',
    long_description=readme,
    author='Paweł Zadrożny',
    author_email='pawel.zny@gmail.com',
    url='https://github.com/pawelzny/eeee',
    packages=find_packages(exclude=('bin', 'docs')),
    package_dir={'eeee': 'eeee'},
    include_package_data=True,
    use_scm_version=True,
    install_requires=['setuptools_scm'],
    zip_safe=False,
    keywords='eeee, event, emitter, signals',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Framework :: Tornado',
        'License :: Other/Proprietary License',
    ],
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
        'test': TestCommand,
    },
)
