.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help

SHELL := /bin/bash  # The default /bin/sh shell does not implement source.

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

ACTIVATE_VENV := source .dev_venv/bin/activate

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

dev-env:  ## Builds the development environment
	dev/setup.sh

clean: clean-build clean-pyc clean-coverage ## remove all build, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-coverage: ## remove and coverage artifacts
	rm -f .coverage
	rm -fr htmlcov/

test: ## run tests quickly with the default Python
	${ACTIVATE_VENV} && tox

coverage: ## check code coverage quickly with the default Python
	${ACTIVATE_VENV} && PYTHONPATH=src coverage run -m unittest discover tests
	${ACTIVATE_VENV} && coverage report -m
	${ACTIVATE_VENV} && coverage html
	$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/texas_holdem.rst
	rm -f docs/modules.rst
	${ACTIVATE_VENV} && sphinx-apidoc -o docs/ src/texas_holdem
	${ACTIVATE_VENV} && $(MAKE) -C docs clean
	${ACTIVATE_VENV} && $(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

