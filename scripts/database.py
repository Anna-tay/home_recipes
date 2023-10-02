import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Adding new Recipe to database
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


# def get_filter_data():

#     db = getConnected()
#     collection = db.collection("recipe").stream()
#     # gets it in a json
#     print(collection)

#     # reading it from a json -------------------------
#     print('each recipe')

#     for recipe in collection:
#         recipes = recipe.to_dict()
#         # getting the specific value
#         print(recipes.get('title'))


# DO THIS ONE LATER
# def get_total_filter():
#     db = getConnected()
#     recipes =  db.collection("recipe").stream()
#     print(recipes)

#     return len(recipes)


# def get_data():
#     pass


# # gets data
# collection = db.collection("recipe").stream()
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


