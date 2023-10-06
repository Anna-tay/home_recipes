import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask, render_template, url_for, request, jsonify

# SETTING UP CONNECTING TO FIREBASE
def getConnected():
    # getting file path
    cred = credentials.Certificate("database/recipe-box-7a513-firebase-adminsdk-ab32o-0558f7de3a.json")
    # initializing the firebase database
    firebase_admin.initialize_app(cred)
    # reading from the database
    db = firestore.client()

    return db


# Getting all recipes that are sorted and not
def fetch_data(db, search_value, row, row_page):
    # making a empty list to store data in
    recipe_list = []
    print(f'this is sv {search_value}')

    # Retrieve data from Firestore
    if search_value == '':
        recipe_list = db.collection('recipe').limit(row_page).offset(row).stream()
    else:
        query = db.collection('recipe').where('title', '>=', search_value).limit(row_page).offset(row)
        recipe_list = query.stream()

    data = []
    for recipe in recipe_list:
        recipe_id = recipe.id
        # print(recipe_id)
        recipe = recipe.to_dict()
        data.append({
            'id': recipe_id,
            'title': recipe['title'],
            'meal': recipe['meal'],
            'owner': recipe['owner'],
            'rating': recipe['rating']
        })


    return data


# POPULATING TABLE WITH AJAX
def table(db):

    try:
        if request.method == "POST":
            # getting all the specifics from the data table
            draw = request.form['draw']
            row = int(request.form['start'])
            row_page = int(request.form['length'])
            search_value = request.form["search[value]"]
            # print(draw)
            # print(row)
            # print(row_page)
            # print(search_value) # the search value from user

            data = fetch_data(db, search_value, row, row_page)

        response = {
            'draw' : draw,
            'iTotalRecords': 5,
            'iTotalDisplayRecords': 5,
            'aaData': data,
        }
        return jsonify(response)

    except Exception as e:
        print(f'e prinited: {e}')
        response = {
            'draw' : 1,
            'iTotalRecords': 5,
            'iTotalDisplayRecords': 5,
            'aaData': 'none',
        }
        return jsonify(response)

