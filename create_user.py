from getpass import getpass

from app import app
from database import create_database, create_user


def main():
    create_database(app)

    username = input("Username: ").strip()
    password = getpass("Password: ")
    password_confirmation = getpass("Confirm password: ")

    if password != password_confirmation:
        print("Passwords do not match.")
        return

    role = input(
        "Role [user/guest/admin]: "
    ).strip().lower()

    if not role:
        role = "user"

    try:
        with app.app_context():
            user = create_user(
                username=username,
                password=password,
                role=role
            )

            created_username = user.username
            created_role = user.role

        print(
            f"User '{created_username}' "
            f"created with role '{created_role}'."
        )

    except ValueError as error:
        print(f"Could not create user: {error}")


if __name__ == "__main__":
    main()