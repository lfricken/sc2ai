from distutils.core import setup

setup(
	name='sc2ai',
	version='0.1dev',
	packages=['sc2ai',],
	long_description=open('README.md').read(),
	install_requires=['tensorflow', 'tensorboard', 'sc2', 'sc2reader', 'numpy', 'pandas']
)