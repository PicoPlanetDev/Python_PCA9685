# build
build:
	echo "Building..."
	rm -rf ./dist
	python3 -m build

# upload
upload:
	echo "Uploading..."
	python3 -m twine upload dist/*