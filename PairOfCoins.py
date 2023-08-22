from Coin import Coin
class PairOfCoins:
    def __init__(self, coin1, coin2):
        self.coin1 = coin1
        self.coin2 = coin2
        # self.percentagePriceDifference = self.calculatePricePercentageDifference()

    def calculatePricePercentageDifference(self):
        value1 = self.coin1.getValue()
        value2 = self.coin2.getValue()
        return abs(value1-value2)/min(value1,value2)*100
    def getName(self):
        return self.coin1.getName()
    def getValue(self):
        return self.coin1.getValue()
