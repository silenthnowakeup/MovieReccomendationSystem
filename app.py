import streamlit as st
from data_preprocessing import df
from movie_recommendation import recommend_for_app
movie_list = df['title'].values

st.title("Movie Recommendation System")

selected_movie = st.selectbox(
    'How would you like to be contacted?',
    movie_list)

if st.button('Recommend'):
    names, posters = recommend_for_app(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
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
