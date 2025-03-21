# afgBot.py
import discord
from discord.ext import commands
from system_manager import SystemManager

class afgBot(commands.Bot):
    def __init__(self, token: str, sqluser: str, sqlpassword: str):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.reactions = True
        intents.voice_states = True

        super().__init__(command_prefix="/", intents=intents)
        self._sqluser = sqluser
        self._sqlpassword = sqlpassword
        self._adonilla_id = 364043473768284161
        self._system_manager = SystemManager(self._sqluser, self._sqlpassword, self)
    
    @property
    def sqluser(self):
        return self._sqluser
    
    @property
    def sqlpassword(self):
        return self._sqlpassword
    
    @property
    def adonilla_id(self):
        return self._adonilla_id
    
    @property
    def system(self):
        return self._system_manager
