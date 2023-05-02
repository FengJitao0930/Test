
# need to install couchdb
import couchdb
import json
# need to install mastodon.py
from mastodon import Mastodon, StreamListener
import re

# connect to the couchdb
admin = 'cccadmin'  # change it to your admin account
password = 'whysohard24!' # change it to your password

# send request to couchdb
url = f'http://{admin}:{password}@127.0.0.1:5984/'
couch = couchdb.Server(url)

# create a couchdb database called 'mastodon', if the database exists,just find that database. If not, just creat the database.
db_name = 'mastodontest'

if db_name not in couch:
    db = couch.create(db_name)
else:
    db = couch[db_name]


# mastodon server connect
m = Mastodon(
    api_base_url='https://aus.social',
    access_token='2nwIHJnHrDkZkFnzbFEgDZmsYTTgu8aXnutLRRgermg'
)

class Listener(StreamListener):
    def on_update(self, status):
        json_element = json.dumps(status, indent=2, sort_keys=True, default=str)
        json_single = json.loads(json_element)


        # if their account is created in Australia, then store their information

        #ignore the http tag in the sentence, to extract the real words in the note.

        no_tags_string = re.sub('<.*?>', '', json_single['content'])

        # Replace Unicode line separator and paragraph separator characters
        no_special_chars_string = no_tags_string.replace(u'\u2028', ' ').replace(u'\u2029', ' ')

        # Replace HTML entities
        readable_string = no_special_chars_string.replace('&gt;', '>')
        # if  "food" in readable_string or "meal" in readable_string or "dish" in readable_string:
        if json_single['language'] == "en":
            new_store = {}
            new_store['id'] = json_single['account']['id']
            new_store['content'] = readable_string
            new_store['created_at'] = json_single['created_at']

            doc_id, doc_rev = db.save(new_store)


m.stream_public(Listener())
