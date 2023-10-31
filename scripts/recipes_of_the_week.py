'''this file gets 3 new recipes each week for the user to try. It will run auto manically each
monday of each week at 6am. I want all the data to be filled in.

It will take the information it has the put it into a file so that it only has to read from
that file the document keys that are the recipes fo the week. '''

from firebase_admin import firestore
from firebase_admin import credentials, initialize_app
import sys
import authentication as auth
import random

'''gets the recipe of the week every Monday. Runs on a cron'''
def pick_recipe_week():
    # setting up all credentials/getting keys done
    key = auth.send_authentication()
    cred = credentials.Certificate(key)
    # initializing the Firebase database
    initialize_app(cred)

    # reference to the database
    dataBaseClient = firestore.client()

    # gets the collection we are in
    collection_ref = dataBaseClient.collection('recipe')
    # gets all documents in a collection
    documents = collection_ref.stream()
    length = 0
    doc_list = []
    for doc in documents:
        key = doc.to_dict()
        doc_list.append(doc.id)
        length = length + 1

    # getting random numbers
    random_numbers = []
    unique_integers = set()
    while len(unique_integers) < 3:
        unique_integers.add(random.randint(0, length - 1))  # Change the range as needed

    # Convert the set to a list if you need the result as a list
    random_numbers = list(unique_integers)

    # clears the file then write the new line of code
    with open("static\\recipe_of_week.txt", "w") as file:
        # writing the document keys into the file
        file.write(f"{doc_list[random_numbers[0]]},")
        file.write(f"{doc_list[random_numbers[1]]},")
        file.write(f"{doc_list[random_numbers[2]]}")

pick_recipe_week()