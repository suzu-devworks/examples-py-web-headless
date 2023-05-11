# examples playwright

Playwright is a framework for Web Testing and Automation. It allows testing Chromium, Firefox and WebKit with a single API

## References

- https://playwright.dev/python/
- https://github.com/microsoft/playwright-python


## Setups

```shell
clone https://github.com/suzu-devworks/examples-py-web-uitesting.git

cd examples-py-web-uitesting
cd src/examples-playweight

pdm use
pdm install

```


## Create projects

```shell
# create virtual environment
python -m venv .venv 
. .venv/bin/activate

# upgrade base packages.
python -m pip install --upgrade pip
python -m pip install --upgrade setuptools

# add Package manager(PDM).
pip install pdm

mkdir -p src/examples-playweight
cd src/examples-playweight

# create new pyproject.toml
pdm init
pdm add -d flake8 mypy black isort pytest-cov

# install playwright
pdm add pytest-playwright
playwright install
playwright install-deps

```
