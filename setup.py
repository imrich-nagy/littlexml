from setuptools import setup

setup(
    name='littlexml',
    packages=['littlexml'],
    entry_points={
        'console_scripts': ['littlexml = littlexml.__main__:parse_args'],
    },
)
