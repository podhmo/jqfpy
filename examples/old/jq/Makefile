QJ = python -m jqfpy -S
TEE ?= | tee

# see: https://stedolan.github.io/jq/tutorial/
jq: 00 01 02 03 04 05
TEE ?= | tee
jq.tutorial.json:
	curl 'https://api.github.com/repos/stedolan/jq/commits?per_page=5&until=2019-01-01T00:00:00Z' -o $@

dst:
	mkdir -p dst

# jq '.'
00: jq.tutorial.json dst
	cat $< | ${QJ} 'get()' ${TEE} dst/00.json

# jq '.[0]'
01: jq.tutorial.json dst
	cat $< | ${QJ} 'get()[0]' ${TEE} dst/01.json

# jq '.[0] | {message: .commit.message, name: .commit.committer.name}'
02: jq.tutorial.json dst
	cat $< | ${QJ} 'd = get()[0]; {"message": get("commit/message", d), "name": get("commit/committer/name", d)}' ${TEE} dst/020.json
	cat $< | ${QJ} '{"message": get("0/commit/message"), "name": get("0/commit/committer/name")}'  ${TEE} dst/021.json

# jq '.[] | {message: .commit.message, name: .commit.committer.name}'
03: jq.tutorial.json dst
	cat $< | ${QJ} --squash 'L = get(); [{"message": get("commit/message", d), "name": get("commit/committer/name", d)} for d in L]' ${TEE} dst/03.json

# jq '[.[] | {message: .commit.message, name: .commit.committer.name}]'
04: jq.tutorial.json dst
	cat $< | ${QJ} 'L = get(); [{"message": get("commit/message", d), "name": get("commit/committer/name", d)} for d in L]'  ${TEE} dst/04.json

# jq '[.[] | {message: .commit.message, name: .commit.committer.name, parents: [.parents[].html_url]}]'
05: jq.tutorial.json dst
	cat $< | ${QJ} 'L = get(); [{"message": get("commit/message", d), "name": get("commit/committer/name", d), "parents": [p["html_url"] for p in d["parents"]]} for d in L]' ${TEE} dst/050.json
	cat $< | ${QJ} 'L = get(); [h.pick("commit/message@message", "commit/committer/name@name", "parents[]/html_url@parents", d=d) for d in L]' ${TEE} dst/051.json
