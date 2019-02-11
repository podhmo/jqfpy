QJ = python -m jqfpy -S
TEE ?= 2>&1 | tee
defaut: 00 01 02 03

dst:
	mkdir -p dst/qj dst/jq dst/diff

# json pointer
00: dst
	${QJ} -S 'get("paths/~1api~1foo")' 00data.json ${TEE} dst/qj/000.output
	jq -S '.paths."/api/foo"' 00data.json ${TEE} dst/jq/000.output
	diff -u dst/jq/000.output dst/qj/000.output ${TEE} dst/diff/000.diff
	test -z `cat dst/diff/000.diff`

	${QJ} 'get("paths/~0api~0bar")' 00data.json ${TEE} dst/qj/001.output
	jq -S '.paths."~api~bar"' 00data.json ${TEE} dst/jq/001.output
	diff -u dst/jq/001.output dst/qj/001.output ${TEE} dst/diff/001.diff
	test -z `cat dst/diff/001.diff`

# --slurp
01: dst
	@echo "--one file----------------------------------------"
	jq . -M -S -c 01data.json ${TEE} dst/jq/010.output
	${QJ} -S -c 'get()' 01data.json | sed 's/\([: dst,]\) /\1/g' ${TEE} dst/qj/010.output
	diff -u dst/jq/010.output dst/qj/010.output ${TEE} dst/diff/010.diff
	test -z `cat dst/diff/010.diff`

	@echo "--two files----------------------------------------"
	jq -M -S -c . 01data.json 01data.json ${TEE} dst/jq/011.output
	${QJ} -S -c 'get()' 01data.json 01data.json | sed 's/\([: dst,]\) /\1/g' ${TEE} dst/qj/011.output
	diff -u dst/jq/011.output dst/qj/011.output ${TEE} dst/diff/011.diff
	test -z `cat dst/diff/011.diff`

	@echo "--two files and stdin----------------------------------------"
	cat 01data.json | jq -M -S -c . 01data.json 01data.json ${TEE} dst/jq/012.output
	cat 01data.json | ${QJ} -S -c 'get()' 01data.json 01data.json | sed 's/\([: dst,]\) /\1/g' ${TEE} dst/qj/012.output
	diff -u dst/jq/012.output dst/qj/012.output ${TEE} dst/diff/012.diff
	test -z `cat dst/diff/012.diff`

	@echo "--one file slurp----------------------------------------"
	jq -M -S --slurp 'sort_by(.age)' 01data.json ${TEE} dst/jq/013.output
	${QJ} -S --slurp 'sorted(get(), key=lambda x: int(x["age"]))' 01data.json ${TEE} dst/qj/013.output
	diff -u dst/jq/013.output dst/qj/013.output ${TEE} dst/diff/013.diff
	test -z `cat dst/diff/013.diff`

	@echo "--two files slurp----------------------------------------"
	jq -M -S --slurp 'sort_by(.age)' 01data.json 01data.json ${TEE} dst/jq/014.output
	${QJ} -S --slurp 'sorted(get(), key=lambda x: int(x["age"]))' 01data.json 01data.json ${TEE} dst/qj/014.output
	diff -u dst/jq/014.output dst/qj/014.output ${TEE} dst/diff/014.diff
	test -z `cat dst/diff/014.diff`

# --buffered, --unbuffered
02: dst
	@echo "--buffered----------------------------------------"
	(python gen.py 2>&1 | jq -S . | cat) ${TEE} dst/jq/020.output
	(python gen.py 2>&1 | ${QJ} --buffered 'get()' | cat) ${TEE} dst/qj/020.output
	diff -u dst/jq/020.output dst/qj/020.output ${TEE} dst/diff/020.diff
	test -z `cat dst/diff/020.diff`

	@echo "--unbuffered----------------------------------------"
	(python gen.py 2>&1 | jq -S . --unbuffered | cat ) ${TEE} dst/jq/021.output
	(python gen.py 2>&1 | ${QJ} --unbuffered 'get()' | cat ) ${TEE} dst/qj/021.output
	diff -u dst/jq/021.output dst/qj/021.output ${TEE} dst/diff/021.diff
	test -z `cat dst/diff/021.diff`

	@echo "--buffered slurp----------------------------------------"
	(python gen.py 2>&1 | jq -S . --slurp | cat ) ${TEE} dst/jq/022.output
	(python gen.py 2>&1 | ${QJ} 'get()' --slurp --buffered | cat ) ${TEE} dst/qj/022.output
	diff -u dst/jq/022.output dst/qj/022.output ${TEE} dst/diff/022.diff
	test -z `cat dst/diff/022.diff`

	@echo "--unbuffered slurp----------------------------------------"
	(python gen.py 2>&1 | jq -S . --slurp --unbuffered | cat ) ${TEE} dst/jq/023.output
	(python gen.py 2>&1 | ${QJ} --unbuffered 'get()' --slurp | cat ) ${TEE} dst/qj/023.output
	diff -u dst/jq/023.output dst/qj/023.output ${TEE} dst/diff/023.diff
	test -z `cat dst/diff/023.diff`

	@echo "--buffered2----------------------------------------"
	(cat 06data.json | jq -S . --slurp | cat ) ${TEE} dst/jq/024.output
	(cat 06data.json | ${QJ} 'get()' --slurp --buffered | cat ) ${TEE} dst/qj/024.output
	diff -u dst/jq/024.output dst/qj/024.output ${TEE} dst/diff/024.diff
	test -z `cat dst/diff/024.diff`

	@echo "--unbuffered2----------------------------------------"
	(cat 06data.json | jq -S . --slurp --unbuffered | cat ) ${TEE} dst/jq/025.output
	(cat 06data.json | ${QJ} --unbuffered 'get()' --slurp | cat ) ${TEE} dst/qj/025.output
	diff -u dst/jq/025.output dst/qj/025.output ${TEE} dst/diff/025.diff
	test -z `cat dst/diff/025.diff`

# broken json
03: dst
	@echo "--broken 1json---------------------------------"
	${QJ} "get()" 03data.json > dst/qj/030.output 2>&1 || exit 0
	test -n "`grep 'JSONDecodeError\|ValueError' dst/qj/030.output`"

	@echo "--broken 2json---------------------------------"
	${QJ} "get()" 04data.json > dst/qj/031.output 2>&1 || exit 0
	test -n "`grep 'JSONDecodeError\|ValueError' dst/qj/031.output`"

	@echo "--broken 2json with slurp ---------------------------------"
	${QJ} --slurp "get()" 04data.json > dst/qj/032.output 2>&1 || exit 0
	test -n "`grep 'JSONDecodeError\|ValueError' dst/qj/032.output`"

	@echo "--no broken---------------------------------"
	${QJ} --slurp "get()" 05data.json > dst/qj/033.output 2>&1 || exit 0
	test -z "`grep 'JSONDecodeError\|ValueError' dst/qj/033.output`"
	rm -rf dst/qj/03*.output
