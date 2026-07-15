from flask_migrate import Migrate
import os
from pathlib import Path

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    g
)

from database import (
    db,
    create_database,
    add_post,
    get_posts_by_room,
    get_user_by_username,
    get_user_by_id
)


BASE_DIR = Path(__file__).resolve().parent
LOCAL_DATABASE_PATH = BASE_DIR / "rp_hub.db"

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY",
    "development-key-change-before-deployment"
)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{LOCAL_DATABASE_PATH.as_posix()}"
)

db.init_app(app)

migrate = Migrate(app, db)


rooms_data = {
    1: {
        "title": "Tolkien",
        "description": "A roleplay room set in Middle-earth."
    },
    2: {
        "title": "Historical Roleplay",
        "description": "A roleplay room set in the early 20th century."
    },
    3: {
        "title": "Lovecraft",
        "description": (
            "A roleplay room inspired by the Dreamlands "
            "and weird fiction."
        )
    }
}

@app.before_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = get_user_by_id(user_id)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get(
            "username",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        user = get_user_by_username(username)

        if user is None:
            error = "Invalid username or password."

        elif not user.check_password(password):
            error = "Invalid username or password."

        else:
            session.clear()
            session["user_id"] = user.id

            return redirect(url_for("rooms"))

    return render_template(
        "login.html",
        error=error
    )

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()

    return redirect(url_for("home"))


@app.route("/rooms")
def rooms():
    return render_template(
        "rooms.html",
        rooms=rooms_data
    )


@app.route("/room/<int:room_id>", methods=["GET", "POST"])
def room(room_id):
    room = rooms_data.get(room_id)

    if room is None:
        return "Room not found", 404

    if request.method == "POST":
        if g.user is None:
            return redirect(url_for("login"))

        character_name = request.form.get(
            "character_name",
            ""
        ).strip()

        content = request.form.get(
            "content",
            ""
        ).strip()

        if character_name and content:
            add_post(
                room_id,
                character_name,
                content
            )

        return redirect(
            url_for("room", room_id=room_id)
        )

    posts = get_posts_by_room(room_id)

    return render_template(
        "room.html",
        room=room,
        posts=posts
    )


if __name__ == "__main__":
    create_database(app)
    app.run(debug=True)