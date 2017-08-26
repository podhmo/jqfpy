QJ = python -m jqfpy

jq: jq.tutorial.json
	# see: https://stedolan.github.io/jq/tutorial/

	# jq '.'
	cat $< | ${QJ} 'get()'

	# jq '.[0]'
	cat $< | ${QJ} 'get()[0]'

	# jq '.[0] | {message: .commit.message, name: .commit.committer.name}'
	cat $< | ${QJ} 'd = get()[0]; {"message": get("commit/message", d), "name": get("commit/committer/name", d)}'
	cat $< | ${QJ} '{"message": get("0/commit/message"), "name": get("0/commit/committer/name")}'

	# jq '.[] | {message: .commit.message, name: .commit.committer.name}'
	cat $< | ${QJ} --squash 'L = get(); [{"message": get("commit/message", d), "name": get("commit/committer/name", d)} for d in L]'

	# jq '[.[] | {message: .commit.message, name: .commit.committer.name}]'
	cat $< | ${QJ} 'L = get(); [{"message": get("commit/message", d), "name": get("commit/committer/name", d)} for d in L]'

	# jq '[.[] | {message: .commit.message, name: .commit.committer.name, parents: [.parents[].html_url]}]'
	cat $< | ${QJ} 'L = get(); [{"message": get("commit/message", d), "name": get("commit/committer/name", d), "parents": [p["html_url"] for p in d["parents"]]} for d in L]'

jq.tutorial.json:
	curl 'https://api.github.com/repos/stedolan/jq/commits?per_page=5' -o $@
