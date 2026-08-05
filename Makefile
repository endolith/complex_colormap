VERSION=$(shell python3 -c "import complex_colormap; print(complex_colormap.__version__)")

.PHONY: default tag upload publish clean test

default:
	@echo "\"make publish\"?"

tag:
	# Make sure we're on the master branch
	@if [ "$(shell git rev-parse --abbrev-ref HEAD)" != "master" ]; then exit 1; fi
	@echo "Tagging v$(VERSION)..."
	git tag v$(VERSION)
	git push --tags

upload: tag
	@if [ "$(shell git rev-parse --abbrev-ref HEAD)" != "master" ]; then exit 1; fi
	python3 -m pip install build
	rm -rf dist
	python3 -m build
	gpg --detach-sign -a dist/*
	twine upload dist/*

publish: tag upload

test:
	python3 -m pip install -e .[test]
	pytest

clean:
	rm -rf dist build *.egg-info
