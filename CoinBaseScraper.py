from DataScraper import DataScraper
from Coin import Coin
from bs4 import BeautifulSoup
from selenium import webdriver
import concurrent.futures
import time
from selenium.webdriver.common.by import By
class CoinBaseScraper(DataScraper):
    def __init__(self):
        super().__init__(10)
        self.link = 'https://www.coinbase.com/explore'


    def provideLinkForGivenPage(self, pageNumber):
        return self.link + f'?page={pageNumber}'

    def pickCurrency(self, driver):
        cokkiesClick = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div/button[2]')
        if cokkiesClick is not None:
            cokkiesClick.click()
        time.sleep(2)
        currencyDropdownButton = driver.find_element(By.XPATH, '//*[@id="asset-page-currency-selector"]/div/div/button')
        currencyDropdownButton.click()
        time.sleep(2)
        currencyButton = driver.find_element(By.XPATH, '//*[@id="search-dropdown-option-139"]')
        currencyButton.click()
        time.sleep(5)
        return driver

    def scrapeOnePage(self, pageNumber, dataCoin):
        soupCoinBase = self.createSoup(self.provideLinkForGivenPage(pageNumber))
        offers = soupCoinBase.find_all('tr', class_='cds-tableRow-t45thuk cds-tableRowHover-t9ma3wv')


        for offer in offers:
            infos = offer.find_all("td", class_='cds-tableCell-t1jg7jzg')

            coinName = infos[0].find('div', class_ = 'cds-flex-f1g67tkn cds-flex-start-f1urtf06 cds-cell cds-baseStyles-b11jkhgs').find('h2', class_ = 'cds-typographyResets-t1xhpuq2 cds-headline-hb7l4gg cds-foreground-f1yzxzgu cds-transition-txjiwsi cds-start-s1muvu8a').text
            # coinAbbreviation = infos[0].find('div', class_ = 'cds-flex-f1g67tkn cds-flex-start-f1urtf06 cds-cell cds-baseStyles-b11jkhgs').find('p', class_ = 'cds-typographyResets-t1xhpuq2 cds-label2-l5adacs cds-foregroundMuted-f1vw1sy6 cds-transition-txjiwsi cds-start-s1muvu8a cds-truncate-t1dtku18').text

            coinPrice = infos[1].find('div', class_ = 'cds-flex-f1g67tkn cds-flex-end-f9tvb5a cds-column-ci8mx7v cds-flex-start-f1urtf06').text
            coinPrice = float(coinPrice.replace(',', '').replace('$', ''))

            newCoin = Coin(coinName, coinPrice, "CoinBase")
            dataCoin.append(newCoin)

