'''this file gets 3 new recipes each week for the user to try. It will run auto manically each
monday of each week at 6am. I want all the data to be filled in.

It will take the information it has the put it into a file so that it only has to read from
that file the document keys that are the recipes fo the week. '''

from firebase_admin import firestore
from firebase_admin import credentials, initialize_app, storage as fb_storage
import authentication as auth
import random
import base64
import json

'''gets the recipe of the week every Monday. Runs on a cron'''
def pick_recipe_week():
    # setting up all credentials/getting keys done
    key = auth.send_authentication()
    bucket = auth.send_bucket()
    cred = credentials.Certificate(key)
    # initializing the firebase database
    initialize_app(cred, {
        'storageBucket': bucket
    })

    # reference to database
    dataBaseClient = firestore.client()

    bucket = fb_storage.bucket()

    # gets the collection we are in
    collection_ref = dataBaseClient.collection('recipe')
    # gets all documents in a collection
    documents = collection_ref.stream()
    length = 0
    doc_list = []
    for doc in documents:
        doc_list.append(doc)
        length = length + 1

    # getting random numbers
    random_numbers = []
    unique_integers = set()
    while len(unique_integers) < 3:
        unique_integers.add(random.randint(0, length - 1))  # Change the range as needed

    # Convert the set to a list if you need the result as a list
    random_numbers = list(unique_integers)

    recipe_list = []
    list_src = []
    id_list = []
    for number in random_numbers:
        recipe = doc_list[number].to_dict()
        if recipe['img'] != []:
            image_paths = recipe['img']
            blob = bucket.blob(image_paths[0])
            # Read the image data as a byte string
            image_data = blob.download_as_bytes()
            # Encode the image data as a base64 string
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            img_src= f"data:image/jpeg;base64,{image_base64}"
        else:
            img_src = ''
        list_src.append(img_src)
        id_list.append(doc_list[number].id)
        recipe_list.append(recipe)

    # clears the file then write the new line of code
    with open("static\\recipe_of_week.json", "w") as file:
        # writing the document keys into the file
        json.dump({
            "recipe1": recipe_list[0],
            "recipe2": recipe_list[1],
            "recipe3": recipe_list[2],
            "img1": list_src[0],
            "img2": list_src[1],
            "img3": list_src[2],
            "id1": id_list[0],
            "id2": id_list[1],
            "id3": id_list[2],
        }, file)

pick_recipe_week()