import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore



def getConnected():
    # getting file path
    cred = credentials.Certificate("database/recipe-box-7a513-firebase-adminsdk-ab32o-0558f7de3a.json")
    # initializing the firebase database
    firebase_admin.initialize_app(cred)
    # reading from the database
    db = firestore.client()

    return db

def get_total():
    db = getConnected()
    collection = db.collection("Recipe").stream()
    # gets it in a json
    print(collection)

    # reading it from a json -------------------------
    print('each recipe')
    total = 0
    for recipe in collection:
        total += 1
        recipes = recipe.to_dict()
        # getting the specific value
        print(recipes.get('title'))
    print(total)

def get_filter_data():

    db = getConnected()
    collection = db.collection("Recipe").stream()
    # gets it in a json
    print(collection)

    # reading it from a json -------------------------
    print('each recipe')

    for recipe in collection:
        recipes = recipe.to_dict()
        # getting the specific value
        print(recipes.get('title'))


# DO THIS ONE LATER
# def get_total_filter():
#     db = getConnected()
#     recipes =  db.collection("Recipe").stream()
#     print(recipes)

#     return len(recipes)


# def get_data():
#     pass

get_total()
# # gets data
# collection = db.collection("Recipe").stream()
# # gets it in a json
# print(collection)

# reading it from a json -------------------------
# print('each recipe')
# for recipe in collection:
#     print("".format(recipe.to_dict())) #printing each recipe in a dic
#     recipes = recipe.to_dict()
#     # getting the specific value
#     print(recipes.get('title'))


# writing to fire store Database -----------------
# db = getConnected()

# recipies = db.collection("Recipe")

# # adding to document. Adding a unique thing
# recipies.document().set({
#     'title': "Banana pan 1 cakes",
#     'notes': "these are all the notes",
#     'img': 'static\images\Recipe_box_logo.png'
#     })


