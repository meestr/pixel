import sqlite3


data = sqlite3.connect('data.db')
c = data.cursor()
c.execute("""CREATE TABLE players (id integer, bal integer, daily_factor integer)""")