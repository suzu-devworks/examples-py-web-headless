# examples-playweight

Microsoft Playwright programing example.

[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)

> Playwright is a framework for Web Testing and Automation. It allows testing Chromium, Firefox and WebKit with a single API

## References

- https://playwright.dev/python/
- https://github.com/microsoft/playwright-python

## Setup

Clone the repository:

```shell
clone https://github.com/suzu-devworks/examples-py-web-headless.git

cd examples-py-web-headless

```

Create a virtualenv in advance:

```shell
python -m venv .venv
. .venv/bin/activate

python -m pip install --upgrade pip
pip install pdm

```

Here's how this project is setup:

```shell
cd src/examples-playweight

# select interpreter
pdm use

# install dependencies and self.
pdm install

```

## Install headless browsers

```shell
# browsers.
playwright install

# dependencies.
playwright install-deps
```

## Create project

This project was generated with the command:

```shell
mkdir -p src/examples-playweight
cd src/examples-playweight

# create new pyproject.toml
pdm init
pdm add -d flake8 mypy black isort pytest-cov

pdm add pytest-playwright

```
