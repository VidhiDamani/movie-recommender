import pickle
import numpy as np
import streamlit as st


@st.cache_resource(show_spinner="Loading movie data...")
def load_model():
    """Load precomputed similarity data — instant startup, no heavy computation."""
    import pandas as pd

    with open('movies_slim.pkl', 'rb') as f:
        movies = pickle.load(f)

    top10 = np.load('similarity_top10.npy')

    return movies, top10


def recommend(movie):
    movies, top10 = load_model()

    movie = movie.lower().strip()
    movie_index = None
    titles_lower = movies['title'].str.lower().tolist()
    for i, title in enumerate(titles_lower):
        if movie == title:
            movie_index = i
            break

    if movie_index is None:
        return []

    similar_indices = top10[movie_index]

    recommended = []
    for i in similar_indices:
        data = {
            "title": movies.iloc[int(i)]['title'],
            "genre": movies.iloc[int(i)]['genres'],
            "overview": movies.iloc[int(i)]['overview'],
        }
        recommended.append(data)

    return recommended
