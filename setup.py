# For now, the intention of this file is merely Resolve issues with imports in tests
# https://docs.pytest.org/en/6.2.x/goodpractices.html#install-package-with-pip
from setuptools import setup, find_packages

setup(name="parser", packages=find_packages())
