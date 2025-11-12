import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load your dataset
movies = pd.read_csv('movies.csv')

# Make sure your CSV has 'title', 'genres', 'overview' columns
movies['overview'] = movies['overview'].fillna('')
movies['genres'] = movies['genres'].fillna('')

# Combine genres + overview
movies['tags'] = movies['overview'] + ' ' + movies['genres']

# Convert text to vectors
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies['tags']).toarray()

# Calculate cosine similarity
similarity = cosine_similarity(vectors)

# Function to recommend movies
def recommend(movie):
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
