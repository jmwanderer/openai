.PHONY: test
test: unittest systest 

.PHONY: systest
systest:
	PYTHONPATH=. pytest

.PHONY: unittest
unittest:
	python3 -m unittest hangman/hangman_test.py

.PHONY: build
build:
	python3 -m build  --wheel


