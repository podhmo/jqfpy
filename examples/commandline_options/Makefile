QJ = python -m jqfpy

default: 00 01 02 03 04 05

dst:
	mkdir -p dst

00: dst
	echo --compact-output
	cat 00data.json | ${QJ} 'get()' 2>&1 > dst/000.json
	cat 00data.json | ${QJ} -c 'get()' 2>&1 > dst/001.json

01: dst
	echo --slurp-input
	cat 01data.json | ${QJ} -s 'get()' 2>&1 > dst/01.json

02: dst
	echo --sort-keys
	cat 02data.json | ${QJ} -c 'get()' 2>&1 > dst/020.json
	cat 02data.json | ${QJ} -c -S 'get()'  2>&1 > dst/021.json

03: dst
	echo --ascii-output
	cat 03data.json | ${QJ}  'get()'  2>&1 > dst/030.json
	cat 03data.json | ${QJ} -a 'get()'  2>&1 > dst/031.json

04: dst
	echo --raw-output
	cat 03data.json | ${QJ}  'get("en")'  2>&1 > dst/040.json
	cat 03data.json | ${QJ} -r 'get("en")'  2>&1 > dst/041.json
	cat 04data.json | ${QJ} --squash  2>&1 > dst/042.json
	cat 04data.json | ${QJ} --squash -r  2>&1 > dst/043.json

05: dst
	cat 05data.json | ${QJ} -r  2>&1 > dst/050.json
	cat 05data.json | ${QJ} -r --squash  2>&1 > dst/051.json
	cat 05data.json | ${QJ} -r --squash --squash  2>&1 > dst/052.json
