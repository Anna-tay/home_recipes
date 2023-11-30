import base64
import json
import threading
from concurrent.futures import ThreadPoolExecutor
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

    # if data['rating'] == NULL/
    rating = get_rating(data['rating'])

    # return dictionary
    return (data, src_list, rating)


'''Fetching the recipe with threading'''
def fetch_recipe(document, bucket, searches, fetch_semaphore):
    search_owner = searches[0]
    search_type  = searches[1]
    search_value = searches[2]
    # turns the doc into a dic
    with fetch_semaphore:
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

        if title or mt or owner:
            # getting the first image from the database for each recipe
            if recipe['img'] != []:
                image_paths = recipe['img']

                blob = bucket.blob(image_paths[0])
                # Read the image data as a byte string
                image_data = blob.download_as_bytes()
                # Encode the image data as a base64 string
                image_base64 = base64.b64encode(image_data).decode('utf-8')
                img_src = f"data:image/jpeg;base64,{image_base64}"
            else:
                img_src = ''
            # getting rating
            rating = get_rating(recipe['rating'])

            # return list of items
            return [document.id, recipe, img_src, rating]

        return None

'''Getting all recipes that are match to the user search'''
def get_search_recipes_concurrent(database, bucket, search_value, search_type, search_owner):
    recipes = []
    collection_ref = database.collection('recipe')
    documents = collection_ref.stream()
    fetch_semaphore = threading.Semaphore(3)


    with ThreadPoolExecutor() as executor:
        futures = []

        for document in documents:
            # For each document, submit a task to fetch the recipe
            future = executor.submit(fetch_recipe, document, bucket,
                                     [search_owner, search_type, search_value],
                                     fetch_semaphore)
            futures.append(future)

        # Wait for all tasks to complete
        for future in futures:
            recipe_data = future.result()
            if recipe_data:
                recipes.append(recipe_data)

    return recipes

'''gets the recipe doc from the file then returns the recipe and the img_src'''
def get_recipe_week():

    with open("static\\recipe_of_week.json", "r") as json_file:
        data = json.load(json_file)


        recipes_week = [
            [data['recipe1'], data['img1'], get_rating(data['recipe1']['rating']), data['id1']],
            [data['recipe2'], data['img2'], get_rating(data['recipe2']['rating']), data['id2']],
            [data['recipe3'], data['img3'], get_rating(data['recipe3']['rating']), data['id3']],
            ]

    return recipes_week

'''returns the average rating'''
def get_rating(ratings):

    if ratings[0] == None:
        return ""
    else:
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