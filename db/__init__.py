import sqlite3

from db.models import JobFile, User, JobHistory, Role

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
    cur.execute(
        '''INSERT INTO users (name, email, password, quota, login_provider) VALUES ('JASON', 'Jason@gmail.com', '######', 10000, 'gmail')''')
    cur.execute(
        '''INSERT INTO users (name, email, password, quota, login_provider) VALUES ('JOSEPH', 'Joseph@hotmail.com', 
        '######', 5000, 'username')''')
    cur.execute(
        '''INSERT INTO printers (name, ip, camera, type, queue) VALUES ('dremel', '', '', 'dremel', '{\"queue\":[[
        "file.gcode", {"UploadMethod": "USB", "Owner": 1}], ["file2.gcode",{"UploadMethod": "Network", 
        "Owner": 2}]]}')''')

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
