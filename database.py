from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Post(db.Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    room_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    character_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )


def create_database(app):
    with app.app_context():
        db.create_all()


def add_post(room_id, character_name, content):
    new_post = Post(
        room_id=room_id,
        character_name=character_name,
        content=content
    )

    db.session.add(new_post)
    db.session.commit()


def get_posts_by_room(room_id):
    statement = (
        db.select(Post)
        .where(Post.room_id == room_id)
        .order_by(Post.id.asc())
    )

    posts = db.session.execute(statement).scalars().all()

    return posts