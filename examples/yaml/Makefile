QJ = python -m jqfpy --format=yaml

default: 00 01

00:
	${QJ} 00data.yaml

01:
	${QJ} 'get("person/skills")' 00data.yaml
	${QJ} --squash 'get("person/skills")' 00data.yaml
