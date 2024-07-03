from selenium import webdriver


class MakeBrowser:
    def __init__(self) -> None:
        self.__browser: webdriver.Chrome
        self.__options = webdriver.ChromeOptions()

    def __enter__(self):
        self.__options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.__options.add_experimental_option("useAutomationExtension", False)
        self.__options.add_argument("--disable-blink-features=AutomationControlled")

        self.__browser = webdriver.Chrome(self.__options)
        return self.__browser

    def __exit__(self, _, __, ___):
        self.__browser.quit()
