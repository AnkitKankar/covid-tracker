from flask import Flask,request,jsonify
from pymongo import MongoClient
import pymongo
import ssl


app = Flask(__name__)


# Provide the mongodb atlas url to connect python to mongodb using pymongo
# CONNECTION_STRING = "mongodb+srv://admin:admin123@cluster0.wm8q8.mongodb.net/covid_tracker"

CONNECTION_STRING ="mongodb+srv://admin:admin123@cluster0.wm8q8.mongodb.net/covid_tracker"
# ?retryWrites=true&w=majority
client = MongoClient(CONNECTION_STRING)

# Create the database for our example (we will use the same database throughout the tutorial
db = client['covid_tracker']


ssl._create_default_https_context = ssl._create_unverified_context

@app.route('/registerUser',methods=['POST']) 
def RegisterUser():
    req = request.json
    # try:
    user_data = [int(x['userId']) for x in db.user_collection.find({},{'userId':1})]
    user_id = str(max(user_data)+1)
    req['userId'] = user_id
    db.user_collection.insert_one(req)
    return  jsonify({'userId':user_id})
    
    # except Exception as e:
    #     return jsonify({
    #         "message":str(e),
    #         "Status":"Failure"
    #     }) 
# No symptoms, No travel history, No contact with covid positive patient - Risk = 5%
# Any one symptom, travel history or contact with covid positive patient is true - Risk = 50%
# Any two symptoms, travel history or contact with covid positive patient is true - Risk = 75%
# Greater than 2 symptoms, travel history or contact with covid positive patient is true - Risk = 95%

# APIs:
# registerUser: 
# Sample request - {"name":"A","phoneNumber":"9999999999","pinCode":"111111"}
# Sample response - {"userId": "1"}
# selfAssessment:
# Sample request - {"userId":"1","symptoms":["fever","cold","cough"],"travelHistory":true,"contactWithCovidPatient":true}
# Sample response - {"riskPercentage": 95}


@app.route('/selfAssessment')
def SelfAssessment(req):
    try:
        if(req["symptoms"].length==0 and req["travelHistory"]==False and req["contactWithCovidPatient"]==False):
            return {"riskPercentage":5}
        
        elif(req["symptoms"].length==1 and (req["travelHistory"] or req["contactWithCovidPatient"])):
            return {"riskPercentage":50}

        elif(req["symptoms"].length==2 and (req["travelHistory"] or req["contactWithCovidPatient"])):
            return {"riskPercentage":75}
        
        elif(req["symptoms"].length>3 and (req["travelHistory"] or req["contactWithCovidPatient"])):
            return {"riskPercentage":95}
    
    except Exception as e:
        return jsonify({
            "message":str(e),
            "Status":"Failure"

        })
    




app.run(host='localhost', port=81)
