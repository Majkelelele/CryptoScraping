from PairOfCoins import PairOfCoins
from Coin import Coin
class Sorting:
    def __init__(self, site1Coins, site2Coins):
        self.site1data = site1Coins
        self.site2data = site2Coins


    def createListOfMatchingCoins(self):
        coin_pairs = []

        for coin1 in self.site1data:
            for coin2 in self.site2data:
                if (self.coinRequirements(coin1,coin2)):
                    coin_pair = PairOfCoins(coin1,coin2)
                    coin_pairs.append(coin_pair)
        sortedlist = sorted(coin_pairs, key=lambda pair: pair.percentagePriceDifference)

        return sortedlist

    def coinRequirements(self, coin1, coin2):
        return coin1.getValue() > 0 and coin2.getValue() > 0 and \
            coin1.getName() == coin2.getName()

