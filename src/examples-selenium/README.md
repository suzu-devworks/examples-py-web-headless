# examples selenium


## References

- https://www.selenium.dev/ja/documentation/
- https://github.com/seleniumhq-community/docker-seleniarm
- https://github.com/SeleniumHQ/seleniumhq.github.io/tree/trunk/examples/python/tests



## Setups

```shell
clone https://github.com/suzu-devworks/examples-py-web-uitesting.git

cd examples-py-web-uitesting
cd src/examples-selenium

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

mkdir -p src/examples-selenium
cd src/examples-selenium

# create new pyproject.toml
pdm init
pdm add -d flake8 mypy black isort pytest-cov

# install selenium
pdm add selenium
pdm add webdriver-manager

```
