QJ = python -m jqfpy

defaut: 00 01

# json pointer
00:
	rm 	-f .jq.output0 .qj.output0
	@${QJ} -S 'get("paths/~1api~1foo")' 00data.json > .qj.output0
	@jq -S '.paths."/api/foo"' 00data.json > .jq.output0
	diff -u .jq.output0 .qj.output0
	@${QJ} 'get("paths/~0api~0bar")' 00data.json > .qj.output0
	@jq -S '.paths."~api~bar"' 00data.json > .jq.output0
	diff -u .jq.output0 .qj.output0

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

	@echo "--two files and stdin----------------------------------------"
	@cat 01data.json | jq -M -S -c . 01data.json 01data.json > .jq.output
	@cat 01data.json | ${QJ} -S -c 'get()' 01data.json 01data.json | sed 's/\([:,]\) /\1/g' > .qj.output
	diff -u .jq.output .qj.output

	@echo "--one file slurp----------------------------------------"
	@jq . -M -S --slurp 'sort_by(.age)' 01data.json > .jq.output
	@${QJ} -S --slurp 'sorted(get(), key=lambda x: int(x["age"]))' 01data.json > .qj.output
	diff -u .jq.output .qj.output

	@echo "--two files slurp----------------------------------------"
	@jq -M -S --slurp 'sort_by(.age)' 01data.json 01data.json > .jq.output
	@${QJ} -S --slurp 'sorted(get(), key=lambda x: int(x["age"]))' 01data.json 01data.json > .qj.output
	diff -u .jq.output .qj.output

# buffered
02:
	@echo "--buffered----------------------------------------"
	(python gen.py | jq . | cat ) > .jq.output 2>&1
