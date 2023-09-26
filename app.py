from flask import Flask, render_template, url_for, request
import scripts.ajax as Ajax

app = Flask(__name__)

# Home page
@app.route('/', methods = ["GET", "POST"])
def home():
    if request.method == 'POST':
        return render_template("entry.html")
    return render_template("home.html")

# ajax 
@app.route('/ajax', methods =["GET", "POST"])
def ajax():
    Ajax.table()
# put all ajax python stuff into one bit def then break it down after wards.

# Add recipe page
@app.route('/entry', methods = ["GET", "POST"])
def entry():

    return render_template("entry.html")

# View recipe
@app.route('/view', methods = ["GET", "POST"])
def view():

    return render_template("view.html")

if __name__ == '__main__':
    app.run(debug=True)
