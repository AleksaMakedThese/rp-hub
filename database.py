import sqlite3


def create_database():
    connection = sqlite3.connect("rp_hub.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id INTEGER NOT NULL,
            character_name TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def add_post(room_id, character_name, content):
    connection = sqlite3.connect("rp_hub.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO posts (room_id, character_name, content)
        VALUES (?, ?, ?)
    """, (room_id, character_name, content))

    connection.commit()
    connection.close()


def get_posts_by_room(room_id):
    connection = sqlite3.connect("rp_hub.db")

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, room_id, character_name, content
        FROM posts
        WHERE room_id = ?
        ORDER BY id ASC
    """, (room_id,))

    posts = cursor.fetchall()

    connection.close()

    return posts