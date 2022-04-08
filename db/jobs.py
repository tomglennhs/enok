from typing import List

from db import cur, JobFile, con, JobHistory


def recall_job(id):
    job = cur.execute(
        "SELECT * FROM job_history WHERE ROWID = ?", (id,)).fetchall()
    return job


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


def add_job(filepath: str, filament_length: float, user_id: int):
    cur.execute("INSERT INTO job_files (filepath, filament_length, user_id) VALUES (?, ?, ?)",
                (filepath, filament_length, user_id))
    con.commit()


def delete_job(id: int):
    cur.execute("DELETE FROM job_files WHERE id = ?", (id,))
    con.commit()


def get_history_by_job_id(id: int) -> List[JobHistory]:
    arr = []
    history = cur.execute("SELECT * FROM job_history WHERE job_file_id = ?", (id,)).fetchall()
    for entry in history:
        id, time_started, time_finished, status, job_file_id, printer_id = entry
        arr.append(JobHistory(id=id, time_started=time_started, time_finished=time_finished, status=status,
                              job_file_id=job_file_id, printer_id=printer_id))
    return arr