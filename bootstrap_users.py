import os

from app import app
from database import create_user, get_user_by_username


def ensure_user(
    username_variable: str,
    password_variable: str,
    role: str
) -> None:
    username = os.getenv(username_variable)
    password = os.getenv(password_variable)

    if not username or not password:
        print(
            f"Bootstrap skipped for role '{role}': "
            "credentials are not configured."
        )
        return

    existing_user = get_user_by_username(username)

    if existing_user is not None:
        print(
            f"Bootstrap skipped: user "
            f"'{existing_user.username}' already exists."
        )
        return

    new_user = create_user(
        username=username,
        password=password,
        role=role
    )

    print(
        f"Created production user "
        f"'{new_user.username}' with role '{new_user.role}'."
    )


def main() -> None:
    with app.app_context():
        ensure_user(
            username_variable="BOOTSTRAP_ADMIN_USERNAME",
            password_variable="BOOTSTRAP_ADMIN_PASSWORD",
            role="admin"
        )

        ensure_user(
            username_variable="BOOTSTRAP_GUEST_USERNAME",
            password_variable="BOOTSTRAP_GUEST_PASSWORD",
            role="guest"
        )

        ensure_user(
            username_variable="BOOTSTRAP_USER_USERNAME",
            password_variable="BOOTSTRAP_USER_PASSWORD",
            role=os.getenv(
                "BOOTSTRAP_USER_ROLE",
                "user"
            ).strip().lower()
        )

if __name__ == "__main__":
    main()