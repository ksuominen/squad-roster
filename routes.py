from app import app
from flask import render_template, request, redirect

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if player.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Wrong username or password.")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="The passwords do not match.")
        if player.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Registration failed.")
