from typing import List

from db import cur, JobFile, con, JobHistory


def recall_job(job_id: int):
    job = cur.execute(
        "SELECT * FROM job_history WHERE ROWID = ?", (job_id,)).fetchall()
    return job


def get_job_file(file_id: int) -> JobFile:
    job_file = cur.execute(
        "SELECT id, filepath, filament_length, user_id FROM job_files WHERE id = ?", (file_id,)).fetchone()
    file_id, filepath, filament_length, user_id = job_file
    return JobFile(id=file_id, filepath=filepath, filament_length=filament_length, user_id=user_id)


def get_job_files_by_user(user_id: int) -> List[JobFile]:
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


def add_job(filepath: str, filament_length: float, user_id: int) -> int:
    cur.execute("INSERT INTO job_files (filepath, filament_length, user_id) VALUES (?, ?, ?)",
                (filepath, filament_length, user_id))
    con.commit()
    return cur.lastrowid


def delete_job(job_id: int):
    cur.execute("DELETE FROM job_files WHERE id = ?", (job_id,))
    con.commit()


def get_history_by_job_id(job_id: int) -> List[JobHistory]:
    arr = []
    history = cur.execute("SELECT * FROM job_history WHERE job_file_id = ?", (job_id,)).fetchall()
    for entry in history:
        job_id, time_started, time_finished, status, job_file_id, printer_id = entry
        arr.append(JobHistory(id=job_id, time_started=time_started, time_finished=time_finished, status=status,
                              job_file_id=job_file_id, printer_id=printer_id))
    return arr


def update_job_filament_len(job_id: int, length: float):
    cur.execute("UPDATE job_files SET filament_length = ? WHERE id = ?", (length, job_id))
    con.commit()
