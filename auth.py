import hashlib
import secrets
from database.connection import get_connection


def hash_password(password):
    salt = secrets.token_hex(16)

    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        600000
    ).hex()

    return f"{salt}${hashed}"


def verify_password(password, stored_password):
    try:
        salt, saved_hash = stored_password.split("$")

        hashed = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            600000
        ).hex()

        return secrets.compare_digest(hashed, saved_hash)

    except (ValueError, AttributeError):
        return False


def register_user(nama, email, password):
    db = get_connection()

    if db is None:
        return False, "Koneksi database gagal."

    cursor = db.cursor()

    try:
        password_hash = hash_password(password)

        cursor.execute(
            """
            INSERT INTO users (nama, email, password_hash)
            VALUES (%s, %s, %s)
            """,
            (nama, email, password_hash)
        )

        db.commit()

        return True, "Akun berhasil dibuat!"

    except Exception as error:
        db.rollback()

        if getattr(error, "errno", None) == 1062:
            return False, "Email sudah terdaftar."

        return False, "Gagal membuat akun. Periksa database."

    finally:
        cursor.close()
        db.close()


def login_user(email, password):
    db = get_connection()

    if db is None:
        return None

    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT id, nama, email, password_hash
            FROM users
            WHERE email = %s
            """,
            (email,)
        )

        user = cursor.fetchone()

        if user and verify_password(
            password,
            user["password_hash"]
        ):
            return {
                "id": user["id"],
                "nama": user["nama"],
                "email": user["email"]
            }

        return None

    finally:
        cursor.close()
        db.close()
