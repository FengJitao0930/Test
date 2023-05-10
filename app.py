from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_restful import Api, Resource
import couchdb

app = Flask(__name__)
CORS(app)

couch = couchdb.Server('http://cccadmin:whysohard24!@172.26.135.17:5984/')
db = couch['huge_twitter_geo']


@app.route('/')
def root():
    return render_template('Index.html')


# default GET
@app.route('/api/cancer_map')
def cancer_map():
    # Mango Queries
    # query = {
    #     "selector": {
    #         "text": {
    #             "$regex": "(?i)cancer"
    #         }
    #     },
    #     "fields": ["_id", "geo", "position"],
    #     "limit": 5000
    # }

    # View Check
    view = db.view('cancerCount/cancerRows')
    # Execute the query

    # (10°41) 43°38' south longitudes 113°09' eaand 153°38' east
    results = []
    for row in view:
        if row["value"]["geo"]["bbox"][1] < -43.38 or row["value"]["geo"]["bbox"][1] > -10.41 or row["value"]["geo"]["bbox"][0] < 113.09 or row["value"]["geo"]["bbox"][0] > 153.38:
            continue

        ifExists = False
        for res in results:
            if row["value"]["geo"]["bbox"][1] == res["lat"] and row["value"]["geo"]["bbox"][0] == res["lng"]:
                res["count"] += 1
                ifExists = True
                break

        if not ifExists:
            new_geo = {
                "lat": row["value"]["geo"]["bbox"][1],
                "lng": row["value"]["geo"]["bbox"][0],
                "position": row["value"]["position"],
                "count": 1
            }
            results.append(new_geo)

    # Return the results as JSON
    return results


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8080')
