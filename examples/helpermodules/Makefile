default: 00 01 02 03

TEE ?= | tee 
dst:
	mkdir -p dst

# h.dumpfile
00: dst
	rm -rf dst/00 && mkdir dst/00
	# dumpfile
	jqfpy '[h.dumpfile(v, "dst/00/"+k) for k,v in get().items()]' src/00*/data.json > /dev/null
	# dumpfile(yaml)
	jqfpy '[h.dumpfile(v, "dst/00/"+k.replace(".json",".yaml")) for k,v in get().items()]' src/00*/data.json > /dev/null
	# dumpfile with --relative-path
	jqfpy --relative-path '[h.dumpfile(v, "../../dst/00/"+k) for k,v in get().items()]' src/00*/data.json > /dev/null
	# dumpfile with --here
	jqfpy --here=dst/00 '[h.dumpfile(v, k) for k,v in get().items()]' src/00*/data.json > /dev/null
	test -f dst/00/a.json
	test ! -f a.json

# h.pick
01: dst
	rm -rf dst/01 && mkdir dst/01
	cat src/01*/data.json | jqfpy ${TEE} dst/01/input.json
	cat src/01*/data.json | jqfpy 'h.pick("person/name", "person/age")' ${TEE} dst/01/pick.json
	cat src/01*/data.json | jqfpy 'h.pick("person/name@name", "person/age@age")' ${TEE} dst/01/unwrap.json
	cat src/01*/data.json | jqfpy 'h.pick("name", "age", d=get("person"))' ${TEE} dst/01/unwrap2.json

# h.omit()
02: dst
	rm -rf dst/02 && mkdir dst/02
	cat src/02*/data.json | jqfpy ${TEE} dst/02/input.json
	cat src/02*/data.json | jqfpy 'h.omit("father", "mother")' ${TEE} dst/02/omit.json
	cat src/02*/data.json | jqfpy 'h.omit("father", "mother/nickname")' ${TEE} dst/02/omit.json
	cat src/02*/data.json | jqfpy 'h.omit("nickname", d=get("father"))' ${TEE} dst/02/omit.json

# h.chunk()
03: dst
	rm -rf dst/03 && mkdir dst/03
	cat src/03*/data.json | jqfpy ${TEE} dst/03/input.json
	cat src/03*/data.json | jqfpy 'h.chunk(get("members"), n=5)' ${TEE} dst/03/chunk5.json
	cat src/03*/data.json | jqfpy 'h.chunk(get("members"), n=4)' ${TEE} dst/03/chunk4.json

# h.loadfile()
04: dst
	rm -rf dst/04 && mkdir dst/04
	cat src/04loadfile/main.json | jqfpy --here=src/04loadfile  '{k: h.loadfile(fname) for k, fname in get().items()}' ${TEE} dst/04/stdout.json
# here is cwd  (defaullt)
	jqfpy 'import os.path; {k: h.loadfile(os.path.join("src/04loadfile/", fname)) for k, fname in get().items()}' src/04*/main.json ${TEE} dst/04/default.json
# relative path
	jqfpy --relative-path '{k: h.loadfile(fname) for k, fname in get().items()}' src/04*/main.json ${TEE} dst/04/relative-path.json
