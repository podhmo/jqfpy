default: 00 01 02 03 04

dst:
	mkdir -p dst

00: dst
	cat data.json | jq '.apps | . as $$o | keys | map(select($$o[.].use))' 2>&1 > dst/000.json
	cat data.json | jqfpy '[k for k, opts in get("apps").items() if opts["use"]]' 2>&1 > dst/001.json

01: dst
	cat data.json | jq -r '.apps | . as $$o | keys | map(select($$o[.].use)) | sort_by(.) | .[]' 2>&1 > dst/010.json
	cat data.json | jqfpy --squash -r 'L = get("apps"); ks = [k for k, opts in L.items() if opts["use"]]; sorted(ks)' 2>&1 > dst/011.json

02: dst
	cat 02data.yaml | jqfpy -i yaml 'get("person")' 2>&1 > dst/020.json
	cat 02data.yaml | jqfpy -i yaml -o ltsv 'get("person")'  2>&1 > dst/021.json

03: dst
	cat 02data.yaml | jqfpy -i yaml 'h.pick("person/name", "person/age")'  2>&1 > dst/030.json
	cat 02data.yaml | jqfpy -i yaml 'h.pick("person/name@name", "person/age@age")'  2>&1 > dst/031.json

04: dst
	cat 02data.yaml | jqfpy -i yaml 'h.omit("person/nickname")' 2>&1 > dst/04.json

