import getpass

from fbchat.models import *
from MyClient import MyClient
import db


def get_all_users(threads, client):
    user_ids = set()


    # Get all of the unique user ids
    for thread in threads.values():
        if thread.type == ThreadType.USER:
            # users don't have participants but should themselves be added
            user_ids.add(thread.uid)
        else:
            for user in thread.participants:
                user_ids.add(user)

    users = client.fetchUserInfo(*user_ids)

    return users





username = input("Enter username: ")
password = getpass.getpass("Enter password: ")

client = MyClient(username, password)


threads = client.fetchThreads(limit = 1000)

users = get_all_users(threads, client)
db.save_users(users)

db.save_threads(threads, client.uid)


client.logout()






