# integration tests (regression tests)
WHERE ?= .
run:
	$(MAKE) --silent _find-candidates | xargs -n 1 make -C || (echo "**********NG**********" && exit 1)
ci:
	$(MAKE) --silent _find-candidates | xargs -n 1 echo "TEE='2>&1 >' OPTS=--log=WARNING" make --silent -C | bash -x -e || (echo "**********NG**********" && exit 1)
	test -z `git diff examples` || (echo  "*********DIFF*********" && git diff examples && exit 2)
_find-candidates:
	@find ${WHERE} -mindepth 2 -name Makefile | xargs -n 1 -I{} dirname {}

build:
#	pip install wheel
	python setup.py bdist_wheel

upload:
#	pip install twine
	twine check dist/jqfpy-$(shell cat VERSION)*
	twine upload dist/jqfpy-$(shell cat VERSION)*

.PHONY: build upload
