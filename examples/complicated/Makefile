QJ = python -m jqfpy -S

defaut: 00 01 02 03

# json pointer
00:
	rm 	-f .jq.output0 .qj.output0
	@${QJ} -S 'get("paths/~1api~1foo")' 00data.json > .qj.output0
	@jq -S '.paths."/api/foo"' 00data.json > .jq.output0
	diff -u .jq.output0 .qj.output0
	@${QJ} 'get("paths/~0api~0bar")' 00data.json > .qj.output0
	@jq -S '.paths."~api~bar"' 00data.json > .jq.output0
	diff -u .jq.output0 .qj.output0

# --slurp
01:
	rm 	-f .jq.output11 .qj.output11
	@echo "--one file----------------------------------------"
	@jq . -M -S -c 01data.json > .jq.output1
	@${QJ} -S -c 'get()' 01data.json | sed 's/\([:,]\) /\1/g' > .qj.output1
	diff -u .jq.output1 .qj.output1

	@echo "--two files----------------------------------------"
	@jq -M -S -c . 01data.json 01data.json > .jq.output1
	@${QJ} -S -c 'get()' 01data.json 01data.json | sed 's/\([:,]\) /\1/g' > .qj.output1
	diff -u .jq.output1 .qj.output1

	@echo "--two files and stdin----------------------------------------"
	@cat 01data.json | jq -M -S -c . 01data.json 01data.json > .jq.output1
	@cat 01data.json | ${QJ} -S -c 'get()' 01data.json 01data.json | sed 's/\([:,]\) /\1/g' > .qj.output1
	diff -u .jq.output1 .qj.output1

	@echo "--one file slurp----------------------------------------"
	@jq -M -S --slurp 'sort_by(.age)' 01data.json > .jq.output1
	@${QJ} -S --slurp 'sorted(get(), key=lambda x: int(x["age"]))' 01data.json > .qj.output1
	diff -u .jq.output1 .qj.output1

	@echo "--two files slurp----------------------------------------"
	@jq -M -S --slurp 'sort_by(.age)' 01data.json 01data.json > .jq.output1
	@${QJ} -S --slurp 'sorted(get(), key=lambda x: int(x["age"]))' 01data.json 01data.json > .qj.output1
	diff -u .jq.output1 .qj.output1

# --buffered, --unbuffered
02:
	rm 	-f .jq.output2* .qj.output2*
	@echo "--buffered----------------------------------------"
	@(python gen.py | jq -S . | cat ) > .jq.output20 2>&1
	@(python gen.py | ${QJ} --buffered 'get()' | cat ) > .qj.output20 2>&1
	diff -u .jq.output20 .qj.output20

	@echo "--unbuffered----------------------------------------"
	@(python gen.py | jq -S . --unbuffered | cat ) > .jq.output21 2>&1
	@(python gen.py | ${QJ} --unbuffered 'get()' | cat ) > .qj.output21 2>&1
	diff -u .jq.output21 .qj.output21

	@echo "--buffered slurp----------------------------------------"
	@(python gen.py | jq -S . --slurp | cat ) > .jq.output22 2>&1
	@(python gen.py | ${QJ} 'get()' --slurp --buffered | cat ) > .qj.output22 2>&1
	diff -u .jq.output22 .qj.output22

	@echo "--unbuffered slurp----------------------------------------"
	@(python gen.py | jq -S . --slurp --unbuffered | cat ) > .jq.output23 2>&1
	@(python gen.py | ${QJ} --unbuffered 'get()' --slurp | cat ) > .qj.output23 2>&1
	diff -u .jq.output23 .qj.output23

	@echo "--buffered2----------------------------------------"
	@(cat 06data.json | jq -S . --slurp | cat ) > .jq.output24 2>&1
	@(cat 06data.json | ${QJ} 'get()' --slurp --buffered | cat ) > .qj.output24 2>&1
	diff -u .jq.output24 .qj.output24

	@echo "--unbuffered2----------------------------------------"
	@(cat 06data.json | jq -S . --slurp --unbuffered | cat ) > .jq.output25 2>&1
	@(cat 06data.json | ${QJ} --unbuffered 'get()' --slurp | cat ) > .qj.output25 2>&1
	diff -u .jq.output25 .qj.output25

# broken json
03:
	@echo "--broken 1json---------------------------------"
	${QJ} "get()" 03data.json > .qj.output30 2>&1 || exit 0
	test -n "`grep 'JSONDecodeError\|ValueError' .qj.output30`"

	@echo "--broken 2json---------------------------------"
	${QJ} "get()" 04data.json > .qj.output31 2>&1 || exit 0
	test -n "`grep 'JSONDecodeError\|ValueError' .qj.output31`"

	@echo "--broken 2json with slurp ---------------------------------"
	${QJ} --slurp "get()" 04data.json > .qj.output32 2>&1 || exit 0
	test -n "`grep 'JSONDecodeError\|ValueError' .qj.output32`"

	@echo "--no broken---------------------------------"
	${QJ} --slurp "get()" 05data.json > .qj.output33 2>&1 || exit 0
	test -z "`grep 'JSONDecodeError\|ValueError' .qj.output33`"
