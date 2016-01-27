from TwitterAPI import TwitterAPI
from custom_rest_pager import CustomTwitterRestPager
import pickle
import json
import os

API_KEY = "NVLAVt1xdqPreKI3VyQ34NzF2"
API_SECRET = "xPsPZlq2Sneoq2hURZ1TUgc4GKQb87gSydFuOq3XYSY5oUKmnZ"

ACCESS_TOKEN = "148570539-qsHNBavdtJcLLVEdHDxNFeNRTfmFiKQ74FZ08FK1"
ACCESS_TOKEN_SECRET = "9QwtTxAsE3ACYhSImjiem5UxGOuvfMduukEpz7b0B1iTp"

api = TwitterAPI(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
user_ids = pickle.load(open("user_ids.p", "rb"))

print (len(user_ids), "user_ids")


for i, user_id in enumerate(user_ids[:27] + user_ids[28:]):
    counter = 0
    user_tweets_file = open("users_tweets/{}_tweets.txt".format(user_id), "w")
    user_coords_file = open("users_coords/{}".format(user_id), "w")

    user_coords_file.write("lon, lat\n")
    r = CustomTwitterRestPager(api, 'statuses/user_timeline', {'user_id':user_id, 'count':200}, max_requests=3)
    for item in r.get_iterator():
        if 'text' in item:
            tweet = {key:item.get(key) for key in ["text", "created_at"]}
            coords = item.get("coordinates", None)
            if coords:
                if 'coordinates' in coords:
                    counter += 1
                    lon, lat = coords['coordinates']
                    user_coords_file.write(
                        "{}, {}\n".format(lon, lat)
                    )
            user_tweets_file.write("{}\n".format(json.dumps(tweet)))
        elif 'message' in item and item['code'] == 88:
            print ('SUSPEND, RATE LIMIT EXCEEDED: %s\n' % item['message'])
            break
    print(i,": user ", user_id, "num localized tweets: ", counter)
    #user_coords_file.write(json.dumps(user_coordinates))

    user_coords_file.close()
    user_tweets_file.close()
