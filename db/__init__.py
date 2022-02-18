import sqlite3
con = sqlite3.connect('enok.db', check_same_thread=False)

cur = con.cursor()
# db initialization stuff
# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS users
               (name TEXT, email TEXT, password TEXT, role BOOLEAN, quota INT, login_provider TEXT)''')


cur.execute('''CREATE TABLE IF NOT EXISTS printers
               (name TEXT, ip TEXT, camera TEXT, type TEXT, queue TEXT, uid TEXT)''')

cur.execute('''CREATE TABLE IF NOT EXISTS job_files
               (file_uid TEXT, filepath TEXT, filament_length INT)''')

cur.execute('''CREATE TABLE IF NOT EXISTS job_history
               (time_started DEFAULT CURRENT_TIMESTAMP, time_finished TIMESTAMP, status TEXT, jfid TEXT, pid TEXT)''')


# Insert a row of data
cur.execute('''INSERT INTO users VALUES ('JASON', 'Jason@gmail.com', '######', 1, 10000, 'gmail')''')
cur.execute('''INSERT INTO users VALUES ('JOSEPH', 'Joseph@hotmail.com', '######', 0, 5000, 'username')''')

# Save (commit) the changes
con.commit()

def getUsers():
    users = cur.execute("SELECT ROWID, * FROM users").fetchall()
    return users