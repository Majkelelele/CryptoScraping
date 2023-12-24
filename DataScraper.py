from abc import abstractmethod
import concurrent.futures
import time

from bs4 import BeautifulSoup
from selenium import webdriver


class DataScraper:
    def __init__(self, maxPage):
        self.maxPage = maxPage

    def addOptions(self, options):
        # options.add_argument("--headless")
        # options.add_argument(
        #     "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
        #     " Chrome/93.0.4577.63 Safari/537.36")
        # options.addArgument("--start-maximized")
        return options

    def createSoup(self, link):
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=self.addOptions(options))
        driver.get(link)
        driver.maximize_window()
        time.sleep(5)
        driver = self.pickCurrency(driver)

        html = driver.page_source
        driver.quit()
        return BeautifulSoup(html, 'lxml')
    @abstractmethod
    def provideLinkForGivenPage(self, pageNumber):
        pass
    @abstractmethod
    def scrapeOnePage(self, pageNumber, dataCoinBinance):
        pass

    def scrapeGivenPages(self, minPage, maxPage):
        data = []
        # for i in range(minPage,maxPage+1):
        #     self.scrapeOnePage(i,data)
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(self.scrapeOnePage, page, data) for page in range(minPage, maxPage + 1)]
            concurrent.futures.wait(futures)

        return data
    def scrapeAllPages(self):
        return self.scrapeGivenPages(1,self.maxPage)
    @abstractmethod
    def pickCurrency(self, driver):
        pass