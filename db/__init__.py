import sqlite3
con = sqlite3.connect('enok.db', check_same_thread=False)

cur = con.cursor()
# db initialization stuff
# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS users
               (id integer primary key, name TEXT, email TEXT, password TEXT, role INT, quota REAL, login_provider TEXT)''')

cur.execute('''CREATE TABLE IF NOT EXISTS printers
               (id integer primary key, name TEXT, ip TEXT, camera TEXT, type TEXT, queue TEXT)''')


cur.execute('''CREATE TABLE IF NOT EXISTS job_files
               (id integer primary key, filepath TEXT, filament_length REAL, user_id int, FOREIGN KEY (user_id) REFERENCES users(id))''')

cur.execute('''CREATE TABLE IF NOT EXISTS job_history
               (id integer primary key, time_started DEFAULT CURRENT_TIMESTAMP, time_finished TIMESTAMP, status TEXT, job_file_id int, printer_id int, FOREIGN KEY (job_file_id) REFERENCES job_files(id), FOREIGN KEY (printer_id) REFERENCES printers(id))''')

# Insert a row of data
cur.execute('''INSERT INTO users (name, email, password, role, quota, login_provider) VALUES ('JASON', 'Jason@gmail.com', '######', 1, 10000, 'gmail')''')
cur.execute('''INSERT INTO users (name, email, password, role, quota, login_provider) VALUES ('JOSEPH', 'Joseph@hotmail.com', '######', 0, 5000, 'username')''')

# Save (commit) the changes
con.commit()


def getUsers():
    users = cur.execute("SELECT * FROM users").fetchall()
    return users
