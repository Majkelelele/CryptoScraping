from DataScraper import DataScraper
from Coin import Coin
from bs4 import BeautifulSoup
from selenium import webdriver
import concurrent.futures
import time
from selenium.webdriver.common.by import By
class CoinBaseScraper(DataScraper):
    def __init__(self):
        super().__init__(15)
        self.link = 'https://www.coinbase.com/explore'
        # self.USDPrice = float(self.findUSDPrice().split()[1])

    def createSoup(self,link):
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=self.addOptions(options))
        driver.get(link)
        # Wait for content to load (you might need to adjust the waiting time)
        driver.implicitly_wait(5)
        currency_dropdown_button = driver.find_element(By.CSS_SELECTOR,
            '#asset-page-currency-selector > div > div > button')
        currency_dropdown_button.click()
        # Find the dropdown menu
        driver.implicitly_wait(1)

        currency_dropdown_menu = driver.find_element(By.CSS_SELECTOR, '#asset-page-currency-selector > div > div.cds-flex-f1g67tkn.cds-flex-end-fb2j2v1.cds-column-ci8mx7v.cds-staticPosition-si6ru8l > div > ul')

        # Locate the USD option and click it (replace 'USD' with the actual text of the option)
        usd_option = currency_dropdown_menu.find_element(By.CSS_SELECTOR, '#search-dropdown-option-43')
        usd_option.click()

        driver.implicitly_wait(1)

        time.sleep(5)


        # Get the page source after JavaScript rendering
        html = driver.page_source
        # Close the driver
        driver.quit()
        return BeautifulSoup(html, 'lxml')
    def provideLinkForGivenPage(self, pageNumber):
        return self.link + f'?page={pageNumber}'
    def scrapeOnePage(self, pageNumber, dataCoin):
        soupCoinBase = self.createSoup(self.provideLinkForGivenPage(pageNumber))
        offers = soupCoinBase.find_all('tr', class_='cds-tableRow-t45thuk cds-tableRowHover-t9ma3wv')

        for offer in offers:
            allMainCoinInfos = offer.find_all_next('td', class_='cds-tableCell-t1jg7jzg')
            coinName = allMainCoinInfos[0].findNext('h2', class_="cds-typographyResets-t1xhpuq2 cds-headline-hb7l4gg cds-foreground-f1yzxzgu cds-transition-txjiwsi cds-start-s1muvu8a").text
            coinPrice = allMainCoinInfos[1].find_next('div', class_="cds-flex-f1g67tkn cds-flex-end-f9tvb5a cds-column-ci8mx7v cds-flex-start-f1urtf06").find('span').text
            coinPrice = float(coinPrice.replace(',', '').replace('€', ''))
            coinAbbreviation = allMainCoinInfos[0].findNext('p',class_='cds-typographyResets-t1xhpuq2 cds-label2-l5adacs cds-foregroundMuted-f1vw1sy6 cds-transition-txjiwsi cds-start-s1muvu8a').text
            newCoin = Coin(coinName, coinPrice, "CoinBase", coinAbbreviation)
            dataCoin.append(newCoin)



    # def scrapeGivenPages(self, minPage, maxPage):
    #     data = []
    #
    #     with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    #         futures = [executor.submit( self.scrapeOnePage, page, data) for page in range(minPage, maxPage + 1)]
    #         concurrent.futures.wait(futures)
    #
    #     return data
    def findUSDPrice(self):
        soupTether = self.createSoup('https://www.coinbase.com/price/tether')
        price = soupTether.find('div', class_ = 'cds-typographyResets-t1xhpuq2 cds-display3-doujgnf cds-foreground-f1yzxzgu'
        ' cds-transition-txjiwsi cds-start-s1muvu8a cds-tabularNumbers-t11sqpt cds-1-_qem5ui').find('span').text
        return price