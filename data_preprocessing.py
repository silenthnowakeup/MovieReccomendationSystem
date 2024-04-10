import ast
import pandas as pd
from nltk.stem.porter import PorterStemmer


ps = PorterStemmer()


def convert(obj):
    names = list()
    for i in ast.literal_eval(obj):
        names.append(i["name"])
    return names


def convert_cast(obj):
    names = list()
    counter = 0
    for i in ast.literal_eval(obj):
        if counter != 3:
            names.append(i["name"])
            counter += 1
        else:
            break
    return names


def convert_crew(obj):
    names = list()
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            names.append(i["name"])
            break
    return names


def stem(text: str):
    y = [ps.stem(word) for word in text.split()]
    return ' '.join(y)


def preprocess_data():
    movies = pd.read_csv("data/tmdb_5000_movies.csv")
    credits = pd.read_csv("data/tmdb_5000_credits.csv")

    movies = movies.merge(credits, on="title")

    movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
    movies.dropna(inplace=True)

    movies['genres'] = movies['genres'].apply(convert)
    movies['keywords'] = movies['keywords'].apply(convert)
    movies['cast'] = movies['cast'].apply(convert_cast)
    movies['crew'] = movies['crew'].apply(convert_crew)

    movies['overview'] = movies['overview'].apply(lambda x: x.split())
    movies[['genres', 'keywords', 'cast', 'crew']] = movies[['genres', 'keywords', 'cast', 'crew']].apply(
        lambda col: col.map(lambda x: [i.replace(" ", "") for i in x]))
    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
    new_df = movies[['movie_id', 'title', 'tags']]
    new_df.loc[:, 'tags'] = new_df['tags'].apply(lambda x: " ".join(x)).str.lower()

    new_df.loc[:, 'tags'] = new_df['tags'].apply(stem)
    return new_df

df = preprocess_data()
