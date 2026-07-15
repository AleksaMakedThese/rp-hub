from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash


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


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="user"
    )

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(
            self.password_hash,
            password
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

    posts = db.session.execute(
        statement
    ).scalars().all()

    return posts


def get_user_by_username(username):
    normalized_username = username.strip().lower()

    statement = db.select(User).where(
        User.username == normalized_username
    )

    user = db.session.execute(
        statement
    ).scalar_one_or_none()

    return user


def create_user(username, password, role="user"):
    normalized_username = username.strip().lower()

    if not normalized_username:
        raise ValueError("Username cannot be empty.")

    if not password:
        raise ValueError("Password cannot be empty.")

    allowed_roles = {"user", "guest", "admin"}

    if role not in allowed_roles:
        raise ValueError(
            "Role must be user, guest, or admin."
        )

    existing_user = get_user_by_username(
        normalized_username
    )

    if existing_user is not None:
        raise ValueError(
            "A user with this username already exists."
        )

    new_user = User(
        username=normalized_username,
        role=role
    )

    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return new_user
def get_user_by_id(user_id):
    return db.session.get(User, user_id)