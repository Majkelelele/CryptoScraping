from DataScraper import DataScraper
from Coin import Coin
import concurrent.futures
from bs4 import BeautifulSoup
from selenium import webdriver
class BinanceScraper(DataScraper):
    def __init__(self):
        super().__init__(25)
        self.link = 'https://www.binance.com/en/markets/overview'

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
    def provideLinkForGivenPage(self, pageNumber):
        return self.link + f'?p={pageNumber}'
    def scrapeOnePage(self, pageNumber, dataCoinBinance):

        soupBinance = self.createSoup(self.provideLinkForGivenPage(pageNumber))
        offers = soupBinance.findAll('div', class_='css-vlibs4')

        for offer in offers:
            coinName = offer.find('div', class_='css-uaf1yb').text
            coinPrice = offer.find('div', class_='css-hwo5f4').text
            coinPrice =  float(coinPrice.replace("€", "").replace(",", ""))
            coinAbbreviation = offer.find('div', class_ = 'css-1x8dg53').text
            newCoin = Coin(coinName, coinPrice,"Binance",coinAbbreviation)
            dataCoinBinance.append(newCoin)



    # def scrapeGivenPages(self, minPage, maxPage):
    #     data = []
    #
    #     with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    #         futures = [executor.submit(self.scrapeOnePage, page, data) for page in range(minPage, maxPage + 1)]
    #         concurrent.futures.wait(futures)
    #
    #     return data
