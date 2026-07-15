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
    add_post,
    get_posts_by_room,
    get_user_by_username,
    get_user_by_id
)


BASE_DIR = Path(__file__).resolve().parent
LOCAL_DATABASE_PATH = BASE_DIR / "rp_hub.db"

app = Flask(__name__)


APP_ENV = os.getenv("APP_ENV", "development")
IS_PRODUCTION = APP_ENV == "production"


secret_key = os.getenv("SECRET_KEY")

if IS_PRODUCTION and not secret_key:
    raise RuntimeError(
        "SECRET_KEY must be set in production."
    )

app.config["SECRET_KEY"] = (
    secret_key
    or "local-development-key"
)


database_url = os.getenv("DATABASE_URL")

if IS_PRODUCTION and not database_url:
    raise RuntimeError(
        "DATABASE_URL must be set in production."
    )

app.config["SQLALCHEMY_DATABASE_URI"] = (
    database_url
    or f"sqlite:///{LOCAL_DATABASE_PATH.as_posix()}"
)


app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True
}


app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = IS_PRODUCTION


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

        if not g.user.can_publish:
            return "This account has read-only access.", 403

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
                room_id=room_id,
                user_id=g.user.id,
                character_name=character_name,
                content=content
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
    app.run(debug=True)