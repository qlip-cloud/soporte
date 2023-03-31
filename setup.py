from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in support_portal/__init__.py
from support_portal import __version__ as version

setup(
	name='support_portal',
	version=version,
	description='Support Portal',
	author='Mentum',
	author_email='camilo.otalora@mentum.group',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
