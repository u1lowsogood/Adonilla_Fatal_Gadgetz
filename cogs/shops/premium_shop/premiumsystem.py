import psycopg2
from psycopg2.extras import DictCursor
from textwrap import dedent

class PremiumSystem:

    def __init__(self):
        self.ROLES = [
            (1241082277790744717,797377803099570176),
            (1241082811557875845,797378756573790238),
            (1241082814661918811,797378769597628457),
            (1241082818512294092,797378770657869834),
            (1241082801869295666,797378771786137620),
        ]

    def _connect(self):
        return psycopg2.connect(user=self.sqluser, password=self.sqlpassword, host="localhost", port="5432", dbname="adonilla_economy_system")

    def get_level_sum(self, member):
        sm = 0
        for i, roles in enumerate(self.ROLES,start=1):
            if member.get_role(roles[1]) != None:
                sm += i
        return sm