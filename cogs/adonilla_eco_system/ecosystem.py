import sqlite3
from discord.ext import commands

class Economy:
    def __init__(self, db_path="economy.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._initialize_table()

    def _initialize_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS economy (
                uuid TEXT PRIMARY KEY,
                balance INTEGER NOT NULL
            )
        """)
        self.conn.commit()

    def get_balance(self, uuid):
        self.cursor.execute("SELECT balance FROM economy WHERE uuid = ?", (uuid,))
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def deposit(self, uuid, amount):
        balance = self.get_balance(uuid) + amount
        self.cursor.execute(
            "REPLACE INTO economy (uuid, balance) VALUES (?, ?)", 
            (uuid, balance)
        )
        self.conn.commit()

    def withdraw(self, uuid, amount):
        balance = self.get_balance(uuid) - amount
        if balance < 0:
            raise ValueError("Insufficient funds")
        self.cursor.execute(
            "REPLACE INTO economy (uuid, balance) VALUES (?, ?)", 
            (uuid, balance)
        )
        self.conn.commit()

# ボット初期化
bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# Cog例
class EconomyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def balance(self, ctx):
        economy = self.bot.economy
        uuid = str(ctx.author.id)
        balance = economy.get_balance(uuid)
        await ctx.send(f"{ctx.author.mention}の残高: {balance}コイン")

    @commands.command()
    async def deposit(self, ctx, amount: int):
        economy = self.bot.economy
        uuid = str(ctx.author.id)
        economy.deposit(uuid, amount)
        await ctx.send(f"{ctx.author.mention}に{amount}コインを入金しました！")

# 起動時にEconomyインスタンスを作成
bot.economy = Economy()

# Cogを登録
bot.add_cog(EconomyCog(bot))

bot.run("YOUR_TOKEN")
