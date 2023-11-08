from flask import Flask, render_template, url_for, request, redirect
from firebase_admin import firestore
from firebase_admin import credentials, storage as fb_storage, initialize_app
from google.cloud import storage
import scripts.get_data as Get_data
import scripts.data as Data
import scripts.authentication as auth
import time
import threading

app = Flask(__name__)
# getting file path
key = auth.send_authentication()
bucket = auth.send_bucket()
cred = credentials.Certificate(key)
# initializing the firebase database
initialize_app(cred, {
    'storageBucket': bucket
})

# reference to database
dataBaseClient = firestore.client()

bucket = fb_storage.bucket()

# Home page
@app.route('/', methods = ["GET", "POST"])
def home():
    # STARTING A TIMER
    #Start a timer
    begin_time = time.time()
    recipes = []
    search_value = ""
    sv = 'false'
    if request.method == 'POST':
        search_value = request.form.get('search_value')
        search_type = request.form.get('meal_type')
        search_owner = request.form.get('search_owner')
        # print(search_type)
        if search_value != '' or search_owner != '' or search_type != 'NULL':
            if search_owner == '':
                search_owner = 'NULL'
            if search_value == '':
                search_value = 'NULL'
            sv = 'true'
            # calling the function I want to be threaded
            recipes = Get_data.get_search_recipes_concurrent(dataBaseClient, bucket, 
                                                             search_value, search_type, 
                                                             search_owner, begin_time)
            # start and join them all here

    length = len(recipes)
    recipes_of_week = Get_data.get_recipe_week()
    return render_template("home.html", recipes = recipes, search_value = search_value,
                           length = length, sv=sv, recipes_of_week = recipes_of_week)

# Add recipe page
@app.route('/entry', methods = ["GET", "POST"])
def entry():
    if request.method == "POST":
        # getting all variables from user input
        title = request.form.get('title')
        owner = request.form.get('owner')
        notes = request.form.get('notes')
        meal = request.form.get('meal')
        serv_yield = request.form.get('serving_yield')
        link = request.form.get('link')
        rating = request.form.get('rating')
        # manual recipe
        ingredients = request.form.get('ingredients')
        instructions = request.form.get('instructions')
        # getting files
        files = request.files.getlist('recipe_img')
        print(files)
        # adding them all to recipe database
        Data.add_recipe(dataBaseClient, bucket, title.capitalize(), owner,
                         notes, serv_yield, meal, rating, files, link,
                           ingredients, instructions)

        return redirect(url_for('home'))
    return render_template("entry.html")

# View recipe
@app.route('/view/<recipe_id>', methods = ["GET", "POST"])
def view(recipe_id):
    if request.method == "POST":
        new_rating = request.form.get('rating')
        Data.add_rating(dataBaseClient, new_rating, recipe_id)
    # getting values from the database and putting it into a dictionary
    data_dic, imgs_src, rating = Get_data.get_recipe(dataBaseClient, bucket, recipe_id)
    return render_template("view.html", data_dic = data_dic, imgs_src=imgs_src,
                            rating=rating)

# Handling error pages
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
