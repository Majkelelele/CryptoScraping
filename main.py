from DataScraper import DataScraper
import time
from Sorting import Sorting
from PairOfCoins import PairOfCoins

def main():

    dataScraper = DataScraper()
    coinsBinance = dataScraper.scrapeAllPages(25,'Binance')
    coinsCoinBase = dataScraper.scrapeAllPages(25,'CoinBase')
    sorting = Sorting(coinsBinance,coinsCoinBase)
    data = sorting.createListOfMatchingCoins()



    for coin in data:
        print(coin.getName())
        print(str(coin.calculatePricePercentageDifference())+'%')
    print(data.__len__())


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Main execution time: {execution_time:.6f} seconds")







