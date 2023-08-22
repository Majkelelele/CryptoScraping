from Coin import Coin
class CoinCollection:
    def __init__(self):
        self.coins = {}

    def add_coin(self, coin):
        self.coins[coin.name] = coin

    def find_coin_by_name(self, coin_name):
        if coin_name in self.coins:
            return self.coins[coin_name]
        else:
            return None