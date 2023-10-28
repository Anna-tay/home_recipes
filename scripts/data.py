import io
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import base64
from PIL import Image
'''This script will set/add/update all data'''

''' Adding new Recipe to database'''
def add_recipe(database, bucket, title, owner, notes,
                serv_yield, meal, rating, files, link):
    # getting recipe document
    collection_ref = database.collection('recipe')
    if not files:
        return "No files selected"

    if not files:
        print('No files selected')
    # list to store all the image file paths
    file_path_list = []
    for file in files:
        if file.filename == "":
            continue

        # # Upload each file to Firebase Storage
        # path = f"{title}/{file.filename}"
        # blob = bucket.blob(path)
        # blob.upload_from_string(file.read(), content_type=file.content_type)
        # file_path_list.append(path)

        # Open the file using PIL (Pillow)
        image = Image.open(file)

        # Convert the image to WebP format
        webp_buffer = io.BytesIO()
        image.save(webp_buffer, format="webp")

        # Upload the WebP image to Firebase Storage
        path = f"{title}/{file.filename}.webp"  # Add .webp extension
        blob = bucket.blob(path)
        blob.upload_from_string(webp_buffer.getvalue(), content_type="image/webp")
        file_path_list.append(path)

    # making a new document
    data = ({
        'title': title,
        'owner': owner,
        'notes': notes,
        'img': file_path_list,
        'serving_yield': serv_yield,
        'meal': meal,
        'link': link,
        'rating': [rating],
    })
    # adding them to collection
    collection_ref.add(data)


'''gets the new rating and adds it to the database'''
def add_rating(database, new_rating, id):
    # Reference to the Firestore document
    doc_ref = database.collection('recipe').document(id)

    # Get the current data in the document
    document = doc_ref.get()
    data = document.to_dict()

    # Check if the 'rating' field exists, and if not, initialize it as an empty list
    if 'rating' in data:
        ratings = data['rating']
        if len(data['rating']) == 20:
            total = 0
            for r in data['rating']:
                total = total + r
            adv = total/data['rating']
            ratings = [adv, adv, adv]
    else:
        ratings = []

    # Append the new rating to the list of ratings
    ratings.append(new_rating)

    # Update the 'rating' field with the new list of ratings
    doc_ref.update({'rating': ratings})
