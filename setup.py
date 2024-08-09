"""
A setuptools based setup module.
"""
from setuptools import setup, find_packages
import pathlib


here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.markdown').read_text(encoding="utf-8")

setup(
    name='prospector-holds',
    version='0.0.0',
    description='Search the Prospector Library Catalogue',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/stvstnfrd/prospector-holds',
    author='stvstnfrd',
    author_email='stvstnfrd@noreply.users.github.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPLv3 License',
        'Programming Language :: Python :: 3',
    ],
    keywords='information science, library science',
    package_dir={
        '': 'src',
    },
    packages=find_packages(where='src'),
    python_requires=">=3.0, <4",
    install_requires=(
    ),
    extras_require={
        'test': (
            'pylint',
        ),
    },
    package_data={
        'prospector-holds': (
        ),
    },
    entry_points={
        'console_scripts': [
            'prospector-holds=prospector_holds.main:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/stvstnfrd/prospector-holds/issues',
        'Source': 'https://github.com/stvstnfrd/prospector-holds/',
    },
)
