from bs4 import BeautifulSoup
from PairOfCoins import PairOfCoins
from Coin import Coin
from selenium import webdriver


class DataScraper:
    def __init__(self):
        self.BinanceLink = 'https://www.binance.com/en/markets/overview'
        self.KrakenLink = 'https://www.kraken.com/prices'
        self.CoinBaseLink = 'https://www.coinbase.com/explore'

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
    #     options.add_argument("--headless")
        options.add_argument("--disable-images")
        options.add_argument("--disable-javascript")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        options.add_argument("--disable-internal-flash")
        return options



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
            newCoin = Coin(coinName, coinPrice,"Binance")
            dataCoinBinance.append(newCoin)
    def scrapeOnePageCoinBase(self, pageNumber, dataCoin):
        soupCoinBase = self.createSoup(self.provideLinkForGivenPageCoinBase(pageNumber))
        offers = soupCoinBase.find_all('tr', class_='cds-tableRow-t45thuk cds-tableRowHover-t9ma3wv')

        for offer in offers:
            allMainCoinInfos = offer.find_all_next('td', class_ = 'cds-tableCell-t1jg7jzg')
            coinName = allMainCoinInfos[0].findNext('h2', class_="cds-typographyResets-t1xhpuq2 cds-headline-hb7l4gg cds-foreground-f1yzxzgu cds-transition-txjiwsi cds-start-s1muvu8a").text
            coinPrice = allMainCoinInfos[1].findNext('div', class_ = 'cds-flex-f1g67tkn cds-flex-end-f9tvb5a cds-column-ci8mx7v cds-flex-start-f1urtf06').find('span').text
            coinPrice = float(coinPrice.split()[-1].replace(",", ""))/4.11
            newCoin = Coin(coinName, coinPrice,"CoinBase")
            dataCoin.append(newCoin)


    # def scrapeOnePageKraken(self, pageNumber, dataCoinKraken):
    #     soupKraken = self.createSoup(self.provideLinkForGivenPageKraken(pageNumber))
    #     offers = soupKraken.findAll('tr', class_='fc187 fc-bc02027a-1 fc189')
    #
    #     for offer in offers:
    #         coinName = offer.find('span', class_='fc-bc02027a-7')
    #
    #         coinPrice = offer.find('span', class_='fc-bc02027a-9')
    #         newCoin = Coin(coinName, coinPrice)
    #         dataCoinKraken.append(newCoin)


    def scrapeAllPages(self,maxPage,site):
        data = []
        for page in range(1, maxPage + 1):
            if site == 'Binance':
                self.scrapeOnePageBinance(page, data)
            else:
                self.scrapeOnePageCoinBase(page, data)
        return data