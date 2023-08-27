class Coin:
    def __init__(self, name, value, site, abr):
        self.name = name
        self.value = value
        self.abreviation = abr
        self.siteName = site

    def getName(self):
        return self.name
    def getValue(self):
        return self.value
    def getAbreviation(self):
        return self.abreviation
    def getSiteName(self):
        return self.siteName
    def compare(self, other_coin):
        if self.name == other_coin.name:
            return True
        else:
            return False
    def calculatePercentageDifference(self, other):
        return abs(self.value-other.value)/min(self.value,other.value)*100
    def findItself(self, data):
        Coin = None
        for coin in data:
            if coin.getName() == "Maker":
                Coin = coin
        return Coin