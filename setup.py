from setuptools import setup
from setuptools import find_packages


setup(name='rtk',
      version="0.0.6",
      description='RTK',
      author_email='mark@douthwaite.io',
      packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
      )

