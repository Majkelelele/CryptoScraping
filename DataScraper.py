from bs4 import BeautifulSoup
from selenium import webdriver
from abc import abstractmethod
import concurrent.futures
class DataScraper:
    def __init__(self, maxPage):
        self.maxPage = maxPage

    def createSoup(self,link):
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=self.addOptions(options))
        driver.get(link)
        # Wait for content to load (you might need to adjust the waiting time)
        driver.implicitly_wait(5)
        # Get the page source after JavaScript rendering
        html = driver.page_source
        # Close the driver
        driver.quit()
        return BeautifulSoup(html, 'lxml')

    def addOptions(self, options):
        # options.add_argument("--headless")
        # options.add_argument(
        #     "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
        #     " Chrome/93.0.4577.63 Safari/537.36")
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('--disable-gpu')
        # options.add_argument('--remote-debugging-port=9222')
        return options

    @abstractmethod
    def provideLinkForGivenPage(self, pageNumber):
        pass
    @abstractmethod
    def scrapeOnePage(self, pageNumber, dataCoinBinance):
        pass

    def scrapeGivenPages(self, minPage, maxPage):
        data = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(self.scrapeOnePage, page, data) for page in range(minPage, maxPage + 1)]
            concurrent.futures.wait(futures)

        return data
    def scrapeAllPages(self):
        return self.scrapeGivenPages(1,self.maxPage)