import firebase_admin
from firebase_admin import credentials,firestore
from datetime import datetime

class FirebaseFunctions:
    
    def __init__(self):
        self.db = None

    def getClient(self):
        if(self.db!=None):
            return self.db
        cred = credentials.Certificate("secretKey.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': "https://gitroaster.firebaseio.com"
        })
        self.db = firestore.client()     
        return self.db
           

FirebaseFunctions = FirebaseFunctions()
db = FirebaseFunctions.getClient()

def addRoast(username,roast):
    
    doc_ref = db.collection('data').document(username).collection('roasts').document(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    doc_ref.set({
        "roast":roast
    })
