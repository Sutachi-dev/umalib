from setuptools import setup, find_packages

def requirements_from_file(file_name):
    return open(file_name).read().splitlines()

setup(
    name='umalib',
    version='0.1',
    description="This module is a common library for umapyoi",
    url="https://github.com/k158124456/umalib",
    packages=find_packages(),
    install_requires=requirements_from_file('requirements.txt'),
)