import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

''' Adding new Recipe to database'''
def add_recipe(database, title, owner, notes, serv_yield, meal, rating):
    # getting recipe document
    collection_ref = database.collection('recipe')

    # making a new document
    data = ({
        'title': title,
        'owner': owner,
        'notes': notes,
        'img': 'img',
        'serving_yield': serv_yield,
        'meal': meal,
        'rating': rating,
    })

    collection_ref.add(data)

''' Getting all the values from the database and putting them into a dictionary to return'''
def get_all_values(database, recipe_id):
    # gets the collection we are in
    collection_ref = database.collection('recipe')
    # gets the document
    document = collection_ref.document(recipe_id).get()
    # turns the doc into a dic
    data = document.to_dict()
    # return dictionary
    return data
