import sqlite3
from typing import Optional
con = sqlite3.connect('enok.db', check_same_thread=False)

cur = con.cursor()
# db initialization stuff
# Create table
default = 0
cur.execute('''CREATE TABLE IF NOT EXISTS users
               (id integer primary key, name TEXT, email TEXT UNIQUE, password TEXT, role INT DEFAULT 0, quota REAL, login_provider TEXT)''')

cur.execute('''CREATE TABLE IF NOT EXISTS printers
               (id integer primary key, name TEXT, ip TEXT, camera TEXT, type TEXT, queue TEXT)''')


cur.execute('''CREATE TABLE IF NOT EXISTS job_files
               (id integer primary key, filepath TEXT, filament_length REAL, user_id int, FOREIGN KEY (user_id) REFERENCES users(id))''')

cur.execute('''CREATE TABLE IF NOT EXISTS job_history
               (id integer primary key, time_started DEFAULT CURRENT_TIMESTAMP, time_finished TIMESTAMP, status TEXT, job_file_id int, printer_id int, FOREIGN KEY (job_file_id) REFERENCES job_files(id), FOREIGN KEY (printer_id) REFERENCES printers(id))''')


try:
    # Insert a row of data
    cur.execute('''INSERT INTO users (name, email, password, quota, login_provider) VALUES ('JASON', 'Jason@gmail.com', '######', 10000, 'gmail')''')
    cur.execute('''INSERT INTO users (name, email, password, quota, login_provider) VALUES ('JOSEPH', 'Joseph@hotmail.com', '######', 5000, 'username')''')
    # Save (commit) the changes
    con.commit()
except sqlite3.IntegrityError:
    pass

# Pull general information
def get_table_data(*tables):
    table_data = []
    for table in tables:
        table_data.append(cur.execute(
            "SELECT ROWID, * FROM " + str(table)).fetchall())
    return table_data

# Pull information for users


def get_user_param(id, *param):
    user_param = []
    for i in param:
        user_param.append(cur.execute("SELECT " + str(i) +
                          " FROM users WHERE ROWID = ?", (id,)).fetchone())
    return user_param

# Pull information for printers


def get_printer(id):
    printer = cur.execute(
        "SELECT * FROM printers WHERE ROWID = ?", (id,)).fetchall()
    return printer

# Pull infromation for Job_History


def recall_job(id):
    job = cur.execute(
        "SELECT * FROM job_history WHERE ROWID = ?", (id,)).fetchall()
    return job

# Pull information for Job_Files


def get_job_file(id):
    job_file = cur.execute(
        "SELECT * FROM job_files WHERE ROWID = ?", (id,)).fetchall()
    return job_file


def get_user_by_email(email: str):
    user = cur.execute("SELECT * FROM users WHERE email = ?",
                       (email,)).fetchone()
    return user


def get_user_by_id(id: str):
    user = cur.execute("SELECT * FROM users WHERE id = ?", (id,)).fetchone()
    return user


def create_user(name: str, email: str,
                login_provider: str = "local", password: Optional[str] = None,):
    cur.execute('''INSERT INTO users (name, email, login_provider, password) VALUES (?, ?, ?)''',
                (name, email, login_provider, password)).fetchone()
    con.commit()
    return get_user_by_email(email)
