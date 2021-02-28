#!/bin/bash
# Sets up local development environment.
set xue

cd $(dirname $0)

ROOT_DIR=$(git rev-parse --show-toplevel)
# Set up git hook
pushd $ROOT_DIR/.git/hooks
ln -sf ../../dev/pre-commit pre-commit
popd

# Create python virtual env containing the necessary packages for testing / development
pushd $ROOT_DIR
python -m venv .dev_venv
source .dev_venv/bin/activate
pip install autopep8 coverage tox sphinx
pip install -e .
popd
