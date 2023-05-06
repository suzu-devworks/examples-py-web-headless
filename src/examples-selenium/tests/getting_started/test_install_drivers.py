from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType


# @pytest.mark.skip(reason="Do not run in CI")
def test_driver_manager_chrome():
    driver = webdriver.Chrome(
        service=ChromiumService(
            ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
        )
    )

    driver.quit()
