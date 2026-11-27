
import streamlit as st

from auth import register_user, login_user
from views.home import show_home


# ==========================================
# KONFIGURASI HALAMAN
# ==========================================

st.set_page_config(
    page_title="VYBES - Your Mood, Your Music",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==========================================
# SESSION STATE
# ==========================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "login"

if "show_logout" not in st.session_state:
    st.session_state.show_logout = False


# ==========================================
# CSS GLOBAL VYBES
# ==========================================

st.markdown("""
<style>

/* BACKGROUND */
.stApp {
    background:
        radial-gradient(
            circle at 80% 10%,
            #38205e 0%,
            transparent 35%
        ),
        linear-gradient(
            145deg,
            #17102c,
            #100e20 65%,
            #090912
        );
}

/* HEADER STREAMLIT */
header[data-testid="stHeader"] {
    background: transparent;
}

/* KONTEN RESPONSIVE */
.block-container {
    width: 94% !important;
    max-width: 1450px !important;
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;
}

/* BRAND */
.brand {
    width: 100%;
    text-align: center;
    padding-top: 10px;
    margin-bottom: 35px;
}

.brand-tagline {
    color: #aaa0c4;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 2.5px;
    text-align: center;
    margin-top: 15px;
}

/* WELCOME */
.welcome {
    text-align: center;
    margin: 25px 0 35px;
}

.welcome h2 {
    color: white;
    font-size: 27px;
    font-weight: 800;
}

.welcome p {
    color: #aaa0bd;
    font-size: 15px;
}

/* INPUT */
div[data-baseweb="input"] {
    background: #1b1628;
    border: 1px solid #423052;
    border-radius: 11px;
}

div[data-baseweb="input"] input {
    color: white !important;
}

div[data-baseweb="input"] input::placeholder {
    color: #898197 !important;
}

.stTextInput label {
    color: #eeeaf7 !important;
    font-weight: 600;
}

/* BUTTON */
div.stButton > button {
    width: 100%;
    min-height: 48px;
    background: linear-gradient(
        90deg,
        #a37aff,
        #773ee0
    );
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 700;
    transition: 0.2s;
}

div.stButton > button:hover {
    background: linear-gradient(
        90deg,
        #b594ff,
        #925cf0
    );
    color: white;
    border: 1px solid #c6aaff;
}

/* ALERT MENGIKUT TEMA STREAMLIT */
div[data-testid="stAlert"] p,
div[data-testid="stAlert"] span,
div[data-testid="stAlert"] [data-testid="stMarkdownContainer"] {
    color: var(--text-color) !important;
}

/* LOGOUT CARD */
.logout-card {
    background: linear-gradient(
        145deg,
        #21162f,
        #100e1b
    );
    border: 1px solid #49305e;
    border-radius: 24px;
    padding: 40px 25px;
    text-align: center;
    max-width: 650px;
    margin: 30px auto;
}

.logout-icon {
    width: 90px;
    height: 90px;
    border-radius: 50%;
    background: #382451;
    color: #c3a0ff;
    font-size: 48px;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 20px auto 30px;
}

.logout-card h2 {
    color: white;
    font-size: 25px;
    font-weight: 800;
}

.logout-card p {
    color: #aaa0bd;
    font-size: 14px;
}

/* FOOTER */
.footer {
    text-align: center;
    color: #81778e;
    font-size: 12px;
    margin-top: 25px;
    line-height: 1.8;
}

/* RESPONSIVE HP */
@media screen and (max-width: 640px) {

    .block-container {
        width: 94% !important;
        padding: 1.2rem 0.5rem 3rem !important;
    }

    .welcome h2 {
        font-size: 22px;
    }

    .welcome p {
        font-size: 13px;
    }

    .logout-card {
        padding: 25px 15px;
    }
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# LOGO VYBES
# ==========================================

def show_brand():

    st.markdown(
        '<div class="brand">',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.image(
            "assets/vybes_logo.png",
            width=220
        )

    st.markdown("""
        <div class="brand-tagline">
            MUSIC THAT MATCHES YOUR MOMENT
        </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ==========================================
# HALAMAN LOGIN DAN REGISTER
# ==========================================

if not st.session_state.logged_in:

    show_brand()

    # ======================================
    # LOGIN
    # ======================================

    if st.session_state.page == "login":

        st.markdown("""
        <div class="welcome">
            <h2>Selamat Datang Kembali</h2>
            <p>Masuk dan temukan musik favoritmu</p>
        </div>
        """, unsafe_allow_html=True)

        email = st.text_input(
            "Email",
            placeholder="Masukkan email kamu",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            placeholder="Masukkan password",
            type="password",
            key="login_password"
        )

        if st.button("Masuk", use_container_width=True):

            if not email.strip() or not password:
                st.warning("Semua kolom harus diisi.")

            else:
                user = login_user(email.strip(), password)

                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.session_state.page = "home"
                    st.session_state.show_logout = False
                    st.rerun()

                else:
                    st.error("Email atau password salah.")

        st.markdown("""
        <div class="footer">
            Belum punya akun? Buat akun baru di bawah.
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 1.5, 1])

        with col2:

            if st.button(
                "Daftar Sekarang",
                key="register_button",
                use_container_width=True
            ):
                st.session_state.page = "register"
                st.rerun()

    # ======================================
    # REGISTER
    # ======================================

    elif st.session_state.page == "register":

        st.markdown("""
        <div class="welcome">
            <h2>Buat Akun VYBES</h2>
            <p>Daftar dan nikmati musik favoritmu</p>
        </div>
        """, unsafe_allow_html=True)

        nama = st.text_input(
            "Nama Lengkap",
            placeholder="Masukkan nama kamu",
            key="register_name"
        )

        email = st.text_input(
            "Email",
            placeholder="Masukkan email kamu",
            key="register_email"
        )

        password = st.text_input(
            "Password",
            placeholder="Buat password minimal 8 karakter",
            type="password",
            key="register_password"
        )

        konfirmasi = st.text_input(
            "Konfirmasi Password",
            placeholder="Masukkan ulang password",
            type="password",
            key="confirm_password"
        )

        if st.button("Buat Akun", use_container_width=True):

            if (
                not nama.strip()
                or not email.strip()
                or not password
                or not konfirmasi
            ):
                st.warning("Semua kolom harus diisi.")

            elif "@" not in email or "." not in email:
                st.warning("Masukkan email yang valid.")

            elif len(password) < 8:
                st.warning("Password minimal 8 karakter.")

            elif password != konfirmasi:
                st.error("Konfirmasi password tidak cocok.")

            else:
                berhasil, pesan = register_user(
                    nama.strip(),
                    email.strip(),
                    password
                )

                if berhasil:
                    st.success(pesan)
                    st.session_state.page = "login"
                    st.rerun()

                else:
                    st.error(pesan)

        st.write("")

        col1, col2, col3 = st.columns([1, 1.5, 1])

        with col2:

            if st.button(
                "Kembali ke Login",
                use_container_width=True
            ):
                st.session_state.page = "login"
                st.rerun()


# ==========================================
# SETELAH LOGIN BERHASIL
# ==========================================

else:

    # ======================================
    # KONFIRMASI LOGOUT
    # ======================================

    if st.session_state.show_logout:

        st.markdown("""
        <div class="logout-card">

            <div class="logout-icon">↪</div>

            <h2>Yakin ingin keluar?</h2>

            <p>
                Kamu harus masuk kembali untuk
                mengakses akun VYBES.
            </p>

        </div>
        """, unsafe_allow_html=True)

        st.write("")

        col1, col2, col3 = st.columns([1, 1.5, 1])

        with col2:

            if st.button(
                "Ya, Keluar",
                use_container_width=True
            ):

                st.session_state.logged_in = False
                st.session_state.user = None
                st.session_state.show_logout = False
                st.session_state.page = "login"

                st.session_state.pop(
                    "home_recommendations",
                    None
                )

                st.rerun()

            if st.button(
                "Batal",
                use_container_width=True
            ):

                st.session_state.show_logout = False
                st.rerun()

        st.markdown("""
        <div class="footer">
            Musik favoritmu menunggumu kembali.
        </div>
        """, unsafe_allow_html=True)

    # ======================================
    # BERANDA
    # ======================================

    else:
        show_home()
