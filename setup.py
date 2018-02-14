from setuptools import setup, find_packages

import os

# Put here required packages
packages = ['Django==1.11.5',
            'djangorestframework',  # was 3.6.4
            'django-filter',  # was 1.0.4
            'Markdown',
            'mysqlclient',  # python3 fork of MySQL-python
            'requests',
            'plotly',  # was 2.0.15
            'pandas',
            ]

if 'REDISCLOUD_URL' in os.environ and 'REDISCLOUD_PORT' in os.environ and 'REDISCLOUD_PASSWORD' in os.environ:
    packages.append('django-redis-cache')
    packages.append('hiredis')

setup(name='MantidErrorReports',
      version='1.2',
      description='RESTful services related to mantid error reporting',
      author='',
      author_email='',
      url='',
      install_requires=packages,
      packages=find_packages(),
      include_package_data=True,
      )
