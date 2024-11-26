import streamlit as st
import pickle
import pandas as pd
import requests
import json

def fetch_poster(movie_id):
        
        responce=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=7298ad6cff97644bb462a59ffc78e286&language=en.US'.format(movie_id), timeout=10)
        print(movie_id)
        movie_data = responce.json()

        # Extract poster_path value
        poster_path = movie_data.get('poster_path', None)
        
        print("data",poster_path)
        print('responsece', responce)
        return "https://image.tmdb.org/t/p/w500/" + poster_path
def fetch_link(movie_id):
        
        responce=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=7298ad6cff97644bb462a59ffc78e286&language=en.US'.format(movie_id), timeout=10)
        print(movie_id)
        movie_data = responce.json()

        # Extract poster_path value
        poster_path = movie_data.get('homepage', None)
        
        print("data",poster_path)
        print('responsece', responce)
        return "https://image.tmdb.org/t/p/w500/" + poster_path
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distaces = similarity[movie_index]
    movies_list = sorted(list(enumerate(distaces)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies=[]
    recommended_movies_posters=[]
    recommended_movies_link=[]
    for i in movies_list:
         movie_id=movies.iloc[i[0]].movie_id
         recommended_movies.append(movies.iloc[i[0]].title)
         recommended_movies_posters.append(fetch_poster(movie_id))
         recommended_movies_link.append(fetch_link(movie_id))
    return recommended_movies,recommended_movies_posters,recommended_movies_link

movies_dict=pickle.load(open('movie_dict.pkl','rb'))

movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl','rb' ))

st.title("Movie Recommendation System")

selected_movie_name=st.selectbox('Ener the name af a movie',movies['title'].values)

if st.button("Recommend"):
    names,posters,link=recommend(selected_movie_name)
    col1,col2,col3,col4,col5=st.columns(5)

    with col1:
      st.text(names[0])
      st.image(posters[0])

    with col2:
       st.text(names[1])
       st.image(posters[1])

    with col3:
       st.text(names[2])
       st.image(posters[2])

    with col4:
          st.text(names[3])
          st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
