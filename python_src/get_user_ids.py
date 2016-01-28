
# -*- coding: utf-8 -*-
import json
import sys
import pickle

USER_IDS = {}
filename = sys.argv[1]
out_filename = sys.argv[2]
ids_file = sys.argv[3]

#output_file = open("filtered_madrid_tweets_by_user", "w")
output_file = open(out_filename, "w")

user_ids = pickle.load(open(ids_file, "rb"))
print(filename)

def filter_users(min_tweets=3):
    return [ user_id for user_id, val in USER_IDS.items() if val >= min_tweets]

with open(filename,"r") as json_file:
    for line in json_file:
        tweet = json.loads(line)
        user_id = tweet["user_id"]
        if user_id in user_ids:
            output_file.write("{}".format(line))
    #     USER_IDS[user_id] = USER_IDS.get(user_id, 0) + 1
    
    # print(len(USER_IDS))
    # filtered_users = filter_users(min_tweets=2)
    # print(len(filtered_users))
    # pickle.dump(filtered_users, open("madrid_user_ids.p", "wb"))

    
