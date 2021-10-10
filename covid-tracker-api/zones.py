# ZONES:
# Mark zones (pin codes) as green, orange and red based on positive covid cases.
# Default zone - GREEN
# <5 cases in a zone - ORANGE
# >5 cases in a zone - RED

# APIs
# getZoneInfo:
# Sample request - {"pinCode":"111111"}
# Sample response - {"numCases":"1","zoneType":"ORANGE"}
from flask import Flask,request,jsonify
from pymongo import MongoClient
import pymongo


app = Flask(__name__)


# Provide the mongodb atlas url to connect python to mongodb using pymongo
CONNECTION_STRING = "mongodb+srv://admin:admin123@cluster0.wm8q8.mongodb.net/myFirstDatabase"


client = MongoClient(CONNECTION_STRING)

# Create the database for our example (we will use the same database throughout the tutorial
db = client['covid_tracker']


@app.route('/getZoneInfo')
def GetZoneInfo():
    try: 
        req = request.json
        zone_info = db.active_cases.find_one({"pinCode":req['pinCode']},{})
        if(zone_info['activeCases']>=5):
            return {"numCases":zone_info['activeCases'],"zoneType":"Red"}
        
        elif(zone_info["activeCases"]<5 and zone_info['activeCases']>1):
            return {"numCases":zone_info['activeCases'],"zoneType":"Orange"}
        
        else:
            return {"numCases":zone_info['activeCases'],"zoneType":"Green"}
    
     except Exception as e:
        return jsonify({
            "message":str(e),
            "Status":"Failure"
        }) 


app.run(host='0.0.0.0', port=81)