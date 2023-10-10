import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

''' Adding new Recipe to database'''
def add_recipe(database, bucket, title, owner, notes,
                serv_yield, meal, rating, files):
    # getting recipe document
    collection_ref = database.collection('recipe')
    if not files:
        return "No files selected"

    # file_names = ""
    if not files:
        print('No files selected')

    for file in files:
        if file.filename == "":
            continue

        # Upload each file to Firebase Storage
        blob = bucket.blob(file.filename)
        blob.upload_from_string(file.read(), content_type=file.content_type)
            # file_names = file_names + file.name

    # destination_blob_name = f"{title}/{file_names}"
    # making a new document
    data = ({
        'title': title,
        'owner': owner,
        'notes': notes,
        'img': title,
        'serving_yield': serv_yield,
        'meal': meal,
        'rating': rating,
    })
    # adding them to collection
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
