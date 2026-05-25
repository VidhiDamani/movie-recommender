import streamlit as st
from recommend import recommend
import pandas as pd
import ast

# Load movie data (for the dropdown only)
movies = pd.read_csv('movies.csv')

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# 💖 Custom CSS — hover-expand cards and clean icon-based design
st.markdown("""
    <!-- Load FontAwesome for modern icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background-color: #0a0a0a;
        color: #fce4ec;
    }

    .stSelectbox label {
        color: #ffb6c1 !important;
        font-weight: 600;
        font-size: 1rem;
    }

    /* ── Card container ── */
    .movie-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid rgba(255, 64, 129, 0.18);
        border-radius: 18px;
        padding: 20px 24px;
        margin: 15px 0;
        cursor: pointer;
        overflow: hidden;
        max-height: 110px; /* Fits title + genre pill comfortably when closed */
        transition:
            max-height 0.5s cubic-bezier(0.4, 0, 0.2, 1),
            transform 0.3s cubic-bezier(0.4, 0, 0.2, 1),
            box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1),
            border-color 0.3s ease;
        position: relative;
    }

    /* Expand and highlight on hover */
    .movie-card:hover {
        max-height: 800px; /* Expands to fit full description */
        transform: translateY(-4px) scale(1.025);
        box-shadow: 0 10px 30px rgba(255, 64, 129, 0.25);
        border-color: #ff4081;
    }

    /* ── Title row ── */
    .card-title-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
    }

    .card-title {
        color: #ff80ab;
        font-size: 1.15rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .card-title i {
        font-size: 1.1rem;
        color: #ff4081;
    }

    /* Chevron rotation on hover */
    .chevron {
        font-size: 0.9rem;
        color: rgba(255, 128, 171, 0.5);
        transition: transform 0.4s ease, color 0.3s ease;
    }

    .movie-card:hover .chevron {
        transform: rotate(180deg);
        color: #ff4081;
    }

    /* ── Genre Container ── */
    .genre-container {
        margin-top: 10px;
    }

    .genre-pill {
        display: inline-block;
        background: rgba(255, 64, 129, 0.12);
        border: 1px solid rgba(255, 64, 129, 0.3);
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 0.78rem;
        color: #ff80ab;
        font-weight: 500;
        letter-spacing: 0.02em;
    }

    .genre-pill i {
        margin-right: 6px;
        color: #ff4081;
    }

    /* ── Expanded Description ── */
    .card-overview {
        opacity: 0;
        max-height: 0;
        overflow: hidden;
        transition: opacity 0.3s ease 0.1s, max-height 0.4s ease;
        color: #d8b4c8;
        font-size: 0.88rem;
        line-height: 1.6;
        margin: 0;
        padding-top: 0;
        border-top: 1px solid rgba(255, 64, 129, 0);
    }

    .movie-card:hover .card-overview {
        opacity: 1;
        max-height: 600px;
        padding-top: 16px;
        margin-top: 16px;
        border-top: 1px solid rgba(255, 64, 129, 0.15);
    }

    /* ── Headers ── */
    .app-title {
        color: #ff4081;
        font-weight: 700;
        font-size: 2.2rem;
        margin-bottom: 5px;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .app-subtitle {
        color: #ffb6c1;
        font-size: 1rem;
        margin-bottom: 25px;
        opacity: 0.85;
    }

    .section-header {
        color: #ff4081;
        font-size: 1.3rem;
        font-weight: 600;
        margin: 30px 0 15px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# 🌸 Clean Header
st.markdown('<div class="app-title"><i class="fa-solid fa-film"></i> Movie Recommender System</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">Find movies similar to your favorites — powered by cosine similarity</div>', unsafe_allow_html=True)

# Dropdown
selected_movie = st.selectbox("Choose a movie:", movies['title'].values)

# Recommend button
if st.button("Recommend"):
    results = recommend(selected_movie)

    if not results:
        st.error("No recommendations found. Try another movie!")
    else:
        st.markdown('<div class="section-header"><i class="fa-solid fa-wand-magic-sparkles"></i> Top 5 Picks For You</div>', unsafe_allow_html=True)

        for movie in results:
            genre_data = movie['genre']

            # Clean genre column
            if isinstance(genre_data, str):
                try:
                    parsed = ast.literal_eval(genre_data)
                    if isinstance(parsed, list):
                        if all(isinstance(i, dict) and 'name' in i for i in parsed):
                            genre_data = ', '.join([i['name'] for i in parsed])
                        else:
                            genre_data = ', '.join([str(i) for i in parsed])
                    else:
                        genre_data = str(parsed)
                except Exception:
                    genre_data = (
                        genre_data.replace('[', '').replace(']', '')
                        .replace('{', '').replace('}', '')
                        .replace("'", '').replace('"', '')
                        .replace('id:', '').replace('name:', ' ')
                    )

            # Get full description without truncation
            overview = movie['overview'] or "No description available."

            st.markdown(f"""
                <div class="movie-card">
                    <div class="card-title-row">
                        <div class="card-title">
                            <i class="fa-solid fa-clapperboard"></i>
                            {movie['title']}
                        </div>
                        <i class="fa-solid fa-chevron-down chevron"></i>
                    </div>
                    <div class="genre-container">
                        <span class="genre-pill">
                            <i class="fa-solid fa-tags"></i>
                            {genre_data}
                        </span>
                    </div>
                    <p class="card-overview">{overview}</p>
                </div>
            """, unsafe_allow_html=True)
