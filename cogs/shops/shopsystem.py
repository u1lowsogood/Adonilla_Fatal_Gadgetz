import psycopg2
from psycopg2.extras import DictCursor
from textwrap import dedent

class ShopSystem:

    def __init__(self, sqluser, sqlpassword, economysystem):
        self.sqluser = sqluser
        self.sqlpassword = sqlpassword
        self.economysystem = economysystem

    def _connect(self):
        return psycopg2.connect(user=self.sqluser, password=self.sqlpassword, host="localhost", port="5432", dbname="adonilla_economy_system")

    def purchase(self, uuid : str, item_id, amount):
        with self._connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("""
                    SELECT items.name, items.description, items.price
                    FROM items
                    JOIN shops ON items.shop_id = shops.id
                    WHERE items.id = %s
                """,  (item_id,))
                item = cur.fetchone()
                if not item:
                    raise ValueError("指定された商品が見つかりません。")

                price, item_name = item[2], item[0]

                balance = self.economysystem.get_balance(uuid)
                total_price = price * amount 
                if balance < total_price:
                    raise ValueError(f"残高が不足しています：{total_price - balance}")

                self.economysystem.withdraw(uuid, total_price)
                self.add_item(uuid, item_id, amount)

                return f"""アイテムを購入しました！\n## 『{item_name}』x{amount}\n\n残高:  :moneybag:**__ {balance - total_price} ADP__**"""

    def add_item(self, uuid, item_id, amount):
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO inventory (user_uuid, item_id, amount)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (item_id)
                    DO UPDATE SET amount = inventory.amount + EXCLUDED.amount
                """, (uuid, item_id, amount,))
                
                # コミットして変更を確定
                conn.commit()

    def consume_item(self, uuid, item_id):
        with self._connect() as conn:
            with conn.cursor() as cur:
                # 在庫確認
                cur.execute("""
                    SELECT amount FROM inventory WHERE user_uuid = %s AND item_id = %s
                """, (uuid, item_id))
                inventory_item = cur.fetchone()
                if not inventory_item or inventory_item[0] <= 0:
                    raise ValueError("インベントリに指定された商品がありません。")

                # 在庫を更新
                cur.execute("""
                    UPDATE inventory SET amount = amount - 1
                    WHERE user_uuid = %s AND item_id = %s
                """, (uuid, item_id,))
                conn.commit()

                return item_id

    def get_shop_items(self, shop_id):
        with self._connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("""
                    SELECT items.name, items.description, items.price
                    FROM items
                    JOIN shops ON items.shop_id = shops.id
                    WHERE shops.id = %s
                """, (shop_id,))
                items = cur.fetchall()
                return [(row['name'], row['description'], row['price']) for row in items]

    def get_inventory_items(self, uuid, shop_id):
        with self._connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("""
                    SELECT items.id, items.name, items.description, inventory.amount
                    FROM inventory
                    JOIN items ON items.id = inventory.item_id
                    JOIN shops ON items.shop_id = shops.id
                    WHERE inventory.user_uuid = %s AND shops.id = %s
                """, (uuid, shop_id,))
                items = cur.fetchall()
                return [(row['id'], row['name'], row['description'], row['amount']) for row in items]