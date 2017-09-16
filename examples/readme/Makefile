default: 00 01 02 03 04

00:
	cat data.json | jq '.apps | . as $$o | keys | map(select($$o[.].use))'
	cat data.json | jqfpy '[k for k, opts in get("apps").items() if opts["use"]]'

01:
	cat data.json | jq -r '.apps | . as $$o | keys | map(select($$o[.].use)) | sort_by(.) | .[]'
	cat data.json | jqfpy --squash -r 'L = get("apps"); ks = [k for k, opts in L.items() if opts["use"]]; sorted(ks)'

02:
	cat 02data.yaml | jqfpy -i yaml 'get("person")'
	cat 02data.yaml | jqfpy -i yaml -o ltsv 'get("person")'

03:
	cat 02data.yaml | jqfpy -i yaml 'h.pick("person/name", "person/age")'
	cat 02data.yaml | jqfpy -i yaml 'h.pick("person/name@name", "person/age@age")'

04:
	cat 02data.yaml | jqfpy -i yaml 'h.omit("person/nickname")'

