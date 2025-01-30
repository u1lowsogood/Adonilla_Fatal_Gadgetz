import discord.ext
import discord.ext.commands
import psycopg2
from psycopg2.extras import DictCursor
from discord.ext import commands
import discord
import re

class ExpSystem:
    def __init__(self, sqluser, sqlpassword, bot):
        self.sqluser = sqluser
        self.sqlpassword = sqlpassword
        self.bot : commands.Bot = bot

        self.exp_max_multiplier = 1.3

    def _connect(self):
        return psycopg2.connect(user=self.sqluser, password=self.sqlpassword, host="localhost", port="5432", dbname="exp")

    def _ensure_exp_exists(self, user_uuid : int):
        with self._connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(
                    "INSERT INTO exp (level, user_uuid, exp_current, exp_max) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
                    (0, user_uuid, 0, 100)
                )
                conn.commit()

    async def add_exp(self, member : discord.Member, exp_amount):
        user_uuid = member.id
        if exp_amount < 0:
            return
        
        self._ensure_exp_exists(user_uuid)
        with self._connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("SELECT exp_current,exp_max,level FROM exp WHERE user_uuid = %s", (user_uuid,))
                result = cur.fetchone()

                exp = result['exp_current']
                exp_max = result['exp_max']
                level = result['level']
                old_level = level

                exp += exp_amount
                
                while exp >= result['exp_max']:
                    exp -= exp_max
                    level += 1
                    exp_max = int(self.exp_max_multiplier*exp_max)

                cur.execute(
                    "UPDATE exp SET exp_current=%s,exp_max=%s, level=%s WHERE user_uuid = %s",
                    (exp,exp_max,level,user_uuid)
                )
                
                conn.commit()

                if old_level != level:
                    await self.level_up(member)

    async def level_up(self, member : discord.Member):

        status = self.get_status(member.id)
        level = status['level']
        old_nick = member.nick or member.name
        match = re.match(r"^(.*?)(?: 【Lv\. \d+】)?$", old_nick)
        base_name = match.group(1) 
        new_nick = f"{base_name} 【Lv. {level}】"

        #lvup_emoji = ["🇱","🇻","🇺","🇵"]
        #for emoji in lvup_emoji:
        #    await message.add_reaction(emoji)

        print(new_nick)
        try:
            await member.edit(nick=new_nick)
        except discord.Forbidden:
            print(f"権限ないよ（笑） {member.name}")

    def get_status(self, user_uuid):
        self._ensure_exp_exists(user_uuid)
        with self._connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("SELECT level,exp_current,exp_max FROM exp WHERE user_uuid = %s", (user_uuid,))
                result = cur.fetchone()

                if result:
                    return {
                        "level": result["level"],
                        "exp_current": result["exp_current"],
                        "exp_max": result["exp_max"]
                    }
                else:
                    return None

    def get_ranking(self,limit=5):
        with self._connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("SELECT user_uuid, level, exp_current, exp_max FROM exp ORDER BY level DESC,exp_current DESC LIMIT %s",(limit,))
                result = cur.fetchall()
                members_list = [(row['user_uuid'], row['level'], row['exp_current'], row['exp_max']) for row in result]
                return members_list