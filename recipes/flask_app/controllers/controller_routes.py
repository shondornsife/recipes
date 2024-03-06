from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.model_user import User
from flask_app.models.model_recipe import Recipe


@app.route("/")
def index():
    if "user_id" in session:
        return redirect("/dashboard")
    return render_template("index.html")


# DISPLAY ROUTE shows the form of dashboard
@app.route("/dashboard")
def dashboard():
    if not "user_id" in session:
        return redirect("/")
    user = User.get_one({"id": session["user_id"]})
    all_recipes = Recipe.get_all()
    return render_template("dashboard.html", user=user, all_recipes=all_recipes)


# @app.route("/dashboard")
# def dashboard():
#     user_id = session.get("user_id")  # assuming you store user ID in the session
#     print(user_id)
#     if user_id:
#         user = User.get_one({"id": user_id})
#         if user:
#             return render_template("dashboard.html", user=user)
#     return redirect("/")


@app.route("/logout")
def logout():
    # Clear the session to log the user out
    session.clear()
    return redirect("/")
