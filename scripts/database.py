import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# getting file path
cred = credentials.Certificate("/database/recipe-box-7a513-firebase-adminsdk-ab32o-0558f7de3a.json")
# initializing the firebase database
firebase_admin.initialize_app(cred)


# reading from the database
db = firestore.client()

# gets data
collection = db.collection("Recipe").stream()
print(collection)