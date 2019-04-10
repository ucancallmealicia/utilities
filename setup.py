'''
Look up packaging instructions from Serious Python to see if anything has changed for Python 3
'''

from setuptools import setup

#this should be pretty detailed; generate from function definitions (i.e. Serious Python)
def readme():
	with open('README.rst') as f:
		return f.read()

setup(name='utilities',
	  version='0.1',
	  description='File handling and other frequently used utility functions',
	  long_description=readme(),
	  url='https://github.com/ucancallmealicia/utilities',
      license='MIT',
	  author='Alicia Detelich',
	  author_email='adetelich@gmail.com',
      classifiers=[
          'Development Status : : Alpha',
          'License :: OSI Approved :: MIT License'
          'Programming Language :: Python :: 3.6',
          'Natural Language :: English',
          'Operating System :: OS Independent'
          ],
	  packages=['utilities'],
	  install_requires=['requests', 'paramiko', 'pymysql', 'sshtunnel', 'pandas'],
	  include_package_data=True,
	  zip_safe=False)