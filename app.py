from flask import Flask, render_template, url_for, request, redirect
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import scripts.ajax as AjaxData
import scripts.database as Data


app = Flask(__name__)
# getting file path
cred = credentials.Certificate("database/recipe-box-7a513-firebase-adminsdk-ab32o-0558f7de3a.json")
# initializing the firebase database
firebase_admin.initialize_app(cred)

dataBase = firestore.client()

# Home page
@app.route('/', methods = ["GET", "POST"])
def home():
    if request.method == 'POST':
        return render_template("entry.html")
    return render_template("home.html")

# ajax
@app.route('/ajax', methods =["GET", "POST"])
def ajax():
    data = AjaxData.table(dataBase)
    return data

# Add recipe page
@app.route('/entry', methods = ["GET", "POST"])
def entry():
    print('came in')
    if request.method == "POST":
        title = request.form.get('title')
        owner = request.form.get('owner')
        notes = request.form.get('notes')
        meal = request.form.get('meal')
        serv_yield = request.form.get('serving_yield')
        rating = request.form.get('rating')
        Data.add_recipe(dataBase, title, owner, notes, serv_yield, meal, rating)

        return redirect(url_for('home'))
    return render_template("entry.html")

# View recipe
@app.route('/view', methods = ["GET", "POST"])
def view():

    return render_template("view.html")

if __name__ == '__main__':
    app.run(debug=True)
