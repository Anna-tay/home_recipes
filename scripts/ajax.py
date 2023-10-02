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

# POPULATING TABLE WITH AJAX
def table(db):

    try:
        if request.method == "POST":

            draw = request.form['draw']
            print(draw)

            collection = db.collection("recipe").stream()

            data = []
            for recipe in collection:
                recipe = recipe.to_dict()
                data.append({
                    'title': recipe['title'],
                    'meal': recipe['meal'],
                    'owner': recipe['owner'],
                    'rating': recipe['rating']
                })
            print(data)
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

