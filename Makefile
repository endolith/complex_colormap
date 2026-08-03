VERSION=$(shell python3 -c "import complex_colormap; print(complex_colormap.__version__)")

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
	rm -rf dist
	python3 -m build
	gpg --detach-sign -a dist/*
	twine upload dist/*

publish: tag upload

clean:
	rm -rf dist build *.egg-info
