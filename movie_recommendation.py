from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from data_preprocessing import df
import requests
import os

# Count Vectorizer
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(df['tags']).toarray()

# Cosine Similarity
similarity = cosine_similarity(vectors)
API_KEY = os.environ.get("API_KEY")


def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=d38d55133de3ba9149e75b5310a6bdf4&language=en-US'.format(
            movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = df[df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    for i in movie_list:
        print(df.iloc[i[0]].title)


def recommend_for_app(movie):
    movie_index = df[df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = list()
    recommended_movies_posters = list()
    for i in movie_list:
        movie_id = df.iloc[i[0]].movie_id
        recommended_movies.append(df.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters
