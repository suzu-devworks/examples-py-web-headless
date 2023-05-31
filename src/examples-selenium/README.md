# examples selenium


## References

- https://www.selenium.dev/ja/documentation/
- https://github.com/seleniumhq-community/docker-seleniarm
- https://github.com/SeleniumHQ/seleniumhq.github.io/tree/trunk/examples/python/tests



## Setups

```shell
clone https://github.com/suzu-devworks/examples-py-web-headless.git

cd examples-py-web-headless
cd src/examples-selenium

pdm use
pdm install

```


## Install browsers and Web drivers

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
