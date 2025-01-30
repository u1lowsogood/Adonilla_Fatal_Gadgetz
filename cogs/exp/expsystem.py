import psycopg2
from psycopg2.extras import DictCursor

class ExpSystem:

    def __init__(self, sqluser, sqlpassword):
        self.sqluser = sqluser
        self.sqlpassword = sqlpassword

        self.exp_max_multiplier = 1.3

    def _connect(self):
        return psycopg2.connect(user=self.sqluser, password=self.sqlpassword, host="localhost", port="5432", dbname="exp")

    def _ensure_exp_exists(self, user_uuid : int):
        with self._connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(
                    "INSERT INTO accounts (level, user_uuid, exp_current, exp_max) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
                    (0, user_uuid, 0, 100)
                )
                conn.commit()

    def add_exp(self, user_uuid, exp_amount):
        self._ensure_account_exists(user_uuid)
        with self._connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("SELECT exp_current,exp_max,level FROM exp WHERE user_uuid = %s", (user_uuid,))
                result = cur.fetchone()

                exp = result['exp_current']
                exp_max = result['exp_max']
                level = result['level']

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

    def get_ranking(self,limit=5):
        with self._connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("SELECT user_uuid, level, exp_current FROM exp ORDER BY level,exp_current DESC LIMIT %s",(limit,))
                result = cur.fetchall()
                members_list = [(row['user_uuid'], row['level']) for row in result]
                return members_list