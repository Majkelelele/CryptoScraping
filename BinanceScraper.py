from DataScraper import DataScraper
from Coin import Coin
import concurrent.futures
class BinanceScraper(DataScraper):
    def __init__(self):
        super().__init__(25)
        self.link = 'https://www.binance.com/en/markets/overview'
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
