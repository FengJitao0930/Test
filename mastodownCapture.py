
# need to install couchdb
import couchdb
import json
# need to install mastodon.py
from mastodon import Mastodon, StreamListener

# connect to the couchdb
admin = 'jitao'  # change it to your admin account
password = 'fjt1879774' # change it to your password

# send request to couchdb
url = f'http://{admin}:{password}@127.0.0.1:5984/'
couch = couchdb.Server(url)

# create a couchdb database called 'mastodon', if the database exists,just find that database. If not, just creat the database.
db_name = 'mastodon'

if db_name not in couch:
    db = couch.create(db_name)
else:
    db = couch[db_name]


# mastodon server connect
m = Mastodon(
    api_base_url='https://mastodon.au',
    access_token='AfJXxavoZkTBBqqPK23U8jFTOb2j7bqar6EgCGMH3bs'
)

class Listener(StreamListener):
    def on_update(self, status):
        json_element = json.dumps(status, indent=2, sort_keys=True, default=str)
        json_single = json.loads(json_element)
        print(json_single['account']['note'])
        doc_id, doc_rev = db.save(json_single)
        print(f'Document saved with ID:{doc_id} and revision: {doc_rev}')

m.stream_public(Listener())
