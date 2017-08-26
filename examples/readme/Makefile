default: jq py

jq:
	cat data.json | jq -r '.apps | . as $$o | keys | map(select($$o[.].use))'

py:
	cat data.json | jqfpy '[k for k, opts in get("apps").items() if opts["use"]]'

