# -*- coding: utf-8 -*-
import json
import sys
import csv

infile_json = sys.argv[1]
infile_csv = sys.argv[2]
outfile_csv = sys.argv[3]


def create_dict_from_csv(filename):
    reader = csv.reader(open(filename))
    result = {}
    for row in reader:
        key = row[1]
        result[key] = row[2:]
    return result
    
def separate_clusters_in_csvs(infile, out_dir, clusters):
    reader = csv.reader(open(infile))
    clusters = [open("{}/cluster{}.csv".format(out_dir, i), "w") for i in range(0,int(clusters))]
    print(clusters)
    for row in reader:
        print(row)
    for cluster in clusters:
        cluster.close()

#separate_clusters_in_csvs(sys.argv[1], sys.argv[2], sys.argv[3])

#output_file = open("tweets_by_user.csv", "w", encoding='utf-8')
output_file = open(outfile_csv, "w", encoding='utf-8')
output_file.write("user_id, text, lat, lon\n")

usr_locations = create_dict_from_csv(infile_csv)
print (usr_locations)
with open(infile_json,"r") as json_file:
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
