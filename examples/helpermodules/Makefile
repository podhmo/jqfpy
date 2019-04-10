default: 00 01

TEE ?= | tee 
dst:
	mkdir -p dst

# h.dumpfile
00: dst
	rm -rf dst/00 && mkdir dst/00
	# dumpfile
	jqfpy '[h.dumpfile("dst/00/"+k, v) for k,v in get().items()]' src/00*/data.json
	# dumpfile(yaml)
	jqfpy '[h.dumpfile("dst/00/"+k.replace(".json",".yaml"), v) for k,v in get().items()]' src/00*/data.json
	# dumpfile with --relative-path
	jqfpy --relative-path '[h.dumpfile("../../dst/00/"+k, v) for k,v in get().items()]' src/00*/data.json
	# dumpfile with --here
	jqfpy --here=dst/00 '[h.dumpfile(k, v) for k,v in get().items()]' src/00*/data.json
	test -f dst/00/a.json
	test ! -f a.json

# h.pick
01: dst
	rm -rf dst/01 && mkdir dst/01
	cat src/01*/data.json | jqfpy ${TEE} dst/01/input.json
	cat src/01*/data.json | jqfpy 'h.pick("person/name", "person/age")' ${TEE} dst/01/pick.json
	cat src/01*/data.json | jqfpy 'h.pick("person/name@name", "person/age@age")' ${TEE} dst/01/unwrap.json
	cat src/01*/data.json | jqfpy 'h.pick("name", "age", d=get("person"))' ${TEE} dst/01/unwrap2.json
