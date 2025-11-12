import streamlit as st
from recommend import recommend
import pandas as pd
import ast  # to safely parse list-like strings

# Load movie data
movies = pd.read_csv('movies.csv')

st.set_page_config(page_title="🎬 Movie Recommender", page_icon="🎀", layout="wide")

# 💖 Custom CSS
st.markdown("""
    <style>
    body {
        background-color: #0a0a0a;
        color: #fce4ec;
        font-family: 'Poppins', sans-serif;
    }

    .stSelectbox label {
        color: #ffb6c1 !important;
        font-weight: bold;
    }

    .movie-card {
        background-color: #1c1c1c;
        color: #ffb6c1;
        border-radius: 20px;
        padding: 20px;
        margin: 20px 0;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 0 10px #ffb6c1;
        cursor: pointer;
        overflow: hidden;
    }

    .movie-card:hover {
        transform: scale(1.08);
        background-color: #2a2a2a;
        box-shadow: 0 0 25px #ff4081;
        padding-bottom: 30px;
    }

    h3 {
        color: #ff80ab;
    }

    </style>
""", unsafe_allow_html=True)

# 🌸 Title
st.title(" 🍿 Movie Recommender System 🍿")
st.write("🎥 Find movies similar to your favorites — using cosine similarity 🎀")

# Dropdown
selected_movie = st.selectbox("Choose a movie:", movies['title'].values)

# Recommend button
if st.button("Recommend 💫"):
    results = recommend(selected_movie)
    if not results:
        st.error("No recommendations found. Try another movie! :(")
    else:
        st.subheader("✨ Recommended Movies ✨")
        for movie in results:
            genre_data = movie['genre']

            # 🧼 Clean genre column
            if isinstance(genre_data, str):
                try:
                    # Try to parse list or dict strings safely
                    parsed = ast.literal_eval(genre_data)
                    if isinstance(parsed, list):
                        # If list of dicts (TMDB style)
                        if all(isinstance(i, dict) and 'name' in i for i in parsed):
                            genre_data = ', '.join([i['name'] for i in parsed])
                        else:
                            genre_data = ', '.join([str(i) for i in parsed])
                    else:
                        genre_data = str(parsed)
                except:
                    # fallback: remove junk symbols
                    genre_data = (
                        genre_data.replace('[', '')
                        .replace(']', '')
                        .replace('{', '')
                        .replace('}', '')
                        .replace("'", '')
                        .replace('"', '')
                        .replace('id:', '')
                        .replace('name:', ' ')
                    )

            # 🎬 Movie display card
            st.markdown(f"""
                <div class="movie-card">
                    <h3>🎬 {movie['title']}</h3>
                    <p><b>Genre:</b> {genre_data}</p>
                    <p><b>About:</b> {movie['overview']}</p>
                </div>
            """, unsafe_allow_html=True)
