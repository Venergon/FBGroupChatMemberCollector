from fbchat.models import *
import os
import sqlite3

#try to connect to the database, and create a new one if it does not exist
if os.path.exists('database.db'): 
    conn = sqlite3.connect('database.db')
else:
    conn = sqlite3.connect('database.db')
    conn.executescript(open('init.sql').read()) # read from file if the database does not exist

# Saves a list of users into the database
# Ignores any users that are already in the database
def save_users(users):
    cursor = conn.cursor()

    for user in users:
        save_user(user, cursor)

    conn.commit()
    cursor.close()

# Saves a single user into the database
# If the user is already in the database, this does nothing
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


# Saves a list of threads (chats) into the database
# Along with all of the participants of each chat
# Ignores any chats that are already in the database
def save_threads(threads, current_user_id):
    cursor = conn.cursor()

    for thread in threads.values():
        save_thread(thread, current_user_id, cursor)

    conn.commit()
    cursor.close()


# Saves a single thread (chat) into the database
# Along with all the participants in the chat
# If the thread is already in the database it isn't put in again
# but any participants that weren't already in the database are still added
def save_thread(thread, current_user_id, cursor):
    # Work out whether this is a chat directly with a person ("User")
    # or a group chat ("Group")
    if thread.type == ThreadType.USER:
        thread_type = "User"
    else:
        thread_type = "Group"


    # Before saving the thread, check the thread does not already exist in the database
    existing_thread = cursor.execute(
                            """SELECT * FROM threads
                                WHERE id = ?""",
                                (thread.uid,)).fetchall()

    if not existing_thread:
        # The thread does not exist, we can add it
        cursor.execute(
            """INSERT INTO threads(id, name, type)
                VALUES (?, ?, ?)""", 
                (thread.uid, thread.name, thread_type))


    # Add all of the participants in this thread to the database

    if thread_type == "User":
        # A user has themselves and the current user as the only participants
        save_participants(thread.uid, set([thread.uid, current_user_id]), cursor)

    else:
        # Need to add all of the participants of the group
        save_participants(thread.uid, thread.participants, cursor)

# Save a list of participants to a single thread into the database
# Ignores any users that are already participants of this thread
def save_participants(thread_id, participants, cursor):
    for participant in participants:
        # first check this participant does not already exist
        existing_participant = cursor.execute(
                            """SELECT * FROM participants
                                WHERE thread_id = ?
                                AND user_id = ?""",
                                (thread_id, participant)).fetchall()

        if not existing_participant:
            # Participant is not in the database, add it
            cursor.execute(
                """INSERT INTO participants(thread_id, user_id)
                    VALUES (?, ?)""",
                    (thread_id, participant))


# Get all info about every thread in the database
# Does not include participants because that is a separate table
def get_all_threads():
    cursor = conn.cursor()
    
    results = cursor.execute("""SELECT * from threads""")

    results = results.fetchall()

    cursor.close()

    return results

# Get all info about every user in the database
def get_all_users():
    cursor = conn.cursor()

    results = cursor.execute("""SELECT * from users""")

    results = results.fetchall()

    cursor.close()

    return results


# Get the names of every participant in a particular chat
# Where chat_name is the name of the chat
# TODO: disambiguate if there are multiple chats with the same name
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
