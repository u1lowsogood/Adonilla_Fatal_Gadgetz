from cogs.adonilla_eco_system.economysystem import EconomySystem
from cogs.shops.shops.shopsystem import ShopSystem
from cogs.shops.premium_shop.premiumsystem import PremiumSystem
from cogs.exp.expsystem import ExpSystem

class SystemManager:
    def __init__(self, sqluser, sqlpassword):
        self.economy = EconomySystem(sqluser, sqlpassword)
        self.shop = ShopSystem(sqluser, sqlpassword, self.economy)
        self.premium = PremiumSystem()
        self.exp = ExpSystem(sqluser, sqlpassword)

    @property
    def economysystem(self):
        return self.economy

    @property
    def shopsystem(self):
        return self.shop

    @property
    def premiumsystem(self):
        return self.premium
    
    @property
    def expsystem(self):
        return self.expsystem