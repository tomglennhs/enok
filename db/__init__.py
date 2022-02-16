import sqlite3
con = sqlite3.connect('enok.db', check_same_thread=False)

cur = con.cursor()
# db initialization stuff
# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS users
               (date text, trans text, symbol text, qty real, price real)''')

# Insert a row of data
cur.execute("INSERT INTO users VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes
con.commit()

def getUsers():
    users = cur.execute("SELECT * FROM users").fetchall()
    return users