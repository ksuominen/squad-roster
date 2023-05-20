from app import app
from flask import render_template, request, redirect
import player
import item
import skill

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
        
@app.route("/logout")
def logout():
    player.logout()
    return redirect("/")

@app.route("/items", methods=["GET", "POST"])
def items():
    if request.method == "GET":
        items = item.get_all_items()
        return render_template("items.html", items=items)
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        item.add_item(name, description)
        return redirect("/items")

@app.route("/skills", methods=["GET", "POST"])
def skills():
    if request.method == "GET":
        trained_skills = skill.get_trained_skills()
        expert_skills = skill.get_expert_skills()
        master_skills = skill.get_master_skills()
        return render_template("skill.html", trained_skills=trained_skills, expert_skills=expert_skills, master_skills=master_skills)
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        level = request.form["level"]
        skill.add_skill(name, description, level)
        return redirect("/skills")