import os

from setuptools import setup


def find_binaries():
    bin_dir = os.path.join(os.path.dirname(__file__), 'bin')
    return [os.path.join(bin_dir, x) for x in os.listdir(bin_dir)]


setup(
    name='bitket',
    version='1.0.0',
    packages=['bitket'],
    scripts=find_binaries(),
    url='https://github.com/ovidner/bitket',
    license='MIT',
    author='Olle Vidner',
    author_email='olle@vidner.se',
    description=''
)
