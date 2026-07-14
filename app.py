from database import create_database, add_post, get_posts_by_room
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


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
        "description": "A roleplay room inspired by the Dreamlands and weird fiction."
    }
}


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/rooms")
def rooms():
    return render_template("rooms.html", rooms=rooms_data)


@app.route("/room/<int:room_id>", methods=["GET", "POST"])
def room(room_id):
    room = rooms_data.get(room_id)

    if room is None:
        return "Room not found", 404

    if request.method == "POST":
        character_name = request.form.get("character_name", "").strip()
        content = request.form.get("content", "").strip()

        if character_name and content:
            add_post(room_id, character_name, content)

        return redirect(url_for("room", room_id=room_id))

    posts = get_posts_by_room(room_id)

    return render_template(
        "room.html",
        room=room,
        posts=posts
    )


if __name__ == "__main__":
    create_database()
    app.run(debug=True)