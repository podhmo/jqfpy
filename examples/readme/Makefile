default: jq py

default: 00 01

00:
	cat data.json | jq '.apps | . as $$o | keys | map(select($$o[.].use))'
	cat data.json | jqfpy '[k for k, opts in get("apps").items() if opts["use"]]'

01:
	cat data.json | jq -r '.apps | . as $$o | keys | map(select($$o[.].use)) | sort_by(.) | .[]'
	cat data.json | jqfpy --squash -r 'L = get("apps"); ks = [k for k, opts in L.items() if opts["use"]]; sorted(ks)'

