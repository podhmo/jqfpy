QJ = python -m jqfpy -S

default: 00 01

00:
	${QJ} 00log.ltsv > .qj.output0
	diff -u 00expected.json .qj.output0

01:
	${QJ} 01log.ltsv > .qj.output1
	diff -u 01expected.json .qj.output1
