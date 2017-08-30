QJ = python -m jqfpy

# json pointer
00:
	${QJ} 'get("paths/~1api~1foo")' 00data.json
	${QJ} 'get("paths/~0api~0bar")' 00data.json

# --slurp, --unbuffered
01:
	rm 	-f .jq.output* .qj.output*
	@echo "--one file----------------------------------------"
	@jq . -M -S -c 01data.json > .jq.output
	@${QJ} -S -c 'get()' 01data.json | sed 's/\([:,]\) /\1/g' > .qj.output
	diff -u .jq.output .qj.output

	@echo "--two files----------------------------------------"
	@jq -M -S -c . 01data.json 01data.json > .jq.output
	@${QJ} -S -c 'get()' 01data.json 01data.json | sed 's/\([:,]\) /\1/g' > .qj.output
	diff -u .jq.output .qj.output

	@echo "--one file slurp----------------------------------------"
	@jq . -M -S --slurp 01data.json > .jq.output
	@${QJ} -S --slurp 'get()' 01data.json > .qj.output
	diff -u .jq.output .qj.output
