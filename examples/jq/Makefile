QJ = python -m jqfpy

# see: https://stedolan.github.io/jq/tutorial/
jq: 00 01 02 03 04 05

jq.tutorial.json:
	curl 'https://api.github.com/repos/stedolan/jq/commits?per_page=5' -o $@

# jq '.'
00: jq.tutorial.json
	cat $< | ${QJ} 'get()'

# jq '.[0]'
01: jq.tutorial.json
	cat $< | ${QJ} 'get()[0]'

# jq '.[0] | {message: .commit.message, name: .commit.committer.name}'
02: jq.tutorial.json
	cat $< | ${QJ} 'd = get()[0]; {"message": get("commit/message", d), "name": get("commit/committer/name", d)}'
	cat $< | ${QJ} '{"message": get("0/commit/message"), "name": get("0/commit/committer/name")}'

# jq '.[] | {message: .commit.message, name: .commit.committer.name}'
03: jq.tutorial.json
	cat $< | ${QJ} --squash 'L = get(); [{"message": get("commit/message", d), "name": get("commit/committer/name", d)} for d in L]'

# jq '[.[] | {message: .commit.message, name: .commit.committer.name}]'
04: jq.tutorial.json
	cat $< | ${QJ} 'L = get(); [{"message": get("commit/message", d), "name": get("commit/committer/name", d)} for d in L]'

# jq '[.[] | {message: .commit.message, name: .commit.committer.name, parents: [.parents[].html_url]}]'
05: jq.tutorial.json
	cat $< | ${QJ} 'L = get(); [{"message": get("commit/message", d), "name": get("commit/committer/name", d), "parents": [p["html_url"] for p in d["parents"]]} for d in L]'
