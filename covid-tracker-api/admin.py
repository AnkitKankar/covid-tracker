# ADMIN:
# You need to provide admin options for the covid health workers:
# Register: Covid health workers can register by providing their name, mobile number and pin code.
# Covid Result: Health workers can enter the result of covid tests for patients.
# Health workers can also mark already registered users as recovered.

# APIs:
# registerAdmin:
# Sample request - {"name":"X","phoneNumber":"9999999999","pinCode":"111111"}
# Sample response - {"adminId": "2"}
# updateCovidResult:
# Sample request - {"userId":"1","adminId":"2","result":"positive"}
# Sample response - {"updated":true}




from flask import Flask,request,jsonify
# Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
from pymongo import MongoClient

app = Flask(__name__)

# Provide the mongodb atlas url to connect python to mongodb using pymongo
CONNECTION_STRING = "mongodb+srv://admin:admin123@cluster0.wm8q8.mongodb.net/myFirstDatabase"

    
client = MongoClient(CONNECTION_STRING)

# Create the database for our example (we will use the same database throughout the tutorial
db = client['covid_tracker']

@app.route('/')
def index():
    return 'Web App with Python Flask!'


@app.route('/registerAdmin')
def RegisterAdmin():
    try:
        req = request.json
        admin_data = [int(x['adminId']) for x in db.user_collection.find({},{'adminId':1})]
        admin_id = str(max(admin_data)+1)
        req['adminId'] = admin_id
        db.admin_collection.insert_one(req)
        return {"adminId":admin_id}
    
    except Exception as e:
        return jsonify({
            "message":str(e),
            "Status":"Failure"
        })

@app.route('/updateCovidResult'):
def UpdateCovidResult():
   try:
        req = request.json
        db.covid_result.insert_one(req)
        if(req["result"]=="positive"):
            pin_code = db.admin_collection.find_one({"adminId":req['adminId']},{"pincode":1})
            active_cases = db.active_cases.find_one({"pinCode":pin_code},{"activeCases":1})
            db.active_cases.update_one({"pinCode":pin_code},{"$set":{"activeCases":active_cases +1}})
        return {"updated":true}
    except Exception as e:
        return jsonify({
            "message":str(e),
            "Status":"Failure"
        })

app.run(host='0.0.0.0', port=81)