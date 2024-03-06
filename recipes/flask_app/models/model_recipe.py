from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash, session
from flask_app.models.model_user import User


class Recipe:
    def __init__(self, data: dict):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.date_cooked = data["date_cooked"]
        self.under_thirty = data["under_thirty"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.creator = None  # THIS WILL HOLD USER OBJECT LATER

    @classmethod
    def create(cls, data: dict) -> int:
        query = "INSERT INTO recipes (name, description, instructions, date_cooked, under_thirty, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_cooked)s, %(under_thirty)s, %(user_id)s);"
        id = connectToMySQL(DATABASE).query_db(query, data)
        return id

    @classmethod
    def get_all(cls):
        query = """
    SELECT * FROM recipes
    JOIN users ON recipes.user_id = users.id;
    """
        results = connectToMySQL(DATABASE).query_db(query)

        if not results:
            return []

        instance_list = []
        for dict in results:
            recipe_instance = cls(dict)
            user_data = {
                "id": dict["users.id"],
                "first_name": dict["first_name"],
                "last_name": dict["last_name"],
                "email": dict["email"],
                "password": dict["password"],
                "created_at": dict["users.created_at"],
                "updated_at": dict["users.updated_at"],
            }
            user_instance = User(user_data)
            recipe_instance.creator = user_instance
            instance_list.append(recipe_instance)
        print("ALL THE RECIPES AND THEIR USER ----------->", instance_list)
        return instance_list

    @classmethod
    def get_one(cls, data: dict):
        query = """
    SELECT * FROM recipes
    LEFT JOIN users ON recipes.user_id = users.id
    WHERE recipes.id = %(id)s;
    """
        results = connectToMySQL(DATABASE).query_db(query, data)

        if not results:
            return None

        dict = results[0]
        recipe_instance = cls(dict)
        user_object = User(dict)
        recipe_instance.creator = user_object
        return recipe_instance

    @classmethod
    def delete_one(cls, data: dict):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def update(cls, data: dict):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, date_cooked=%(date_cooked)s, under_thirty=%(under_thirty)s WHERE id=%(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate(data: dict) -> bool:
        is_valid = True

        if len(data["name"]) < 2:
            flash("name is required", "err_recipes_name")
            print("name is required")
            print("err_recipes_name")
            is_valid = False
        if len(data["description"]) < 2:
            flash("description is required", "err_recipes_description")
            print("description is required")
            print("err_recipes_description")
            is_valid = False
        if len(data["instructions"]) < 7:
            flash("instructions is required", "err_recipes_instructions")
            print("instructions is required")
            print("err_recipes_instructions")
            is_valid = False
        if len(data["date_cooked"]) < 8:
            flash("date_cooked is required", "err_users_date_cooked")
            print("date_cooked is required")
            print("err_recipes_date_cooked")
            is_valid = False
        if len(data["under_thirty"]) < 1:
            flash("under_thirty is required", "err_recipes_under_thirty")
            print("under_thirty is required")
            print("err_recipes_under_thirty")
            is_valid = False

        return is_valid
