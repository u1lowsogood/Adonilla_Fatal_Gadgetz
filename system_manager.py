from cogs.adonilla_eco_system.economysystem import EconomySystem
from cogs.shops.shops.shopsystem import ShopSystem
from cogs.shops.premium_shop.premiumsystem import PremiumSystem
from cogs.exp.expsystem import ExpSystem

class SystemManager:
    def __init__(self, sqluser, sqlpassword, bot):
        try:
            self._economy = EconomySystem(sqluser, sqlpassword)
            self._shop = ShopSystem(sqluser, sqlpassword, self._economy)
            self._premium = PremiumSystem()
            self._exp = ExpSystem(sqluser, sqlpassword,bot)
        except Exception as e:
            print(f"[ERROR] SystemManager initialization failed: {e}")
            raise 

    @property
    def economysystem(self):
        return self._economy

    @property
    def shopsystem(self):
        return self._shop

    @property
    def premiumsystem(self):
        return self._premium
    
    @property
    def expsystem(self):
        return self._exp