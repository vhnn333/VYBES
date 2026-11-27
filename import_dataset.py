import pandas as pd
from database.connection import get_connection

# Membaca dataset CSV
data = pd.read_csv("data/songs.csv")

# Menghubungkan ke database
db = get_connection()

if db:
    cursor = db.cursor()

    # Memasukkan data lagu
    sql = """
        INSERT INTO songs
        (judul, artis, genre, mood, aktivitas, energi)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = [
        tuple(row)
        for row in data[
            ["judul", "artis", "genre", "mood", "aktivitas", "energi"]
        ].itertuples(index=False, name=None)
    ]

    try:
        cursor.executemany(sql, values)
        db.commit()

        print("Dataset berhasil dimasukkan!")
        print("Jumlah lagu:", cursor.rowcount)

    except Exception as error:
        db.rollback()
        print("Gagal memasukkan dataset:", error)

    finally:
        cursor.close()
        db.close()

else:
    print("Koneksi database gagal!")
