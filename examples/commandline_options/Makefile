QJ = python -m jqfpy

default: 00 01 02 03

00:
	echo --compact-output
	cat 00data.json | ${QJ} 'get()'
	cat 00data.json | ${QJ} -c 'get()'

01:
	echo --slurp-input
	cat 01data.json | ${QJ} -s 'get()'

02:
	echo --sort-keys
	cat 02data.json | ${QJ} -c 'get()'
	cat 02data.json | ${QJ} -c -S 'get()'

03:
	echo --ascii-output
	cat 03data.json | ${QJ}  'get()'
	cat 03data.json | ${QJ} -a 'get()'

04:
	echo --raw-output
	cat 03data.json | ${QJ}  'get("en")'
	cat 03data.json | ${QJ} -r 'get("en")'
