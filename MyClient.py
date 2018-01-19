from fbchat import Client
import json
import requests
from fbchat.models import *

seen_users = {}

class MyClient(Client):

    # Get all threads that the current user is part of, up to limit
    # Returns a list of Thread objects
    def fetchThreads(self, limit=12):
        # Facebook deprecated the previous api call to get all threads, so the default from fbchat does not work
        # As such this uses a manual request

        # Need the cookies to verify the user
        cookies = self.getSession()


        # A lot of this data came from the request I was using to work out what needed to be sent
        # much of this probably doesn't need to be here
        data =  {      
            "batch_name" : "MessengerGraphQLThreadFetcherRe",
            "__user": self.uid,
            "__a": "1",
            "__dyn": "7AgNeS-aFoGi4Q9UrEwlg9odpbGAdy8-S-C11xG3F6wAxu13wFGEa8Gm4UJi28rxuF98qDKuEjKewExail0h8S6Uhx6byoW58nxGUOEixu1tyrgcUhxGbwYUmCK5UB1G6XDwEwSxqawDDgsxm1NDx6qUpCwCGm8xC784afBxm9yUvy8lUF3bDwgUgoKcU-q48x5x6789E-bQ6e4obAumUlwPzp4h2osAAw",
            "__req": "e",
            "__be": "-1",
            "__pc": "PHASED:messengerdotcom_pkg",
            "__rev": "3577900",
            "fb_dtsg": "AQEBd3GpaPIB:AQGDtDFO67wS",
            "jazoest": "2658169661005171112978073665865817168116687079545511983",
            "queries": '''{"o0":{"doc_id":"1349387578499440","query_params":{"limit": ''' + str(limit) + ''' , "before": 1516250688000, "tags":["INBOX"], "includeDeliveryReceipts":true, "includeSeqID":false}}}'''
            }

        # Sent a request for the threads
        r = requests.request(method="POST", url="https://www.messenger.com/api/graphqlbatch/", cookies= cookies, data=data)

        response = r.text

        # facebook sends back 2 json objects, the 2nd is just one saying that the request was a success
        # We only need the first object
        thread_info = response.split("\n")[0]

        thread_dict = json.loads(thread_info)

        # All of the data is nested many levels deep, thread_dict['o0']['data']['viewer']['message_threads']['nodes'] is a list of threads
        return self.create_threads_from_json(thread_dict['o0']['data']['viewer']['message_threads']['nodes'])

    # Creates thread objects from the json returned by a request for all threads
    # Also makes another request using self.fetchThreadInfo to avoid manually extracting all of the data when it's already been done
    def create_threads_from_json(self, json):

        # Get all of the threads so that we can call self.fetchThreadInfo on them to get the actual objects
        thread_ids = []

        for thread in json:
            # Extract the thread id from the json object
            thread_ids.append(self.get_thread_id_from_json(thread))

        # Get the actual thread objects
        return self.fetchThreadInfo(*thread_ids)

    # Extract the id of a thread from the json object passed in
    def get_thread_id_from_json(self, json):
        id_key = json['thread_key']

        # group chats have the thread id in json['thread_key']['thread_fbid'] while private messages just use the other user's id
        # as their thread id
        if id_key['thread_fbid']:
            thread_id = id_key['thread_fbid']
        else:
            thread_id = id_key['other_user_id']


        return thread_id

