import codecs
import os
import sys

from setuptools import find_packages, setup


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version():
    return read("VERSION")

setup(
    install_requires=[
        "PyYAML",
    ],
    name="encryptor",
    version=get_version(),
    description="Videonetics encryptor Framework",
    author="Monotosh Das",
    author_email="monotosh.das@videonetics.com",
    url="http://pypi.videonetics.com",
    keywords="encryptor",
    classifiers=["License :: OSI Approved :: MIT License"],
    packages=find_packages(),
)
