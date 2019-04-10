default: 00 01 02 03
TEE ?= | tee
dst:
	mkdir -p dst

00: dst := dst/00top
00: dst
	rm	-rf ${dst}; mkdir -p ${dst}
	cat data.json ${TEE} ${dst}/input.json
	cat data.json | jq '.apps | . as $$o | keys | map(select($$o[.].use))' ${TEE} ${dst}/jq.json
	cat data.json | jqfpy '[k for k, opts in get("apps").items() if opts["use"]]' ${TEE} ${dst}/jqfpy.json

01: dst := dst/01top-sorted
01: dst
	rm	-rf ${dst}; mkdir -p ${dst}
	cat data.json ${TEE} ${dst}/input.json
	cat data.json | jq -r '.apps | . as $$o | keys | map(select($$o[.].use)) | sort_by(.) | .[]' ${TEE} ${dst}/jq.json
	cat data.json | jqfpy --squash -r 'L = get("apps"); ks = [k for k, opts in L.items() if opts["use"]]; sorted(ks)' ${TEE} ${dst}/jqfpy.json

02: dst := dst/02other-formats
02: dst
	rm	-rf ${dst}; mkdir -p ${dst}
	cat 02data.yaml | jqfpy -i yaml ${TEE} ${dst}/input.json
	cat 02data.yaml | jqfpy -i yaml -o yaml 'get("person")' ${TEE} ${dst}/person.yaml
	cat 02data.yaml | jqfpy -i yaml -o ltsv 'get("person")' ${TEE} ${dst}/person.ltsv

03: dst := dst/03helper-modules
03: dst
	rm	-rf ${dst}; mkdir -p ${dst}
	cat 02data.yaml | jqfpy -i yaml ${TEE} ${dst}/input.json
	cat 02data.yaml | jqfpy -i yaml 'h.pick("person/name", "person/age")'  ${TEE} ${dst}/h.pick.json
	cat 02data.yaml | jqfpy -i yaml 'h.pick("person/name@name", "person/age@age")'  ${TEE} ${dst}/h.pick.unwrap.json
	cat 02data.yaml | jqfpy -i yaml 'h.omit("person/nickname")' ${TEE} ${dst}/h.omit.json

