00:
	cat 00data.json | jqfpy --additionals=./match.py '[d for d in get("constraint") if h.match("^1\..+", d.get("version"))]' > .qj.output00
	diff -u 00expected.json .qj.output00

