import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@st.cache_resource(show_spinner="Loading movie data...")
def load_model():
    """Load dataset and build similarity matrix once, cached for the session."""
    movies = pd.read_csv('movies.csv')

    movies['overview'] = movies['overview'].fillna('')
    movies['genres'] = movies['genres'].fillna('')

    # Combine genres + overview into tags
    movies['tags'] = movies['overview'] + ' ' + movies['genres']

    # Convert text to vectors
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(movies['tags']).toarray()

    # Calculate cosine similarity matrix
    similarity = cosine_similarity(vectors)

    return movies, similarity


def recommend(movie):
    movies, similarity = load_model()

    movie = movie.lower().strip()
    movie_index = None
    for i, title in enumerate(movies['title'].str.lower()):
        if movie == title:
            movie_index = i
            break

    if movie_index is None:
        return []

    distances = similarity[movie_index]
    movie_list = sorted(
        list(enumerate(distances)), reverse=True, key=lambda x: x[1]
    )[1:6]  # top 5 similar movies

    recommended = []
    for i in movie_list:
        data = {
            "title": movies.iloc[i[0]].title,
            "genre": movies.iloc[i[0]].genres,
            "overview": movies.iloc[i[0]].overview,
        }
        recommended.append(data)

    return recommended
