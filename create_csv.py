# -*- coding: utf-8 -*-
import json
import sys
import csv

def create_dict_from_csv(filename):
    reader = csv.reader(open(filename))
    result = {}
    for row in reader:
        key = row[1]
        result[key] = row[2:]
    return result
    

filename = sys.argv[1]
output_file = open("tweets_by_user.csv", "w", encoding='utf-8')
output_file.write("user_id, text, lat, lon\n")
usr_locations = create_dict_from_csv("usrs_locations.csv")
print (usr_locations)
with open(filename,"r") as json_file:
    for line in json_file:
        tweet = json.loads(line)
        user_id = tweet["user_id"]
        print ("user_id: ", user_id)
        if not user_id in usr_locations:
            usr_locations[user_id] = [
                tweet['coordinates'][1],
                tweet['coordinates'][0]
            ]
        result = "{}, {}, {}, {}\n".format(
            user_id,
            (json.dumps(tweet["text"].replace("\"", ""))),
            usr_locations[user_id][0],
            usr_locations[user_id][1]
        )
        print(result)
        output_file.write(result)
output_file.close()
