import os

from app import app
from database import db, get_user_by_username


USERNAME = "aleksa"


def main() -> None:
    new_password = os.getenv("RESET_ALEKSA_PASSWORD")

    if not new_password:
        print("RESET_ALEKSA_PASSWORD is not set. Skipping password reset.")
        return

    with app.app_context():
        user = get_user_by_username(USERNAME)

        if user is None:
            print(f"User '{USERNAME}' was not found.")
            return

        user.set_password(new_password)
        db.session.commit()

        print(f"Password for '{USERNAME}' was successfully changed.")


if __name__ == "__main__":
    main()