'''this file gets 3 new recipes each week for the user to try. It will run auto manically each
monday of each week at 6am. I want all the data to be filled in.

It will take the information it has the put it into a file so that it only has to read from
that file the document keys that are the recipes fo the week. '''

from firebase_admin import firestore
from firebase_admin import credentials, initialize_app
import authentication as auth
import random
import base64
from PIL import Image

'''gets the recipe of the week over monday. runs on a cron'''
def pick_recipe_week():
    # setting up all credentials/getting keys done
    key = auth.send_authentication()
    cred = credentials.Certificate(key)
    # initializing the firebase database
    initialize_app(cred)

    # reference to database
    dataBaseClient = firestore.client()

    # gets the collection we are in
    collection_ref = dataBaseClient.collection('recipe')
    # gets all documents in a collection
    documents = collection_ref.stream()

    # getting random numbers
    random_numbers = [random.randint(0, len(documents)) for _ in range(3)]
    # clears the file then write the new line of code
    with open("static\recipe_of_week.txt", "w") as file:
        # writing the document keys into the file
        for num in random_numbers:
            file.write(f"{documents[num]}\n")
