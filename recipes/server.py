from flask_app import app
from flask_app.controllers import (
    controller_users,
    controller_routes,
    controller_recipes,
)

app.secret_key = "keep it secret, keep it safe"


if __name__ == "__main__":
    app.run(debug=True)
