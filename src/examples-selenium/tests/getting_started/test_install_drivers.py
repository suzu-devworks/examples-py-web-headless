import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from webdriver_manager.firefox import GeckoDriverManager

"""
see also.
- [selenium](https://github.com/SeleniumHQ/seleniumhq.github.io/blob/trunk/examples/python/tests/getting_started/test_install_drivers.py)
"""  # noqa E501


@pytest.mark.skip(reason="Do not run in CI")
def test_driver_manager_chrome():
    """
    WebDriverException: Message: Service /home/vscode/.wdm/drivers/chromedriver/linux64/113.0.5672.63/chromedriver unexpectedly exited. Status code was: 255
    """  # noqa E501
    driver = webdriver.Chrome(
        service=ChromiumService(
            ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
        )
    )

    driver.quit()


@pytest.mark.skip(reason="Do not run in CI")
def test_driver_manager_firefox():
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

    driver.quit()
