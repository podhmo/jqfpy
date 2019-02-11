default: 00 01 02 03 04
TEE ?= | tee
dst:
	mkdir -p dst

00: dst
	cat data.json | jq '.apps | . as $$o | keys | map(select($$o[.].use))' ${TEE} dst/000.json
	cat data.json | jqfpy '[k for k, opts in get("apps").items() if opts["use"]]' ${TEE} dst/001.json

01: dst
	cat data.json | jq -r '.apps | . as $$o | keys | map(select($$o[.].use)) | sort_by(.) | .[]' ${TEE} dst/010.json
	cat data.json | jqfpy --squash -r 'L = get("apps"); ks = [k for k, opts in L.items() if opts["use"]]; sorted(ks)' ${TEE} dst/011.json

02: dst
	cat 02data.yaml | jqfpy -i yaml 'get("person")' ${TEE} dst/020.json
	cat 02data.yaml | jqfpy -i yaml -o ltsv 'get("person")'  ${TEE} dst/021.json

03: dst
	cat 02data.yaml | jqfpy -i yaml 'h.pick("person/name", "person/age")'  ${TEE} dst/030.json
	cat 02data.yaml | jqfpy -i yaml 'h.pick("person/name@name", "person/age@age")'  ${TEE} dst/031.json

04: dst
	cat 02data.yaml | jqfpy -i yaml 'h.omit("person/nickname")' ${TEE} dst/04.json

