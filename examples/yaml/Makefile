QJ = python -m jqfpy -S

default: 00 01 02 03 04 05

00:
	${QJ} 00data.yaml > .qj.output0
	diff -u 00expected.json .qj.output0

01:
	${QJ} 'get("person/skills")' 00data.yaml  > .qj.output10
	diff -u 010expected.json .qj.output10
	${QJ} --squash -r 'get("person/skills")' 00data.yaml > .qj.output11
	diff -u 011expected.json .qj.output11

02:
	${QJ} -r 'get("name")' 02data.yaml > .qj.output2
	diff -u 02expected.json .qj.output2

03:
	# compact
	${QJ} -r -c -o yaml 'get()' 02data.yaml > .qj.output30
	diff -u 03expected.json .qj.output30

04:
	# ascii-output
	${QJ} -r -a -o yaml 'get()' 04data.yaml > .qj.output40
	diff -u 040expected.yaml .qj.output40
	${QJ} -r -o yaml 'get()' 04data.yaml > .qj.output41
	diff -u 041expected.yaml .qj.output41

05:
	# include hash (#24)
	${QJ} -o yaml 05data.yaml > .qj.output50
	diff -u 050expected.yaml .qj.output50
