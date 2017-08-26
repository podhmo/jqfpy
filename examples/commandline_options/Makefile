QJ = python -m jqfpy

default: 00 01

00:
	echo --compact-output
	cat 00data.json | ${QJ} 'get()'
	cat 00data.json | ${QJ} -c 'get()'

01:
	echo --slurp-input
	cat 01data.json | ${QJ} -s 'get()'
