from flask import Flask, render_template, jsonify, request, redirect, session
import json
import sqlite3
import bcrypt
import os

# Configure application
app = Flask(__name__)

# Get the database file
db_path = "purrfect.db"

# Set the salt 
salt = bcrypt.gensalt()
app.secret_key = 'secret_key'

def insert_user(username, password):
    '''Insert the user info into the database'''

    # Establish a connection to the database
    connection = sqlite3.connect("purrfect.db")
    cursor = connection.cursor()

    # Hashes the password
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password.encode('utf-8'), salt)

    # Inset the user and the hashed password
    cursor.execute("INSERT INTO users(username, hash) values(?, ?);", (username, hash))

    connection.commit()
    connection.close()

def check_password(username, to_check):
    '''Gets the user info by username'''

    # Establish a connection to the database
    connection = sqlite3.connect("purrfect.db")
    cursor = connection.cursor()
    
    # Gets the id, username and password
    cursor.execute("SELECT * FROM users WHERE username = (?);", (username,))
    
    user_info = cursor.fetchone()

    # Check it the username exists
    if not user_info:
        return False

    # Gets the password
    password = user_info[2]

    # Check it the password match with the password from the database
    if bcrypt.checkpw(to_check.encode('utf-8'), password):

        connection.close()
        return True

    connection.close()
    return False

# Inserts the cats info
def insert_cat(name, age, gender, location, description, path):
    '''Inserts the cat data into the db'''

    # Establish a connection to the database
    connection = sqlite3.connect("purrfect.db")
    cursor = connection.cursor()

    # Inset the user and the hashed password
    cursor.execute("INSERT INTO cats(name, age, gender, location, description, photo_path) values(?, ?, ?, ?, ?, ?);", (name, age, gender, location, description, path))

    connection.commit()
    connection.close()

# Gets the cats info
def get_cats():

    # Establish a connection to the database
    connection = sqlite3.connect("purrfect.db")
    cursor = connection.cursor()

    # Gets the cats info from the db
    cursor.execute("SELECT * FROM cats;")

    cats = cursor.fetchall()

    connection.close()

    return cats

# Gets the cats info
def get_cat_by_id(cat_id):

    # Establish a connection to the database
    connection = sqlite3.connect("purrfect.db")
    cursor = connection.cursor()

    # Gets the cats info from the db
    cursor.execute("SELECT * FROM cats WHERE id_cat=(?);", (cat_id,))

    cats = cursor.fetchone()
    connection.close()

    return cats

# Remouves a cat from the database
def adopt_cat(cat_id):

    # Establish a connection to the database
    connection = sqlite3.connect("purrfect.db")
    cursor = connection.cursor()

     # Remove the cat by id

    cursor.execute("DELETE FROM cats WHERE id_cat=(?);", (cat_id,))

    connection.commit()
    connection.close()


@app.route("/")

def home_page():

    if 'username' in session:

        username = session['username']
        cats = get_cats()
        l_locations=[]
        l_genders=[]
        l_ages=[]
        for cat in cats:
            l_locations.append(cat[4])
            l_genders.append(cat[3])
            l_ages.append(cat[2])

        locations=set(l_locations)
        genders=set(l_genders)
        ages=set(l_ages)



        return render_template('home.html', username=username, cats=cats, locations=locations, genders=genders, ages=ages)
    else:
        return redirect("/login")


def apology(message):
    return render_template('appology.html', apology=message) 

@app.route("/login", methods=["GET", "POST"])
def log_in():

    if request.method == "POST":

        # Gets the user info
        username = request.form.get("username")
        password = request.form.get("password")

        # Checks if any form is completed
        if not request.form.get("username"):
            return apology("Please enter a username")
        
        if not request.form.get("password"):
            return apology("Please enter a password")
        
        # Checks if the password and username are correct
        if check_password(username, password):
            session['username'] = username
            return redirect("/")
        
        else:
            return apology("Incorect username or password")
        
    else:
        return render_template("log_in.html")
    

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        # Gets the user info
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        # Checks if any form is completed
        if not username:
            return apology("Please enter a username")
        
        if not password:
            return apology("Please enter a password")
        
        if not confirm:
            return apology("Please enter a password confirmation")
        
        # Check if the password matchs the confirmation
        if password != confirm:
            return apology("Password and confirmation does not match!")
        
        insert_user(username, password)
        
        return redirect("/login")
    else:
        return render_template("signup.html")

@app.route("/logout")
# Disconect the users
def logout():
    session.clear()
    return redirect("/")

@app.route("/find", methods=["GET", "POST"])
def find():
# Gets the username

    if 'username' in session:
        username = session['username']

        # Get the list of tuples of cats
        cats = get_cats()
        if request.method == "POST":
            location = request.form.getlist("location")
            age = request.form.getlist("age")
            gender = request.form.getlist("gender")
            filter_cats = []
            for cat in cats:


                if (not location or cat[4].lower() in location) and (not age or cat[2].lower() in age) and (not gender or cat[3].lower() in gender):
                    filter_cats.append(cat)

            return render_template('find.html', username=username, cats=filter_cats)
        else:
            return render_template('find.html', username=username, cats=cats)
    else:
        return redirect("/login")
    
@app.route("/upload", methods=["GET", "POST"])
def upload():
    
    # Check if the user is logged in
    if 'username' not in session:
        return redirect("/login")

    username = session['username']

    
    if request.method == "POST":

        # Gets the cat information
        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        location = request.form.get("location")
        description = request.form.get("description")

        # Check if all fieald are filled
        if not name:
            return apology("Name field is emplty")
        if not age:
            return apology("Age field is emplty")
        if not gender:
            return apology("Gender field is emplty")
        if not location:
            return apology("Location of the fiels is location")
        if not description:
            return apology("Description of the fiels is description")
        
    
        # Check if a photo was uploaded
        if "image" in request.files:
            photo = request.files["image"]
            # Save the photo to the uploads directory
            path = os.path.join("static/uploads", photo.filename)
            photo.save(path)

            path = path[7:]
        else:
            return apology("Photo needed")
    
        # Inserts the cat data into the database
        insert_cat(name, age, gender, location, description, path)
        return redirect("/find")


    else:
        return render_template('upload.html', username=username)
    
@app.route("/cat/<int:cat_id>", methods=["GET", "POST"])
def cat_details(cat_id):
    cat=get_cat_by_id(cat_id)
    return render_template("cat_details.html", cat=cat)

@app.route("/adopt/<int:cat_id>", methods=["GET", "POST"])
def adopt(cat_id):
    cat=get_cat_by_id(cat_id)
    adopt_cat(cat_id)
    return render_template("adopt.html", cat=cat)


@app.route('/update_favs', methods=['POST'])
def update_favs():

    if 'username' in session:
        # Get the data sent from the frontend
        data = request.get_json()
        favsId = data.get('favsId', [])
        
        # Update the session data with the new favsId
        session['favourites_id'] = favsId

        # Perform any other processing or logic with the updated favsId here
        
        # Return a response if needed (optional)
        return jsonify(message='FavsId updated successfully')
    else:
        # Return an error response if the user is not logged in
        return jsonify(error='User not logged in'), 401

@app.route("/favourites", methods=["GET", "POST"])
def favourites():

    # If the userg acces the page with get renders the users favouites
    if request.method == "GET":
        if 'username' in session:

            cats=[]
            username = session.get('username')
            # Gets the users favourites by id
            favourites_id = session.get('favourites_id', [])

            for id in favourites_id:
                # Gets thhe cats info by id
                cat = get_cat_by_id(id)

                cats.append(cat)
                # If the cat is none removes it
                for cat in cats:
                    if cat is None:
                        cats.remove(cat)

            return render_template("favourites.html", username=username, cats=cats)
    else:
        # If the method is post remove the cat from favourites
        if 'username' in session:
            username = session.get('username')
        #  Gets the users favourites 
            favourites_id = session.get('favourites_id', [])
            cat_id = int(request.form.get('cat_id'))

        #   Removes the cat and updates the list
            favourites_id.remove(cat_id)
            session['favourites_id'] = favourites_id
            return redirect("favourites")

@app.route('/get_array_data')
def get_cats_data():
    if 'username' in session:
        favourites_id = session.get('favourites_id', [])

        # Retruns the users favourites
        return jsonify(favourites_id)

    # If the user is not logged in or doesn't have any favorites
    return jsonify([])

