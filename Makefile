.PHONY: process-data-files
process-data-files:
	python unicode-data/read_property_file.py

.PHONY: build-release
build-release:
	python setup.py sdist
