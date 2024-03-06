from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.model_recipe import Recipe


# DISPLAY ROUTE - shows the form to create recipes
@app.route("/recipes/new")
def recipes_new():
    return render_template("recipes_new.html")


# ACTION ROUTE - process the form from the new route (above)
@app.post("/recipes/create")
def create_recipe():
    is_valid = Recipe.validate(request.form)

    if not is_valid:
        return redirect("/recipes/new")

    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "date_cooked": request.form["date_cooked"],
        "under_thirty": request.form["under_thirty"],
        "user_id": session["user_id"],
    }

    recipe_id = Recipe.create(data)
    return redirect("/dashboard")


# DISPLAY ROUTE - shows details of a recipe
@app.route("/recipes/<int:id>")
def recipes_show(id):
    recipe = Recipe.get_one({"id": id})
    return render_template("recipes_show.html", recipe=recipe)


# DISPLAY ROUTE - shows the form to edit a recipe
@app.route("/recipes/<int:id>/edit")
def recipes_edit(id):
    if "user_id" not in session:
        return redirect("/")
    recipe = Recipe.get_one({"id": id})
    return render_template("recipes_edit.html", recipe=recipe)


# ACTION ROUTE - process the form from the edit route
@app.route("/recipes/<int:id>/update", methods=["POST"])
def update_recipe(id):
    is_valid = Recipe.validate(request.form)

    if not is_valid:
        return redirect("/update_recipe/{{ recipe.id }}")

    data = {
        "id": id,
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "date_cooked": request.form["date_cooked"],
        "under_thirty": request.form["under_thirty"],
    }

    Recipe.update(data)
    return redirect("/dashboard")


# ACTION ROUTE - delete a recipe
@app.post("/recipes/<int:recipe_id>/delete")
def delete_recipe(recipe_id):
    Recipe.delete_one({"id": recipe_id})
    return redirect("/dashboard")


# @app.post("/recipes/<int:recipe_id>/delete")
# def delete_recipe(id):
#     recipe = Recipe.delete_one({"id": id})
#     return render_template("dashboard.html", recipe=recipe)


# DISPLAY ROUTE - shows a list of all recipes
@app.route("/recipes")
def recipes_index():
    recipes = Recipe.get_all()
    return render_template("recipes_index.html", recipes=recipes)
