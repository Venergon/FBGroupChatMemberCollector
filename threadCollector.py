import getpass

from fbchat.models import *
from MyClient import MyClient
import db


# From a set of threads, gets a list of User objects for all of the users in the threads 
def get_all_users(threads, client):
    # Work out the ids of the users so all of the User objects can be made in one request
    # A set is used since users can be in multiple chats, and there's no point retrieving data about them multiple times
    user_ids = set()

    # Add the current user
    user_ids.add(client.uid)


    # Get all of the unique user ids
    for thread in threads.values():

        # Check whether this thread is a private message or a group chat
        if thread.type == ThreadType.USER:
            # users don't have participants but should themselves be added
            user_ids.add(thread.uid)
        else:
            # Add in all the participants of this chat
            for user in thread.participants:
                user_ids.add(user)

    # Fetch all of the actual user objects for these user ids
    users = client.fetchUserInfo(*user_ids)

    return users




# Get login details and log in
username = input("Enter username: ")
password = getpass.getpass("Enter password: ")

client = MyClient(username, password)


# Get all of the threads that the current user is part of (assuming that no one is part of more than 1000 chats,
# If it needs to use more than 1000 chats then just increase the limit
threads = client.fetchThreads(limit = 1)

# Get the user objects of all the participants of all the chats
users = get_all_users(threads, client)

# Save all of the users in the database
db.save_users(users.values())

# Save all of the threads and participants in those threads in the database
db.save_threads(threads.values(), client.uid)


client.logout()






