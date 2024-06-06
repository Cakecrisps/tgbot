import datetime
import sqlite3
db = sqlite3.connect("users.db")
cursor = db.cursor()

def add_pltej(billid,customid, userid,typepay):
    db.execute(f"SELECT * FROM pays WHERE billid = '{billid}'")
    if cursor.fetchone() is None:
         db.execute("INSERT INTO pays VALUES (?,?,?,?,?)", (userid, billid,customid, str(datetime.date.today()),typepay))
         db.commit()

def get_pays():
    return db.execute('SELECT * FROM pays').fetchall()
def deletepay(billid):
    db.execute(f"DELETE FROM pays WHERE billid = '{billid}'")
    db.commit()
