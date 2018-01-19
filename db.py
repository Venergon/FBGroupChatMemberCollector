from fbchat.models import *
import os
import sqlite3

#try to connect to the database, and create a new one if it does not exist
if os.path.exists('database.db'): 
    conn = sqlite3.connect('database.db')
else:
    conn = sqlite3.connect('database.db')
    conn.executescript(open('init.sql').read()) # read from file if the database does not exist

def save_users(users):
    cursor = conn.cursor()

    for user in users.values():
        save_user(user, cursor)

    conn.commit()
    cursor.close()

def save_user(user, cursor):

    # First check the user does not already exist
    existing_user = cursor.execute(
                            """SELECT * FROM users
                                WHERE id = ?""",
                                (user.uid,)).fetchall()

    if not existing_user:
        cursor.execute(
            """INSERT INTO users(id, first_name, last_name, full_name)
                VALUES (?, ?, ?, ?)""",
                (user.uid, user.first_name, user.last_name, user.name))


def save_threads(threads, current_user_id):
    cursor = conn.cursor()

    for thread in threads.values():
        save_thread(thread, current_user_id, cursor)

    conn.commit()
    cursor.close()


def save_thread(thread, current_user_id, cursor):
    if thread.type == ThreadType.USER:
        thread_type = "User"
    else:
        thread_type = "Group"

    # First check the thread does not already exist
    existing_thread = cursor.execute(
                            """SELECT * FROM threads
                                WHERE id = ?""",
                                (thread.uid,)).fetchall()

    if not existing_thread:
        cursor.execute(
            """INSERT INTO threads(id, name, type)
                VALUES (?, ?, ?)""", 
                (thread.uid, thread.name, thread_type))

    if thread_type == "User":
        # A user has themselves as the only participant
        save_participants(thread.uid, set([thread.uid, current_user_id]), cursor)

    else:
        # Need to add all of the participants of the group
        save_participants(thread.uid, thread.participants, cursor)

def save_participants(thread_id, participants, cursor):
    for participant in participants:
        # first check this participant does not already exist
        existing_participant = cursor.execute(
                            """SELECT * FROM participants
                                WHERE thread_id = ?
                                AND user_id = ?""",
                                (thread_id, participant)).fetchall()

        if not existing_participant:
            cursor.execute(
                """INSERT INTO participants(thread_id, user_id)
                    VALUES (?, ?)""",
                    (thread_id, participant))



def get_all_threads():
    cursor = conn.cursor()
    
    results = cursor.execute("""SELECT * from threads""")

    results = results.fetchall()

    cursor.close()

    return results

def get_all_users():
    cursor = conn.cursor()

    results = cursor.execute("""SELECT * from users""")

    results = results.fetchall()

    cursor.close()

    return results


def get_users_in_chat(chat_name):
    cursor = conn.cursor()

    results = cursor.execute("""SELECT users.full_name from users
                                INNER JOIN participants ON users.id = participants.user_id
                                INNER JOIN threads ON participants.thread_id = threads.id
                                WHERE threads.name = ?""",
                                (chat_name, ))

    results = results.fetchall()

    cursor.close()
    
    return results
