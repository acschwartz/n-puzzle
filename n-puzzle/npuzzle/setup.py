#!/usr/bin/env python3

#!/usr/bin/env python3

# FROM: https://levelup.gitconnected.com/import-your-own-python-code-without-pythonpath-tricks-9068495c1bba

from setuptools import setup, find_packages
# List of requirements
requirements = []  # This could be retrieved from requirements.txt
# (i don't have any right now)

# Package (minimal) configuration
setup(
	name="npuzzle",	#pnuzzle lol
	version="1.0.0",
	description="n-puzzle solver",
	packages=find_packages(),  # __init__.py folders search
	install_requires=requirements
)