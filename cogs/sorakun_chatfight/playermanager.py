import random
from cogs.sorakun_chatfight.player import Player
from cogs.sorakun_chatfight.author import Author

class PlayerManager():
    def __init__(self):
        self.players = {"sora":Player(Author.SORA,1,25), "haruto":Player(Author.HARUTO,5,40)}
        self.current_attacker : Player = random.choice(list(self.players.values()))
        self.next_attacker : Player = self.current_attacker

    def get_opponent(self):
        return self.players["haruto"] if self.current_attacker == self.players["sora"] else self.players["sora"]
    
    def set_next_attacker_randomly(self):
        self.next_attacker = random.choice(list(self.players.values()))

    def flip_attacker(self):
        self.current_attacker = self.next_attacker
        self.current_attacker.show_health_gauge = True