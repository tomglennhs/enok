from typing import Optional

from config import config
from db import cur, User, Role, con


def get_user_param(id, *param):
    if (len(param) == 1):
        return cur.execute("SELECT " + str(i) +
                           " FROM users WHERE ROWID = ?", (id,)).fetchone()
    elif (len(param) > 1):
        user_param = []
        for i in param:
            user_param.append(cur.execute("SELECT " + str(i) +
                                          " FROM users WHERE ROWID = ?", (id,)).fetchone())
        return user_param
    else:
        return None


def get_user_by_email(e: str) -> User:
    user = cur.execute("SELECT * FROM users WHERE email = ?",
                       (e,)).fetchone()
    id, name, email, password, role, quota, login_provider = user
    return User(id=id, name=name, email=email, password=password, role=role, quota=quota, login_provider=login_provider)


def get_user_by_id(id: str) -> User:
    user = cur.execute("SELECT * FROM users WHERE id = ?", (id,)).fetchone()
    id, name, email, password, role, quota, login_provider = user
    return User(id=id, name=name, email=email, password=password, role=role, quota=quota, login_provider=login_provider)


def create_user(name: str, email: str,
                login_provider: str = "local", password: Optional[str] = None, role: Role = Role.VIEW_ONLY,
                quota: float = config.default_user_quota):
    cur.execute('''INSERT INTO users (name, email, login_provider, password, role, quota) VALUES (?, ?, ?, ?, ?, ?)''',
                (name, email, login_provider, password, role, quota)).fetchone()
    con.commit()
    return get_user_by_email(email)


def update_user_quota(user_id: int, quota: float):
    cur.execute("UPDATE users SET quota = ? WHERE id = ?", (quota, user_id))
    con.commit()