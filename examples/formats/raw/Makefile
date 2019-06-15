TEE ?= | tee

default: 00 01 02 03 04

dst:
	mkdir -p dst

00: dst
	cat src/data.txt | jqfpy -i raw ${TEE} dst/$@.output
01: dst
	cat src/data.txt | jqfpy -i raw -r ${TEE} dst/$@.output
02: dst
	cat src/data.txt | jqfpy 'xs = [x.strip() for x in get().split(": dst: dst")]; dict(zip(["name", "age"], xs))' -i raw -r -c ${TEE} dst/$@.output
03: dst
	python -u -c 'import time; [(print(i), time.sleep(0.2)) for i in range(5)]' | jqfpy -i raw ${TEE} dst/$@.output
04: dst
	python -u -c 'import time; [(print(i), time.sleep(0.2)) for i in range(5)]' | jqfpy -i raw -u ${TEE} dst/$@.output

