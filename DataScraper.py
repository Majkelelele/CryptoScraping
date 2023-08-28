from bs4 import BeautifulSoup
from PairOfCoins import PairOfCoins
from Coin import Coin
from selenium import webdriver
import concurrent.futures
from selenium.webdriver.common.by import By

class DataScraper:
    def __init__(self):
        self.BinanceLink = 'https://www.binance.com/en/markets/overview'
        self.KrakenLink = 'https://www.kraken.com/prices'
        self.CoinBaseLink = 'https://www.coinbase.com/explore'
        self.USDPrice = float(self.findUSDPrice().split()[1])

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
        options.add_argument("--headless")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
            " Chrome/93.0.4577.63 Safari/537.36")
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('--disable-gpu')
        # options.add_argument('--remote-debugging-port=9222')
        return options


    def scrapeOnePageBinanceXPath(self, pageNumber, dataCoinBinance):
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=self.addOptions(options))
        driver.get(self.provideLinkForGivenPageBinance(pageNumber))
        numberOfCoinsPerPage = 15
        for i in range(0,numberOfCoinsPerPage):
            entireCoin = driver.find_element(by=By.XPATH, value="//div[@class='css-vlibs4'][i]")
            coinName = entireCoin.find_element(by=By.XPATH, value = "//div[@class='css-uaf1yb']").text
            coinPrice = entireCoin.find_element(by=By.XPATH, value = "//div[@class='css-hwo5f4']").text
            coinPrice = float(coinPrice.replace("$", "").replace(",", ""))
            coinAbbreviation = entireCoin.find_element(by=By.XPATH, value = "//div[@class='css-1x8dg53']").text
            newCoin = Coin(coinName, coinPrice, "Binance", coinAbbreviation)
            dataCoinBinance.append(newCoin)

    def provideLinkForGivenPageBinance(self, pageNumber):
        return self.BinanceLink + f'?p={pageNumber}'
    def provideLinkForGivenPageCoinBase(self, pageNumber):
        return self.CoinBaseLink + f'?page={pageNumber}'

    def scrapeOnePageBinance(self, pageNumber, dataCoinBinance):
        soupBinance = self.createSoup(self.provideLinkForGivenPageBinance(pageNumber))
        offers = soupBinance.findAll('div', class_='css-vlibs4')

        for offer in offers:
            coinName = offer.find('div', class_='css-uaf1yb').text
            coinPrice = offer.find('div', class_='css-hwo5f4').text
            coinPrice =  float(coinPrice.replace("$", "").replace(",", ""))
            coinAbbreviation = offer.find('div', class_ = 'css-1x8dg53').text
            newCoin = Coin(coinName, coinPrice,"Binance",coinAbbreviation)
            dataCoinBinance.append(newCoin)
    def scrapeOnePageCoinBase(self, pageNumber, dataCoin):
        soupCoinBase = self.createSoup(self.provideLinkForGivenPageCoinBase(pageNumber))
        offers = soupCoinBase.find_all('tr', class_='cds-tableRow-t45thuk cds-tableRowHover-t9ma3wv')

        for offer in offers:
            allMainCoinInfos = offer.find_all_next('td', class_ = 'cds-tableCell-t1jg7jzg')
            coinName = allMainCoinInfos[0].findNext('h2', class_="cds-typographyResets-t1xhpuq2 cds-headline-hb7l4gg cds-foreground-f1yzxzgu cds-transition-txjiwsi cds-start-s1muvu8a").text
            coinPrice = allMainCoinInfos[1].findNext('div', class_ = 'cds-flex-f1g67tkn cds-flex-end-f9tvb5a cds-column-ci8mx7v cds-flex-start-f1urtf06').find('span').text
            coinPrice = float(coinPrice.split()[-1].replace(",", ""))/self.USDPrice
            coinAbbreviation = allMainCoinInfos[0].findNext('p', class_ = 'cds-typographyResets-t1xhpuq2 cds-label2-l5adacs cds-foregroundMuted-f1vw1sy6 cds-transition-txjiwsi cds-start-s1muvu8a').text
            newCoin = Coin(coinName, coinPrice,"CoinBase",coinAbbreviation)
            dataCoin.append(newCoin)

    def findUSDPrice(self):
        soupTether = self.createSoup('https://www.coinbase.com/price/tether')
        price = soupTether.find('div', class_ = 'cds-typographyResets-t1xhpuq2 cds-display3-doujgnf cds-foreground-f1yzxzgu'
        ' cds-transition-txjiwsi cds-start-s1muvu8a cds-tabularNumbers-t11sqpt cds-1-_qem5ui').find('span').text
        return price



    # def scrapeAllPages(self,maxPage,site):
    #     data = []
    #     for page in range(1, maxPage + 1):
    #         if site == 'Binance':
    #             self.scrapeOnePageBinance(page, data)
    #         else:
    #             self.scrapeOnePageCoinBase(page, data)
    #     return data
    def scrapeAllPages(self, maxPage, site):
        data = []

        def scrape_page(page_number, data_list):
            if site == 'Binance':
                self.scrapeOnePageBinance(page_number, data_list)
                # self.scrapeOnePageBinanceXPath(page_number,data_list)
            else:
                self.scrapeOnePageCoinBase(page_number, data_list)

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(scrape_page, page, data) for page in range(1, maxPage + 1)]
            concurrent.futures.wait(futures)

        return data