from DataScraper import DataScraper
import time

def main():

    dataScraperBinance = DataScraper()
    data = dataScraperBinance.scrapeAllPages(10,'Binance')
    # sortedCoins = sorted(data, key=lambda coin: coin.getValue())
    for coin in data:
        print(coin.getName())
        print(coin.getValue())
    print(data.__len__())


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Main execution time: {execution_time:.6f} seconds")







