import sqlite3
import sqlite3
import datetime
import random
db = sqlite3.connect("users.db", check_same_thread=False)
cursor = db.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
userid BIGINT,
chatid BIGINT,
tokens BIGINT,
Dateofsubs Text,
LastCall Text)""")
db.commit()
import time
def checkautor(userid):
    cursor.execute(f"SELECT * FROM Autors WHERE userid = {userid}")
    #print(cursor.fetchone())
    user = cursor.fetchone()
    if user == None:
        return False
    if user[2] == 0:
        return True
    else:
        return False

def create_autor(userid,name):
    cursor.execute(
            f"INSERT INTO Autors VALUES({userid},'{name}',{1})")
    db.commit()
    return "ok"
def turnoff_autor(userid):
    cursor.execute(f"UPDATE Autors SET isWork = {0} WHERE userid ={userid}")
    db.commit()
    return "ok"
def turnon_autor(userid):
    cursor.execute(f"UPDATE Autors SET isWork = {1} WHERE userid ={userid}")
    db.commit()
    return "ok"
def checkreferal(referalid):
    cursor.execute(f"SELECT * FROM referals WHERE referalid = '{referalid}'")
    if cursor.fetchone() == None:
        return False
    else:
        return True
def create_referal(userid,name,bonus):
    id = f'0{userid}AND{random.randint(-100000,10000)}AND{time.time()}'.replace('.','')
    id = id + '0'*(len(id)%4)
    print(id)
    cursor.execute(
            f"INSERT INTO referals VALUES('{id}',{userid},'{name}','{bonus}',{0})")
    db.commit()
    return id
def get_referals(userid):
    cursor.execute(f"SELECT * FROM referals WHERE creatorid = {userid}")
    return cursor.fetchall()
def check_user_use_referals(referalid,userid):
    cursor.execute(f"SELECT * FROM usedreferals WHERE userid = {userid} AND referalid = '{referalid}'")
    if cursor.fetchone() != None:
        return False
    else:
        return True
def get_starts(referalid):
    cursor.execute(f"SELECT * FROM referals WHERE referalid = '{referalid}'")
    return int(cursor.fetchone()[4])
def add_use_to_referal(userid,referalid):
    cursor.execute(f"UPDATE referals SET starts = {get_starts(referalid)+1} WHERE referalid ='{referalid}'")
    db.commit()
    cursor.execute(f"INSERT INTO usedreferals VALUES ({userid},'{referalid}')")
    db.commit()
def getuserbychatid(chatid):
    cursor.execute(f"SELECT * FROM users WHERE chatid = {chatid}")
    return cursor.fetchone()
def gettokens(id):
    cursor.execute(f"SELECT * FROM users WHERE userid = {id}")
    return cursor.fetchone()


def editlastcall(id, call):
    cursor.execute(
        f"UPDATE users SET LastCall = '{call}' WHERE userid = {int(id)}")

    db.commit()


def editdate(id, date,type):
    cursor.execute(f"UPDATE users SET Dateofsubs = '{date}!{type}' WHERE userid = {int(id)}")
    db.commit()


def edittokens(id, tokens):
    cursor.execute(
        f"UPDATE users SET tokens= '{tokens}' WHERE userid = {int(id)}")
    db.commit()


def checkuser(id):
    cursor.execute(f"SELECT userid FROM users WHERE userid = {int(id)}")
    if cursor.fetchone() is None:
        return True
    else:

        return False


def createuser(id, chatid, tokens, Dateofsubs, typeOfSub):
    try:
        cursor.execute(
            f"INSERT INTO users VALUES({id},{chatid},{int(tokens)},'{Dateofsubs}','{typeOfSub}')")
        db.commit()
        return "ok"
    except:
        return "error"


def getallid():

    for i in cursor.execute("SELECT * FROM users"):
        print(i)
    return cursor.execute("SELECT * FROM users").fetchall()


def deleteusers(id):
    try:
        cursor.execute(f"DELETE FRON users WHERE ID = '{id}'")
        db.commit()
        return "ok"
    except:
        return "error"


def checkdate(id):
    user = gettokens(id)
    if user[3] == '-':
        return False
    date = user[3].split('!')[0]
    date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    if user[3].split('!')[1] == 'M':
        if (datetime.date.today() - date).days <= 30:
            return True
    if user[3].split('!')[1] == 'W':
        if (datetime.date.today() - date).days <= 7:
            return True
    if  user[3].split('!')[1] == 'U':
        return True
    else:
        return False
def addtonull(tokens):
    users = cursor.execute(f"SELECT * FROM users WHERE tokens = 0").fetchall()
    for i in users:

        cursor.execute(f"UPDATE users SET tokens= '{tokens}' WHERE userid = {int(i[0])}")
        db.commit()
    return len(users)       
def createpromo(name,count,tokens):
    cursor.execute(f"INSERT INTO promocodes VALUES('{name}',{count},{tokens})")
    db.commit()
def getpromo(promoname):
    promo = cursor.execute(f"SELECT * FROM promocodes WHERE promoname = '{promoname}'").fetchone()
    return promo
def checkpromo(promoname):
    promo = cursor.execute(f"SELECT * FROM promocodes WHERE promoname = '{promoname}'").fetchone()
    if promo == None or promo[1] == 0:
        return False
    else:
        return True
def mincount(promoname):
    cus = getpromo(promoname)[1] - 1
    if cus < 0:
        cus = 0
    cursor.execute(f"UPDATE promocodes SET usecount = {cus} WHERE promoname = '{promoname}'")
    db.commit()
def deletepromo(name):
    try:
        cursor.execute(f"DELETE FROM promocodes WHERE promoname = '{name}'")
        db.commit()
        return "ok"
    except:
        return "error"
def addusedpromo(userid,name):
    cursor.execute(f"INSERT INTO usedPromo VALUES({userid},'{name}')")
    db.commit()
def checkuse(userid,promoname):
    cursor.execute(f"SELECT * FROM usedPromo WHERE userid = {int(userid)} AND promoname = '{promoname}'")
    if cursor.fetchone() == None:
        return True
    else:
        return False

