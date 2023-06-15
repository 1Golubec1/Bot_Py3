from config import *
class FUNCTIONS:
    @staticmethod
    def save_info(connect, user_id, per, meaning):
        connect.execute(f"UPDATE {name_bd} SET {per} = \"{meaning}\" WHERE id = {user_id}")
        connect.commit()

    @staticmethod
    def Connect(connect, cursor):
        cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {name_bd} (id TEXT, state TEXT, commands TEXT)""")
        connect.commit()

    @staticmethod
    def check_pl(connect, cursor, user_id):
        if cursor.execute(f"SELECT id FROM {name_bd} WHERE id = {user_id} ").fetchone() is None:
            cursor.execute(
                f"INSERT INTO {name_bd} VALUES ({user_id}, '', '[]')")
            connect.commit()
            return True
        return False

    @staticmethod
    def get_variable(connect, user_id, per):
        return connect.execute(f"SELECT {per} FROM {name_bd} WHERE id = {user_id}").fetchone()[0]