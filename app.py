from flask import Flask, render_template, url_for, request, redirect
from firebase_admin import firestore
from firebase_admin import credentials, storage as fb_storage, initialize_app
from google.cloud import storage
import scripts.database as Data
import authentication as auth



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
    recipes = []
    search_value = ""
    sv = 'false'
    if request.method == 'POST':
        search_value = request.form.get('search_value')
        print(f'this is sv {search_value}')
        if search_value != '':
            sv = 'true'
            recipes = Data.get_search_recipes(dataBaseClient, bucket, search_value)

    length = len(recipes)
    return render_template("home.html", recipes = recipes, search_value = search_value,
                           length = length, sv=sv)

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
        rating = request.form.get('rating')
        # getting files
        files = request.files.getlist('recipe_img')
        # adding them all to recipe database
        Data.add_recipe(dataBaseClient, bucket, title, owner,
                         notes, serv_yield, meal, rating, files)

        return redirect(url_for('home'))
    return render_template("entry.html")

# View recipe
@app.route('/view/<recipe_id>', methods = ["GET", "POST"])
def view(recipe_id):
    # getting values from the database and putting it into a dictionary
    data_dic, imgs_src = Data.get_recipe(dataBaseClient, bucket, recipe_id)
    return render_template("view.html", data_dic = data_dic, imgs_src=imgs_src)

if __name__ == '__main__':
    app.run(debug=True)
