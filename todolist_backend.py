#To-Do List App for organizing and monitoring tasks that need to be completed
#tasks rated by priority from 1-3, 1 being high priority and 3 being low priority


import sqlite3
DB = "to_do_list.db"

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS 
            to_do_list(
                task TEXT NOT NULL,
                finished INTEGER NOT NULL DEFAULT 0,
                priority INTEGER NOT NULL DEFAULT 3
                CHECK (priority BETWEEN 1 AND 3),
                comment TEXT NOT NULL
            )"""
        )


def add_task(task, priority, comment):
    with sqlite3.connect(DB) as conn:
        conn.execute(
            "INSERT INTO to_do_list ("
                "task, finished, "
                "priority, comment) "
                "VALUES (?, ?, ?, ?)",
                (task, 0, priority, comment))
    print(f"{task} has been created successfully")


def complete_task(task):
    with sqlite3.connect(DB) as conn:
        cur = conn.execute(
            "UPDATE to_do_list SET finished = 1 "
                "WHERE task = ?",
            (task,))
        if cur.rowcount == 0:
            print("Task not found.")
        conn.commit()


def remove_task(task):
    with sqlite3.connect(DB) as conn:
        cur = conn.execute(
            "DELETE FROM to_do_list WHERE task = ?",
            (task, ))
        if cur.rowcount == 0:
            print("Task not found.")


def fetch_all_tasks():
    with sqlite3.connect(DB) as conn:
        cur = conn.execute(
            "SELECT task, finished, priority, comment "
            "FROM to_do_list "
            "ORDER BY finished ASC, priority ASC")
        return cur.fetchall()

def truncate_table():
    with sqlite3.connect(DB) as conn:
        cur = conn.execute("DELETE FROM to_do_list")
        conn.commit()