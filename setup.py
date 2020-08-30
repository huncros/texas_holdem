#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
  readme = readme_file.read()

with open('src/texas_holdem/__version__.py') as version_file:
  exec(version_file.read())  # Sets the version variable as defined in the version file.

requirements = []

setup_requirements = []

setup(
    author="David Herskovics",
    author_email='huncros@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Calculates your chances when playing Texas Hold'em poker.",
    entry_points={
        'console_scripts': [
            'texas_holdem=texas_holdem.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords='texas holdem poker',
    name='texas_holdem',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    setup_requires=setup_requirements,
    url='https://github.com/huncros/texas_holdem',
    version=version,
    zip_safe=False,
)
