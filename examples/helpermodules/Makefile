default: 00

dst:
	mkdir -p dst

# h.dumpfile
00: dst
	rm -rf dst/00 && mkdir dst/00
	# dumpfile
	jqfpy '[h.dumpfile("dst/00/"+k, v) for k,v in get().items()]' src/00*/data.json
	# dumpfile(yaml)
	jqfpy '[h.dumpfile("dst/00/"+k.replace(".json",".yaml"), v) for k,v in get().items()]' src/00*/data.json
