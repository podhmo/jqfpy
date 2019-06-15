QJ = python -m jqfpy -S

default: 00 01 02 03

00:
	${QJ} 00log.ltsv > .qj.output0
	diff -u 00expected.json .qj.output0

01:
	${QJ} 01log.ltsv > .qj.output1
	diff -u 01expected.json .qj.output1

02:
	${QJ} 'h.pick("host", "status")' 00log.ltsv > .qj.output2
	diff -u 02expected.json .qj.output2

03:
	${QJ} 'h.omit("time", "req", "referer")' 00log.ltsv > .qj.output3
	diff -u 03expected.json .qj.output3
