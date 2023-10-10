import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import base64

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
        blob = bucket.blob(f"{title}/{file.filename}")
        blob.upload_from_string(file.read(), content_type=file.content_type)
            # file_names = file_names + file.name

    # destination_blob_name = f"{title}/{file_names}"
    # making a new document
    data = ({
        'title': title,
        'owner': owner,
        'notes': notes,
        'img': f"{title}/{file.filename}",
        'serving_yield': serv_yield,
        'meal': meal,
        'rating': rating,
    })
    # adding them to collection
    collection_ref.add(data)


''' Getting all the values from the database and putting them into a dictionary to return'''
def get_all_values(database, bucketClient, bucket, recipe_id):
    # gets the collection we are in
    collection_ref = database.collection('recipe')
    # gets the document
    document = collection_ref.document(recipe_id).get()
    # turns the doc into a dic
    data = document.to_dict()

    # getting the images from database
    image_paths_in_bucket = [data['img']]

    # Create an empty list to store HTML img tags
    html_img_tags = []

    # Loop through the image paths
    for image_path_in_bucket in image_paths_in_bucket:
        # Get a reference to the image blob in the bucket
        bucket = bucketClient.get_bucket(bucket)
        blob = bucket.blob(image_path_in_bucket)

        # Retrieve the image data
        image_data = blob.download_as_bytes()

        # Convert the image data to base64
        base64_image = base64.b64encode(image_data).decode('utf-8')

        # Generate an HTML img tag with the base64-encoded image
        html_img_tag = f'<img src="data:image/jpeg;base64,{base64_image}" alt="Image">'

        # Append the img tag to the list
        html_img_tags.append(html_img_tag)

    # Join the list of img tags into a single string
    all_html_img_tags = ''.join(html_img_tags)



    # return dictionary
    return (data, all_html_img_tags)


