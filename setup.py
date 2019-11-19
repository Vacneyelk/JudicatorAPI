from setuptools import setup

requirements = []
with open('requirements.txt') as f:
	requirements = f.read().splitlines()

setup(
	name='judicatorAPI',
	author='Vacneyelk',
	url='https://github.com/Vacneyelk/JudicatorAPI',
	version='0.1a',
	packages=['judicatorAPI'],
	license='MIT',
	description='Python wrapper for Riot Games League of Legends API',
	install_requires=requirements,
	python_requries='>=3.6'
)
