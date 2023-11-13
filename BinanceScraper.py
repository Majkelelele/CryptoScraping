from DataScraper import DataScraper
from Coin import Coin
import concurrent.futures
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
class BinanceScraper(DataScraper):
    def __init__(self):
        super().__init__(2)
        self.link = 'https://www.binance.com/en/markets/overview'

    def createSoup(self,link):
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=self.addOptions(options))
        driver.get(link)
        time.sleep(5)
        driver = self.pickCurrency(driver)

        html = driver.page_source
        driver.quit()
        return BeautifulSoup(html, 'lxml')
    def pickCurrency(self, driver):
        cookiesButton = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
        if cookiesButton is not None:
            cookiesButton.click()
        time.sleep(2)
        # # clicking currency menu
        # driver.find_element(By.XPATH, '//*[@id="__APP_HEADER"]/div/header/div[2]/div[3]').click()
        # time.sleep(2)
        # # USD option
        # driver.find_element(By.XPATH, '//*[@id="__APP_HEADER"]/div/header/div[2]/div[3]/div[2]/div/div/div[2]/div/div[3]/div[50]')
        # time.sleep(5)
        return driver
    def provideLinkForGivenPage(self, pageNumber):
        return self.link + f'?p={pageNumber}'
    def scrapeOnePage(self, pageNumber, dataCoinBinance):

        soupBinance = self.createSoup(self.provideLinkForGivenPage(pageNumber))
        offers = soupBinance.findAll('div', class_='css-vlibs4')

        for offer in offers:
            coinName = offer.find_next('div', class_ = 'css-dybhdz').text
            coinPrice = offer.find('div', class_='css-hwo5f4').text
            coinPrice =  float(coinPrice.replace("$", "").replace(",", ""))
            coinAbbreviation = offer.find_next('div', class_ = 'css-12il21h').text
            newCoin = Coin(coinName, coinPrice,"Binance",coinAbbreviation)
            dataCoinBinance.append(newCoin)
