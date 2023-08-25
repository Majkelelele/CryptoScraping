from Coin import Coin
class PairOfCoins:
    def __init__(self, coin1, coin2):
        self.coin1 = coin1
        self.coin2 = coin2
        self.percentagePriceDifference = self.calculatePricePercentageDifference()

    def calculatePricePercentageDifference(self):
        value1 = self.coin1.getValue()
        value2 = self.coin2.getValue()
        return abs(value1-value2)/min(value1,value2)*100
    def getPricePercentageDifference(self):
        return self.percentagePriceDifference
    def getName(self):
        return self.coin1.getName()
    def getValue(self):
        value1 = str(self.coin1.getValue())
        value2 = str(self.coin2.getValue())
        return value1 + ',' + value2
    def printInfo(self, count):
        print(str(count) + "): ")
        print("Coin name: " + str(self.coin1.getName()))
        print("First site name: " + str(self.coin1.getSiteName()))
        print("First site value: " + str(self.coin1.getValue()))
        print("Second site name: " + str(self.coin2.getSiteName()))
        print("Second site value: " + str(self.coin2.getValue()))
        print("Price percentage difference: " + str(self.calculatePricePercentageDifference()) + '%')
