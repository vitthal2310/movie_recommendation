import streamlit as st
import pickle
import pandas as pd
import requests

API_KEY = "4c4517952c3d31110721ee235e799c77"

def fetch_poster(movie_name):
    """Fetch poster URL for a given movie name from TMDb."""
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"
    response = requests.get(search_url).json()

    if response['results']:
        poster_path = response['results'][0].get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return None

def recommend(movie_name):
    """Recommend 5 similar movies and return names + poster URLs."""
    movie_index = movies[movies['title'].str.lower() == movie_name.lower()].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        title = movies.iloc[i[0]].title
        recommended_movies.append(title)
        recommended_posters.append(fetch_poster(title))
    return recommended_movies, recommended_posters

# Load data
movies_dict = pickle.load(open('new_movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# UI
st.title("🎬 Movie Recommendation System")
selected_movie_name = st.selectbox("Enter the name of a movie", movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        with col:
            if poster:
                st.image(poster, use_container_width=True)  # Updated parameter
            st.caption(name)
