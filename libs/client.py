import sqlite3
import os.path


class Client:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, 'data.db')
        self.data = sqlite3.connect(db_path)
        self.d = self.data.cursor()

    async def get_value(self, _id):
        self.d.execute(f'SELECT * FROM players WHERE id={_id}')
        return self.d.fetchall()

    async def create_value(self, _id):
        with self.data:
            self.d.execute(f'INSERT INTO players VALUES ({_id}, 0, 0)')

    async def update(self, bal, _id):
        with self.data:
            self.d.execute('UPDATE players SET bal = :bal WHERE id = :_id',
                           {'bal': bal, '_id': _id})
    async def update_daily(self, inte, _id):
        with self.data:
            self.d.execute('UPDATE players SET daily_factor = :inte WHERE id = :_id',
                           {"_"})
