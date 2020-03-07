.PHONY: process-data-files
process-data-files:
	python unicode-data/read_property_file.py

.PHONY: build-release
build-release:
	rm dist/*
	python setup.py sdist

.PHONY: release-to-test
release-to-test:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: release-to-prod
release-to-prod:
	twine upload dist/*
