from DataScraper import DataScraper
from Coin import Coin
import concurrent.futures
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
class BinanceScraper(DataScraper):
    def __init__(self):
        super().__init__(10)
        self.link = 'https://www.binance.com/en/markets/overview'


    def pickCurrency(self, driver):
        if driver.find_elements(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'):
            cookiesButton = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
            cookiesButton.click()
            time.sleep(2)
        # clicking currency menu
        # driver.find_element(By.XPATH, '//*[@id="__APP_HEADER"]/div/header/div[2]/div[3]').click()
        # time.sleep(2)
        # # USD option
        # driver.find_element(By.XPATH, '//*[@id="__APP_HEADER"]/div/header/div[2]/div[3]/div[2]/div/div/div[2]/div/div[3]/div[4]')
        # time.sleep(5)
        return driver
    def provideLinkForGivenPage(self, pageNumber):
        return self.link + f'?p={pageNumber}'
    def scrapeOnePage(self, pageNumber, dataCoinBinance):

        soupBinance = self.createSoup(self.provideLinkForGivenPage(pageNumber))
        offers = soupBinance.findAll('div', class_='css-vlibs4')

        for offer in offers:
            coinName = offer.find('div', class_ = 'body3 line-clamp-1 truncate text-t-third css-vurnku').text
            coinPrice = offer.find('div', class_='body2 items-center css-18yakpx').text
            coinPrice =  float(coinPrice.replace("$", "").replace(",", ""))
            # coinAbbreviation = offer.find('div', class_ = 'subtitle3 text-t-primary css-vurnku')
            newCoin = Coin(coinName, coinPrice,"Binance")
            dataCoinBinance.append(newCoin)
