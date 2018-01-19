import db

print("Chats in database: {}".format([thread[1] for thread in db.get_all_threads()]))

print(db.get_all_users())

chat = input("Which chat do you want to check? ")
print("People in {}: {}".format(chat, db.get_users_in_chat(chat)))

