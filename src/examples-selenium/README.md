# examples-selenium

Selenium programing example.

[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)

> Selenium is an umbrella project for a range of tools and libraries that enable and support the automation of web browsers.

## References

- https://www.selenium.dev/ja/documentation/
- https://github.com/seleniumhq-community/docker-seleniarm
- https://github.com/SeleniumHQ/seleniumhq.github.io/tree/trunk/examples/python/tests

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
cd src/examples-selenium

# select interpreter
pdm use

# install dependencies and self.
pdm install

```

## Install headless browsers and Web drivers

### Chromium

- https://chromedriver.chromium.org/downloads

For linux/aarch64.

```shell
sudo apt install chromium chromium-driver
```

in `/usr/bin/chromedriver`

### Firefox

- https://github.com/mozilla/geckodriver/releases

For linux/aarch64 with webdriver-manager.

```shell
sudo apt install firefox-esr
```

## Create project

This project was generated with the command:

```shell
mkdir -p src/examples-selenium
cd src/examples-selenium

# create new pyproject.toml
pdm init
pdm add -d flake8 mypy black isort pytest-cov

pdm add selenium
pdm add webdriver-manager

```
