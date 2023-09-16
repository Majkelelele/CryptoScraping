from abc import abstractmethod
import concurrent.futures

class DataScraper:
    def __init__(self, maxPage):
        self.maxPage = maxPage

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

    @abstractmethod
    def createSoup(self,link):
        pass
    @abstractmethod
    def provideLinkForGivenPage(self, pageNumber):
        pass
    @abstractmethod
    def scrapeOnePage(self, pageNumber, dataCoinBinance):
        pass

    def scrapeGivenPages(self, minPage, maxPage):
        data = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(self.scrapeOnePage, page, data) for page in range(minPage, maxPage + 1)]
            concurrent.futures.wait(futures)

        return data
    def scrapeAllPages(self):
        return self.scrapeGivenPages(1,self.maxPage)