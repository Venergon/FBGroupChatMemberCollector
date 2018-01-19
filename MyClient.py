from fbchat import Client
import json
import requests
from fbchat.models import *

seen_users = {}

class MyClient(Client):


    def fetchThreads(self, limit=12):
        cookies = self.getSession()

        data =  {      
            "batch_name" : "MessengerGraphQLThreadFetcherRe",
            "__user": "100005216200900",
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

        r = requests.request(method="POST", url="https://www.messenger.com/api/graphqlbatch/", cookies= cookies, data=data)

        response = r.text

        thread_info = response.split("\n")[0]

        thread_dict = json.loads(thread_info)

        return self.create_threads_from_json(thread_dict['o0']['data']['viewer']['message_threads']['nodes'])


    def create_threads_from_json(self, json):
        thread_ids = []

        for thread in json:
            thread_ids.append(self.get_thread_id_from_json(thread))

        return self.fetchThreadInfo(*thread_ids)


    def get_thread_id_from_json(self, json):
        id_key = json['thread_key']

        if id_key['thread_fbid']:
            thread_id = id_key['thread_fbid']
        else:
            thread_id = id_key['other_user_id']


        return thread_id

