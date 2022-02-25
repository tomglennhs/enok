import sqlite3
from typing import Optional
con = sqlite3.connect('enok.db', check_same_thread=False)

cur = con.cursor()
# db initialization stuff
# Create table
default = 0
cur.execute('''CREATE TABLE IF NOT EXISTS users
               (id INTEGER PRIMARY KEY, name TEXT, email TEXT UNIQUE, password TEXT, role INT DEFAULT 0, quota REAL, login_provider TEXT)''')

cur.execute('''CREATE TABLE IF NOT EXISTS printers
               (id INTEGER PRIMARY KEY, name TEXT, ip TEXT, camera TEXT, type TEXT, queue TEXT)''')


cur.execute('''CREATE TABLE IF NOT EXISTS job_files
               (id INTEGER PRIMARY KEY, filepath TEXT, filament_length REAL, user_id int, FOREIGN KEY (user_id) REFERENCES users(id))''')

cur.execute('''CREATE TABLE IF NOT EXISTS job_history
               (id INTEGER PRIMARY KEY, time_started DEFAULT CURRENT_TIMESTAMP, time_finished TIMESTAMP, status TEXT, job_file_id int, printer_id int, FOREIGN KEY (job_file_id) REFERENCES job_files(id), FOREIGN KEY (printer_id) REFERENCES printers(id))''')

try:
    # Insert a row of data
    cur.execute('''INSERT INTO users (name, email, password, quota, login_provider) VALUES ('JASON', 'Jason@gmail.com', '######', 10000, 'gmail')''')
    cur.execute('''INSERT INTO users (name, email, password, quota, login_provider) VALUES ('JOSEPH', 'Joseph@hotmail.com', '######', 5000, 'username')''')
    cur.execute('''INSERT INTO printers (name, ip, camera, type, queue) VALUES ('dremel', '', '', 'dremel', '{\"queue\":[["file.gcode", {"UON": false, "Owner": 1}], ["file2.gcode",{"UON": true, "Owner": 2}]]}')''')
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
    if(len(param) == 1):
        return cur.execute("SELECT " + str(i) +
                            " FROM users WHERE ROWID = ?", (id,)).fetchone()
    elif(len(param) > 1):
        user_param = []
        for i in param:
            user_param.append(cur.execute("SELECT " + str(i) +
                            " FROM users WHERE ROWID = ?", (id,)).fetchone())
        return user_param
    else:
        return None

# Pull information for printers

def get_printer_param(id, *param):
    if(len(param) == 1):
        return cur.execute("SELECT " + str(param[0]) + 
                            " FROM printers WHERE ROWID = ?", (id,)).fetchone()[0]
    elif(len(param) > 1):
        printer_param = []
        for i in param:
            printer_param.append(cur.execute("SELECT " + str(i) +
                            " FROM printers WHERE ROWID = ?", (id,)).fetchone())
        return printer_param
    else:
        return None

#Update printers
def set_queue(queue, id):
    cur.execute("UPDATE printers SET queue = \'" + queue +  
                            "\' WHERE ROWID = ?", (id,))
    con.commit()
    
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
