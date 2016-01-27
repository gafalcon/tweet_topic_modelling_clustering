# -*- coding: utf-8 -*-
import json
import sys
import csv
from langdetect import detect

def count_languages(filename):
    langs = {}
    reader = csv.reader(open(filename))
    for row in reader:
        key = row[4]
        langs[key] = langs.get(key, 0) + 1
    return langs


def detect_language_csv():    
    output_file = open("tweets_by_user_lang.csv", "w", encoding='utf-8')
    reader = csv.reader(open("tweets_by_user.csv"), skipinitialspace=True, quotechar='"' )
    output_file.write("user_id, text, lat, lon, lang\n")
    for row in reader:
        lang = detect(row[1])
        print(row)
        output_file.write("{}, {}, {}, {}, {}\n".format(
            row[0],
            (json.dumps(row[1].replace("\"", ""))),
            row[2],
            row[3],
            lang
        ))
    output_file.close()

def filter_by_language(lang, infile, outfile):
    output_file = open(outfile, "w", encoding='utf-8')
    output_file.write("user_id, text, lat, lon, lang\n")
    reader = csv.reader(open(infile), skipinitialspace=True, quotechar='"' )
    for row in reader:
        print(row[4])
        print(len(row[4]))
        if lang == row[4]:
            output_file.write("{}, {}, {}, {}, {}\n".format(
                row[0],
                (json.dumps(row[1].replace("\"", ""))),
                row[2],
                row[3],
                lang
            ))   
    output_file.close()
    
#print(count_languages("tweets_by_user_lang.csv"))
#detect_language_csv()
filter_by_language("fr", "tweets_by_user_lang.csv", "fr_tweets.csv")
filter_by_language("en", "tweets_by_user_lang.csv", "en_tweets.csv")

# filename = sys.argv[1]
# output_file = open("tweets_by_user.csv", "w", encoding='utf-8')
# output_file.write("user_id, text, lat, lon\n")
# usr_locations = create_dict_from_csv("usrs_locations.csv")
# print (usr_locations)
# with open(filename,"r") as json_file:
#     for line in json_file:
#         tweet = json.loads(line)
#         user_id = tweet["user_id"]
#         print ("user_id: ", user_id)
#         if not user_id in usr_locations:
#             usr_locations[user_id] = [
#                 tweet['coordinates'][1],
#                 tweet['coordinates'][0]
#             ]
#         result = "{}, {}, {}, {}\n".format(
#             user_id,
#             (json.dumps(tweet["text"].replace("\"", ""))),
#             usr_locations[user_id][0],
#             usr_locations[user_id][1]
#         )
#         print(result)
#         output_file.write(result)
