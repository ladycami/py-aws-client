import os
from setuptools import setup
from distutils.command.upload import upload
from distutils.command.register import register


class Register(register):

    @staticmethod
    def _get_rc_file():
        return os.path.join('.', '.pypirc')


class Upload(upload):

    @staticmethod
    def _get_rc_file():
        return os.path.join('.', '.pypirc')


with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

    setup(
        cmdclass={
            'register': register,
            'upload': upload,
        }
    )

