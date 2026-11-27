
import pandas as pd
from database.connection import get_connection


def get_recommendations(mood, aktivitas):
    db = get_connection()

    if db is None:
        return pd.DataFrame()

    query = """
        SELECT * FROM songs
    """

    try:
        data = pd.read_sql(query, db)

        # Menghitung kecocokan mood dan aktivitas
        data["skor_kecocokan"] = (
            (data["mood"] == mood).astype(int) * 50
            + (data["aktivitas"] == aktivitas).astype(int) * 50
        )

        # Mengurutkan lagu dari skor tertinggi
        hasil = data[data["skor_kecocokan"] > 0]
        hasil = hasil.sort_values(
            by="skor_kecocokan",
            ascending=False
        )

        return hasil

    finally:
        db.close()
