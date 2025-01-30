from cogs.adonilla_eco_system.economysystem import EconomySystem
from cogs.shops.shops.shopsystem import ShopSystem
from cogs.shops.premium_shop.premiumsystem import PremiumSystem
from cogs.exp.expsystem import ExpSystem

class SystemManager:
    def __init__(self, sqluser, sqlpassword, bot):
        self.economy = EconomySystem(sqluser, sqlpassword)
        self.shop = ShopSystem(sqluser, sqlpassword, self.economy)
        self.premium = PremiumSystem()
        self.exp = ExpSystem(sqluser, sqlpassword,bot)

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
        return self.exp