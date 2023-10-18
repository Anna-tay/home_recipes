import io
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import base64
from PIL import Image

''' Adding new Recipe to database'''
def add_recipe(database, bucket, title, owner, notes,
                serv_yield, meal, rating, files):
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
        'rating': rating,
    })
    # adding them to collection
    collection_ref.add(data)


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

    # return dictionary
    return (data, src_list)

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

        # putting all variables in one list
        recipes.append([document.id, recipe, img_src])

    # return dictionary
    return (recipes)

'''Getting all recipes that are match to the user search'''
def get_search_recipes(database, bucket, search_value):
    recipes=[]
    # gets the collection we are in
    collection_ref = database.collection('recipe')
    # gets all documents in a collection
    documents = collection_ref.stream()
    # print(documents)
    for document in documents:
        # turns the doc into a dic
        recipe = document.to_dict()
        if search_value in recipe['title']:

            # getting the first image from database for each recipe
            image_paths = recipe['img']

            blob = bucket.blob(image_paths[0])
            # Read the image data as a byte string
            image_data = blob.download_as_bytes()
            # Encode the image data as a base64 string
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            img_src= f"data:image/jpeg;base64,{image_base64}"

            # putting all variables in one list
            recipes.append([document.id, recipe, img_src])

    # return dictionary
    return (recipes)
