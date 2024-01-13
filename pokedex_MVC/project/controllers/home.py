from project import app
from flask import render_template, request, redirect, url_for
from project.models.User import *

# route to index base
@app.route("/")
def index():
    return render_template("index.html")

#route to new index after login or create user
@app.route("/", methods=["POST"])
def login():

    # find username/passwords from the html POST form
    username = request.form.get("username")
    password = request.form.get("password")
    new_username = request.form.get("new_username")
    new_password = request.form.get("new_password")

    # define two different error-messages
    error_message = None
    new_error = None

    """
        IF username was posted in html form, find the user and redirect
        to the main pokedex.

        ElseIf new_username was posted, create a new user and insert into 
        the database. The user then has to login with their new account before
        getting routed to the pokedex.
    """
    if username:  
        result = findUser(username, password)
        if username in result:
            return redirect(url_for("pokedex", username=username))
        else:
            error_message = result
    elif new_username:
        result = create_user(new_username, new_password)
        if not result:
            new_error = "Error"
            
    return render_template("index.html", error_message=error_message, new_error=new_error)