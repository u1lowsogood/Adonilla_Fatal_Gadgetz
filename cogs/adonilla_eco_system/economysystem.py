import psycopg2
from psycopg2.extras import DictCursor

class EconomySystem:

    def __init__(self, sqluser, sqlpassword):
        self.sqluser = sqluser
        self.sqlpassword = sqlpassword

    def _connect(self):
        return psycopg2.connect(user=self.sqluser, password=self.sqlpassword, host="localhost", port="5432", dbname="adonilla_economy_system")

    def _ensure_account_exists(self, user_uuid):
        with self._connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(
                    "INSERT INTO accounts (user_uuid) VALUES (%s) ON CONFLICT DO NOTHING",
                    (user_uuid,)
                )
                conn.commit()

    def get_balance(self, user_uuid):
        self._ensure_account_exists(user_uuid)
        with self._connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("SELECT balance FROM accounts WHERE user_uuid = %s", (user_uuid,))
                result = cur.fetchone()
                return result['balance'] if result else 0

    def deposit(self, user_uuid, amount, reason="Deposit"):
        self._ensure_account_exists(user_uuid)
        with self._connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("SELECT balance FROM accounts WHERE user_uuid = %s", (user_uuid,))
                result = cur.fetchone()

                new_balance = result['balance'] + amount

                cur.execute(
                    "UPDATE accounts SET balance = %s WHERE user_uuid = %s",
                    (new_balance, user_uuid)
                )
                
                conn.commit()

    def withdraw(self, user_uuid, amount, reason="Withdrawal"):
        self._ensure_account_exists(user_uuid)
        with self._connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:

                cur.execute("SELECT balance FROM accounts WHERE user_uuid = %s", (user_uuid,))
                result = cur.fetchone()

                new_balance = result['balance'] - amount
                if new_balance < 0:
                    raise ValueError("残金なし")
                
                cur.execute(
                    "UPDATE accounts SET balance = %s WHERE user_uuid = %s",
                    (new_balance, user_uuid)
                )
                conn.commit()

    def get_ranking(self,limit=5):
        with self._connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("SELECT user_uuid, balance FROM accounts ORDER BY balance DESC LIMIT %s",(limit,))
                result = cur.fetchall()
                members_list = [(row['user_uuid'], row['balance']) for row in result]
                return members_list
