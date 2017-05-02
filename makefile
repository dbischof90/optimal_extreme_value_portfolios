install:
	pip3 install -r requirements.txt

run-reference:
	python3 -m samples.reference

help:
	@echo "		install"
	@echo "			installs all needed dependencies with pip."
	@echo "		run-reference"
	@echo "			runs a reference implementation of the provided library"
