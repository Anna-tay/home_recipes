import io
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import base64
from PIL import Image
'''this script has functions that only get data'''

''' Getting all the values from the database and putting them into a dictionary to return'''
def get_recipe(database, bucket, recipe_id):
    # gets the collection we are in
    collection_ref = database.collection('recipe')
    # gets the document
    document = collection_ref.document(recipe_id).get()
    # turns the doc into a dic
    data = document.to_dict()

    # getting the images from database --------------------------
    image_paths = data['img']

    # empty list of src
    src_list = []
    for image_path in image_paths:

        blob = bucket.blob(image_path)

        # Read the image data as a byte string
        image_data = blob.download_as_bytes()

        # Encode the image data as a base64 string
        image_base64 = base64.b64encode(image_data).decode('utf-8')

        img_src= f"data:image/jpeg;base64,{image_base64}"

        src_list.append(img_src)

    # getting rating
    rating = get_rating(data['rating'])

    # return dictionary
    return (data, src_list, rating)

''' Getting all recipe values'''
def get_all_recipes(database, bucket):

    recipes=[]
    # gets the collection we are in
    collection_ref = database.collection('recipe')
    # gets all documents in a collection
    documents = collection_ref.stream()
    # print(documents)
    for document in documents:
        # turns the doc into a dic
        recipe = document.to_dict()

        # getting the first image from database for each recipe
        image_paths = recipe['img']

        blob = bucket.blob(image_paths[0])
        # Read the image data as a byte string
        image_data = blob.download_as_bytes()
        # Encode the image data as a base64 string
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        img_src= f"data:image/jpeg;base64,{image_base64}"

        # getting rating
        rating = get_rating(recipe['rating'])
        # putting all variables in one list
        recipes.append([document.id, recipe, img_src, rating])

    # return dictionary
    return (recipes)

'''Getting all recipes that are match to the user search'''
def get_search_recipes(database, bucket, search_value, search_type, search_owner):
    recipes=[]
    # gets the collection we are in
    collection_ref = database.collection('recipe')
    # gets all documents in a collection
    documents = collection_ref.stream()
    # print(documents)
    for document in documents:
        # turns the doc into a dic
        recipe = document.to_dict()
        owner = False
        mt = False
        title = False
        if search_owner in recipe['owner']:
            owner = True
        if search_type in recipe['meal']:
            mt = True
        if search_value in recipe['title']:
            title = True

        # print(f'this is the title {title} owner {owner} mt {mt}')
        if title or mt or owner:
            # print('it went in')

            # getting the first image from database for each recipe
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
            # getting rating
            rating = get_rating(recipe['rating'])

            # putting all variables in one list
            recipes.append([document.id, recipe, img_src, rating])

    # return dictionary
    return (recipes)

'''gets the recipe doc from the file then returns the recipe and the img_src'''
def get_recipe_week(database, bucket):
    # getting the ref
    collection_ref = database.collection('recipe')

    # making a list of recipes of the week
    recipes_week = []
    with open("static\\recipe_of_week.txt", "r") as file:
        file_content = file.read()
        file_content = file_content.split(",")
        for document_key in file_content:
            # gets the document
            document = collection_ref.document(document_key).get()
            # turns the doc into a dic
            data = document.to_dict()
            # getting the image from database
            image_paths = data['img']
            blob = bucket.blob(image_paths[0])
            # Read the image data as a byte string
            image_data = blob.download_as_bytes()
            # Encode the image data as a base64 string
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            img_src= f"data:image/jpeg;base64,{image_base64}"
            # getting rating
            rating = get_rating(data['rating'])
            recipes_week.append([data, img_src, rating, document_key])

    # returns a list [recipe_dic, recipe_img_src]
    return recipes_week

'''returns the average rating'''
def get_rating(ratings):
    total = 0
    # print(f'this is rating {ratings}')
    for rating in ratings:
        total = total + int(rating)
    adv = total//len(ratings)

    # returns the rating with starts
    if adv == 1:
        adv = "★"
    elif adv == 2:
        adv = "★★"
    elif adv == 3:
        adv = "★★★"
    elif adv == 4:
        adv = "★★★★"
    elif adv == 5:
        adv = "★★★★★"

    return adv