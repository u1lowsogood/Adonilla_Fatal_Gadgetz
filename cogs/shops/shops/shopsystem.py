import psycopg2
from psycopg2.extras import DictCursor

class ShopSystem:

    def __init__(self, sqluser, sqlpassword, economysystem):
        self.sqluser = sqluser
        self.sqlpassword = sqlpassword
        self.economysystem = economysystem

    def _connect(self):
        return psycopg2.connect(user=self.sqluser, password=self.sqlpassword, host="localhost", port="5432", dbname="adonilla_economy_system")

    def purchase(self, uuid: str, shop_id: int, item_id: int, amount: int):
        with self._connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("""
                    SELECT name, description, price
                    FROM shop_items
                    WHERE shop_id = %s AND item_id = %s
                """, (shop_id, item_id))
                item = cur.fetchone()
                if not item:
                    raise ValueError("指定された商品が見つかりません。")

                price, item_name = item['price'], item['name']
                balance = self.economysystem.get_balance(uuid)
                total_price = price * amount
                if balance < total_price:
                    raise ValueError(f"残高が不足しています：{total_price - balance}")

                self.economysystem.withdraw(uuid, total_price)
                kokko_uuid = self.economysystem.get_kokko_uuid()
                self.economysystem.deposit(kokko_uuid, total_price)

                self.add_item(uuid, shop_id, item_id, amount)

                return f"""アイテムを購入しました！\n## 『{item_name}』x{amount}\n\n残高:  :moneybag:**__ {balance - total_price} ADP__**"""

    def add_item(self, uuid: str, shop_id: int, item_id: int, amount: int):
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO inventory (user_uuid, shop_id, item_id, amount)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (user_uuid, shop_id, item_id)
                    DO UPDATE SET amount = inventory.amount + EXCLUDED.amount
                """, (uuid, shop_id, item_id, amount))
                conn.commit()

    def consume_item(self, uuid: str, shop_id: int, item_id: int):
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT amount FROM inventory
                    WHERE user_uuid = %s AND shop_id = %s AND item_id = %s
                """, (uuid, shop_id, item_id))
                inventory_item = cur.fetchone()

                if not inventory_item or inventory_item[0] <= 0:
                    return False

                cur.execute("""
                    UPDATE inventory
                    SET amount = amount - 1
                    WHERE user_uuid = %s AND shop_id = %s AND item_id = %s
                """, (uuid, shop_id, item_id))
                conn.commit()
                return True

    def get_shop_items(self, shop_id: int):
        with self._connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("""
                    SELECT item_id, name, description, price
                    FROM shop_items
                    WHERE shop_id = %s
                    ORDER BY item_id ASC
                """, (shop_id,))
                items = cur.fetchall()
                return [(row['item_id'], row['name'], row['description'], row['price']) for row in items]

    def get_inventory_items(self, uuid: str, shop_id: int):
        with self._connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("""
                    SELECT shop_items.item_id, name, description, amount
                    FROM inventory
                    JOIN shop_items ON inventory.shop_id = shop_items.shop_id AND inventory.item_id = shop_items.item_id
                    WHERE inventory.user_uuid = %s AND inventory.shop_id = %s AND inventory.amount > 0
                    ORDER BY item_id ASC
                """, (uuid, shop_id))
                items = cur.fetchall()
                return [(row['item_id'], row['name'], row['description'], row['amount']) for row in items]
