
import streamlit as st
import pandas as pd
from database.connection import get_connection
from recommendation import get_recommendations


# ==========================================
# MENGAMBIL DATA LAGU DARI MYSQL
# ==========================================

def get_songs():
    db = get_connection()

    if db is None:
        return pd.DataFrame()

    try:
        return pd.read_sql(
            "SELECT * FROM songs ORDER BY id",
            db
        )
    except Exception as error:
        st.error(f"Gagal mengambil data lagu: {error}")
        return pd.DataFrame()
    finally:
        db.close()


# ==========================================
# HALAMAN BERANDA
# ==========================================

def show_home():

    user = st.session_state.user
    nama = user["nama"] if user else "Pengguna"

    semua_lagu = get_songs()

    # ======================================
    # CSS RESPONSIVE
    # ======================================

    st.markdown("""
    <style>

    /* AREA UTAMA */
    .block-container {
        max-width: 1450px !important;
        width: 94% !important;
        padding-top: 2rem !important;
        padding-bottom: 5rem !important;
    }

    /* HEADER */
    .home-brand {
        font-size: 30px;
        font-weight: 900;
        letter-spacing: 2px;
        color: white;
        margin-bottom: 35px;
    }

    .greeting {
        color: #aaa0bd;
        font-size: 15px;
        margin-bottom: 5px;
    }

    .main-heading {
        color: white;
        font-size: clamp(27px, 3vw, 42px);
        font-weight: 850;
        margin-bottom: 25px;
        line-height: 1.2;
    }

    /* SECTION */
    .section-title {
        color: white;
        font-size: 22px;
        font-weight: 800;
        margin-top: 35px;
        margin-bottom: 17px;
    }

    /* SEARCH */
    div[data-testid="stTextInput"] input {
        background: #1c192b;
        color: white !important;
        border: 1px solid #403354;
        border-radius: 13px;
        min-height: 52px;
        font-size: 15px;
    }

    div[data-testid="stTextInput"] input::placeholder {
        color: #898198;
    }

    /* MOOD BUTTON */
    div.stButton > button {
        border-radius: 13px;
        min-height: 52px;
        font-size: 15px;
        font-weight: 700;
        background: linear-gradient(
            100deg,
            #a77aff,
            #773ee0
        );
        color: white;
        border: none;
    }

    div.stButton > button:hover {
        color: white;
        border: 1px solid #d0b5ff;
    }

    /* MIX CARD */
    .mix-card {
        display: flex;
        align-items: center;
        gap: 22px;
        background: linear-gradient(
            110deg,
            #2b1d48,
            #211a39
        );
        border: 1px solid #493363;
        border-radius: 20px;
        padding: 22px;
        margin-bottom: 15px;
    }

    .mix-art {
        width: 115px;
        height: 115px;
        min-width: 115px;
        border-radius: 16px;
        background: linear-gradient(
            135deg,
            #dda0ff,
            #8950ef
        );
        display: flex;
        align-items: center;
        justify-content: center;
        color: #291344;
        font-size: 58px;
        font-weight: 900;
    }

    .mix-label {
        color: #c6a5ff;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1.5px;
    }

    .mix-name {
        color: white;
        font-size: 23px;
        font-weight: 800;
        margin-top: 7px;
    }

    .mix-info {
        color: #aaa0bd;
        font-size: 13px;
        margin-top: 7px;
    }

    /* SONG LIST */
    .song-row {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 12px 5px;
        border-bottom: 1px solid rgba(255,255,255,0.07);
    }

    .song-art {
        width: 58px;
        height: 58px;
        min-width: 58px;
        border-radius: 12px;
        background: linear-gradient(
            135deg,
            #60d8ef,
            #6572ed
        );
    }

    .song-art.purple {
        background: linear-gradient(
            135deg,
            #e1a0ff,
            #8650ed
        );
    }

    .song-name {
        color: white;
        font-size: 16px;
        font-weight: 750;
    }

    .song-artist {
        color: #9991ad;
        font-size: 13px;
        margin-top: 4px;
    }

    /* FOOTER */
    .home-footer {
        color: #8c83a5;
        text-align: center;
        font-size: 12px;
        margin-top: 55px;
    }

    /* RESPONSIVE HP */
    @media screen and (max-width: 640px) {

        .block-container {
            width: 94% !important;
            padding: 1rem 0.5rem 4rem !important;
        }

        .home-brand {
            font-size: 24px;
            margin-bottom: 25px;
        }

        .greeting {
            font-size: 13px;
        }

        .main-heading {
            font-size: 26px;
        }

        .section-title {
            font-size: 19px;
            margin-top: 27px;
        }

        .mix-card {
            padding: 14px;
            gap: 13px;
        }

        .mix-art {
            width: 85px;
            height: 85px;
            min-width: 85px;
            font-size: 42px;
        }

        .mix-name {
            font-size: 17px;
        }

        .mix-info {
            font-size: 11px;
        }

        .song-art {
            width: 48px;
            height: 48px;
            min-width: 48px;
        }

        .song-name {
            font-size: 14px;
        }

        .song-artist {
            font-size: 11px;
        }
    }

    </style>
    """, unsafe_allow_html=True)

    # ======================================
    # HEADER
    # ======================================

    st.markdown(
        '<div class="home-brand">VYBES</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="greeting">Selamat datang kembali,</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="main-heading">Lagi ingin dengar apa, {nama}?</div>',
        unsafe_allow_html=True
    )

    # ======================================
    # SEARCH
    # ======================================

    pencarian = st.text_input(
        "Cari lagu",
        placeholder="Cari lagu, artis, atau suasana...",
        label_visibility="collapsed",
        key="home_search"
    )

    if pencarian.strip():

        if not semua_lagu.empty:

            hasil_cari = semua_lagu[
                semua_lagu.apply(
                    lambda row: pencarian.lower() in (
                        str(row["judul"]) + " " +
                        str(row["artis"]) + " " +
                        str(row["genre"])
                    ).lower(),
                    axis=1
                )
            ]

            st.markdown(
                '<div class="section-title">Hasil Pencarian</div>',
                unsafe_allow_html=True
            )

            if not hasil_cari.empty:

                for _, lagu in hasil_cari.iterrows():
                    st.markdown(
                        f"""
                        <div class="song-row">
                            <div class="song-art"></div>
                            <div>
                                <div class="song-name">{lagu['judul']}</div>
                                <div class="song-artist">{lagu['artis']}</div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            else:
                st.info("Lagu tidak ditemukan.")

    # ======================================
    # MOOD
    # ======================================

    st.markdown(
        '<div class="section-title">Pilih mood kamu</div>',
        unsafe_allow_html=True
    )

    if "selected_mood" not in st.session_state:
        st.session_state.selected_mood = "Senang"

    mood_options = [
        ("Happy", "Senang"),
        ("Chill", "Santai"),
        ("Focus", "Semangat")
    ]

    mood_columns = st.columns(3)

    for i, (label, value) in enumerate(mood_options):

        with mood_columns[i]:

            if st.button(
                label,
                key=f"mood_{value}",
                use_container_width=True
            ):
                st.session_state.selected_mood = value

    st.caption(
        f"Mood yang dipilih: {st.session_state.selected_mood}"
    )

    # ======================================
    # VYBES MIX
    # ======================================

    st.markdown("""
    <div class="section-title">Rekomendasi untukmu</div>

    <div class="mix-card">
        <div class="mix-art">●</div>
        <div>
            <div class="mix-label">VYBES MIX</div>
            <div class="mix-name">Your daily soundtrack</div>
            <div class="mix-info">
                Personal music recommendation
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button(
        "Temukan rekomendasi lagu",
        use_container_width=True
    ):

        mood = st.session_state.selected_mood

        aktivitas = (
            "Belajar" if mood == "Semangat"
            else "Santai"
        )

        hasil = get_recommendations(mood, aktivitas)

        st.session_state.home_recommendations = hasil

    # ======================================
    # HASIL REKOMENDASI
    # ======================================

    if "home_recommendations" in st.session_state:

        hasil = st.session_state.home_recommendations

        if not hasil.empty:

            st.markdown(
                '<div class="section-title">Lagu untukmu</div>',
                unsafe_allow_html=True
            )

            for _, lagu in hasil.head(5).iterrows():

                st.markdown(
                    f"""
                    <div class="song-row">
                        <div class="song-art purple"></div>
                        <div>
                            <div class="song-name">{lagu['judul']}</div>
                            <div class="song-artist">{lagu['artis']} · {lagu['genre']}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.caption(
                    f"Skor kecocokan: {lagu['skor_kecocokan']}%"
                )

        else:
            st.info("Belum ada lagu yang cocok.")

    # ======================================
    # KOLEKSI LAGU
    # ======================================

    st.markdown(
        '<div class="section-title">Koleksi lagu</div>',
        unsafe_allow_html=True
    )

    if not semua_lagu.empty:

        for i, (_, lagu) in enumerate(
            semua_lagu.head(8).iterrows()
        ):

            warna = "purple" if i % 2 else ""

            st.markdown(
                f"""
                <div class="song-row">
                    <div class="song-art {warna}"></div>
                    <div>
                        <div class="song-name">{lagu['judul']}</div>
                        <div class="song-artist">{lagu['artis']}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:
        st.info("Belum ada koleksi lagu.")

    # ======================================
    # FOOTER
    # ======================================

    st.markdown("""
    <div class="home-footer">
        VYBES MUSIC · YOUR MOOD, YOUR MUSIC
    </div>
    """, unsafe_allow_html=True)
