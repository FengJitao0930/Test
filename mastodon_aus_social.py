
# need to install couchdb
import couchdb
import json
# need to install mastodon.py
from mastodon import Mastodon, StreamListener
import re

# connect to the couchdb
admin = 'cccadmin'
password = 'whysohard24!'

# send request to couchdb
url = f'http://{admin}:{password}@127.0.0.1:5984/'
couch = couchdb.Server(url)

# create a couchdb database called 'mastodon_au_social', if the database exists,just find that database. If not, just creat the database.
db_name = 'mastodon_au_social_final'
m = Mastodon(
    api_base_url='https://aus.social',
    access_token='2nwIHJnHrDkZkFnzbFEgDZmsYTTgu8aXnutLRRgermg'
)


# create listener to load the data
class Listener(StreamListener):
    def on_update(self, status):
        # if some message have some error, just print error to let the script run
        try:
            json_element = json.dumps(status, indent=2, sort_keys=True, default=str)
            json_single = json.loads(json_element)




            #ignore the http tag in the sentence, to extract the real words in the note.

            no_tags_string = re.sub('<.*?>', '', json_single['content'])

            # Replace Unicode line separator and paragraph separator characters
            no_special_chars_string = no_tags_string.replace(u'\u2028', ' ').replace(u'\u2029', ' ')

            # Replace HTML entities
            readable_string = no_special_chars_string.replace('&gt;', '>')

            # create a new dictionary to store the capture data
            new_store = {}
            new_store['id'] = json_single['account']['id']
            new_store['content'] = readable_string
            new_store['created_at'] = json_single['created_at']
            doc_id, doc_rev = db.save(new_store)
        except:
            print("error")


# open the harvest
m.stream_public(Listener())
