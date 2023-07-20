from setuptools import setup, find_packages

def requirements_from_file(file_name):
    try:
        with open(file_name) as f:
            return f.read().splitlines()
    except FileNotFoundError:
        print(f"Error: {file_name} not found.")
        return []

setup(
    name='umalib',
    version='0.1',
    description="This module is a common library for umapyoi",
    url="https://github.com/k158124456/umalib",
    packages=find_packages(),
    install_requires=requirements_from_file('requirements.txt'),
)