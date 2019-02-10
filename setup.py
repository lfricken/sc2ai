import setuptools

setuptools.setup(
	name='sc2ai',
	version='0.1dev',
	long_description=open('README.md').read(),
	install_requires=['tensorflow', 'tensorboard', 'sc2', 'sc2reader', 'numpy', 'pandas'],
	packages=setuptools.find_packages()
)