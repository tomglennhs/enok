from enum import Enum
from config import config
from pydantic import BaseModel
import sqlite3
from typing import List, Optional
con = sqlite3.connect('enok.db', check_same_thread=False)

cur = con.cursor()
# db initialization stuff
# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS users
               (id INTEGER PRIMARY KEY, name TEXT, email TEXT UNIQUE, password TEXT, role INT DEFAULT 0, quota REAL, login_provider TEXT)''')

cur.execute('''CREATE TABLE IF NOT EXISTS printers
               (id INTEGER PRIMARY KEY, name TEXT, ip TEXT, camera TEXT, type TEXT, queue TEXT, upload_method TEXT)''')


cur.execute('''CREATE TABLE IF NOT EXISTS job_files
               (id INTEGER PRIMARY KEY, filepath TEXT, filament_length REAL, user_id int, FOREIGN KEY (user_id) REFERENCES users(id))''')

cur.execute('''CREATE TABLE IF NOT EXISTS job_history
               (id INTEGER PRIMARY KEY, time_started DATETIME DEFAULT CURRENT_TIMESTAMP, time_finished DATETIME, status TEXT, job_file_id int, printer_id int, FOREIGN KEY (job_file_id) REFERENCES job_files(id), FOREIGN KEY (printer_id) REFERENCES printers(id))''')

try:
    # Insert a row of data
    cur.execute('''INSERT INTO users (name, email, password, quota, login_provider) VALUES ('JASON', 'Jason@gmail.com', '######', 10000, 'gmail')''')
    cur.execute('''INSERT INTO users (name, email, password, quota, login_provider) VALUES ('JOSEPH', 'Joseph@hotmail.com', '######', 5000, 'username')''')
    cur.execute(
        '''INSERT INTO printers (name, ip, camera, type, queue) VALUES ('dremel', '', '', 'dremel', '{\"queue\":[["file.gcode", {"UploadMethod": "USB", "Owner": 1}], ["file2.gcode",{"UploadMethod": "Network", "Owner": 2}]]}')''')

    # Save (commit) the changes"queue":[["file.gcode", {"UploadMethod": "USB, "Owner": 1}], ["file2.gcode",{"UploadMethod": "Network", "Owner": 2}]]}
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
    print(param[0])
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

# Update printers


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


class JobFile(BaseModel):
    id: int
    filepath: str
    filament_length: float
    user_id: int


class Role(Enum):
    # Users that are not certified to use printers.
    VIEW_ONLY = 0
    # Users that are certified to use printers.
    STANDARD = 1
    # Users that have super user privileges.
    ADMIN = 2


class User(BaseModel):
    id: int
    name: str
    email: str
    password: Optional[str]
    role: Role
    quota: float
    login_provider: str

class JobHistory(BaseModel):
    id: int
    time_started: str
    time_finished: str
    status: str
    job_file_id: int
    printer_id: int

def get_job_file(id) -> JobFile:
    job_file = cur.execute(
        "SELECT id, filepath, filament_length, user_id FROM job_files WHERE id = ?", (id,)).fetchone()
    id, filepath, filament_length, user_id = job_file
    return JobFile(id=id, filepath=filepath, filament_length=filament_length, user_id=user_id)


def get_job_files_by_user(user_id) -> List[JobFile]:
    files = []
    job_file = cur.execute(
        "SELECT id, filepath, filament_length, user_id FROM job_files WHERE user_id = ?", (user_id,)).fetchall()
    for job in job_file:
        id, filepath, filament_length, user_id = job
        files.append(JobFile(id=id, filepath=filepath,
                     filament_length=filament_length, user_id=user_id))
    return files


def get_all_job_files() -> List[JobFile]:
    files = []
    job_file = cur.execute(
        "SELECT id, filepath, filament_length, user_id FROM job_files").fetchall()
    for job in job_file:
        id, filepath, filament_length, user_id = job
        files.append(JobFile(id=id, filepath=filepath,
                     filament_length=filament_length, user_id=user_id))
    return files


def get_user_by_email(e: str) -> User:
    user = cur.execute("SELECT * FROM users WHERE email = ?",
                       (e,)).fetchone()
    id, name, email, password, role, quota, login_provider = user
    return User(id=id, name=name, email=email, password=password, role=role, quota=quota, login_provider=login_provider)


def add_job(filepath: str, filament_length: float, user_id: str):
    cur.execute("INSERT INTO job_files (filepath, filament_length, user_id) VALUES (?, ?, ?)",
                (filepath, filament_length, user_id))
    con.commit()


def delete_job(id: int):
    cur.execute("DELETE FROM job_files WHERE id = ?", (id,))
    con.commit()


def get_user_by_id(id: str) -> User:
    user = cur.execute("SELECT * FROM users WHERE id = ?", (id,)).fetchone()
    id, name, email, password, role, quota, login_provider = user
    return User(id=id, name=name, email=email, password=password, role=role, quota=quota, login_provider=login_provider)


def create_user(name: str, email: str,
                login_provider: str = "local", password: Optional[str] = None, role: Role = Role.VIEW_ONLY, quota: float = config.default_user_quota):
    cur.execute('''INSERT INTO users (name, email, login_provider, password, role, quota) VALUES (?, ?, ?, ?, ?, ?)''',
                (name, email, login_provider, password, role, quota)).fetchone()
    con.commit()
    return get_user_by_email(email)

def get_history_by_job_id(id: int):
    history = cur.execute("SELECT * FROM job_history WHERE job_id = ?", (id,)).fetchall()
    return history