from BinanceScraper import BinanceScraper
from CoinBaseScraper import CoinBaseScraper
import time
from Sorting import Sorting

class MainProgram:
    def run(self):
        start_time = time.time()
        coinsBinance = BinanceScraper().scrapeAllPages()
        coinsCoinBase = CoinBaseScraper().scrapeAllPages()
        # for i, coin in enumerate(coinsBinance, start=1):
        #     coin.printInfo(i)
        # for i, coin in enumerate(coinsCoinBase, start=1):
        #     coin.printInfo(i)



        sorting = Sorting(coinsBinance,coinsCoinBase)
        data = sorting.createListOfMatchingCoins()





        for i, coin in enumerate(data, start=1):
            coin.printInfo(i)


        print("Number of coins matched: " + str(data.__len__()))
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Main execution time: {execution_time:.6f} seconds")