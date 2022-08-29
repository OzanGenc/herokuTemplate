import streamlit as st
import requests
import os
import pandas as pd
import matplotlib.pyplot as plt


st.title("Cocktail Recommender 2.0!")


st.markdown("Cocktail Recommender 2.0 is an improved version of [Cocktail Recommender](https://cocktail-recommender.herokuapp.com/). It is a tool that recommends cocktails based on provided name, ingredients or description of a cocktail using Artificial Intelligence.")
st.markdown("You can provide name of a cocktail (e.g. Margarita) to find similar cocktails to it, you can write ingedients (e.g. Vodka, Orange juice) or you can describe (e.g. fruity, refreshing) what kind of cocktail you would like to enjoy, and get recommendations based on that.")
st.markdown("Cheers :tropical_drink:")


embedding_button = st.radio(
  "Similarity will be calculated using either Ingredients or All Information about the cocktail.",
  ('Only Ingredients', 'All Information'))

if embedding_button == 'Only Ingredients':
  df = pd.read_pickle("./df_universal_embedded_ingredients.pkl")
  similarity_df = pd.read_pickle("./similarity_ingredients_df.pkl")

else:
  df = pd.read_pickle("./df_universal_embedded_content.pkl")
  similarity_df = pd.read_pickle("./similarity_content_df.pkl")
        
        

user_input = None

user_input = st.text_input(label="Please write a cocktail name.").upper()


if user_input:
  
  try:
        
    recommended_cocktails = similarity_df.loc[user_input].sort_values(ascending=False)[1:6]
    
    st.markdown("**Given Cocktail is** [{}]({})".format(user_input, df.loc[user_input]['link']))
    
    st.markdown("**Recommended Cocktails are**" )
    
    st.markdown("**[{}]({}) - :cocktail: - [{}]({}) - :tropical_drink: - [{}]({}) - :wine_glass: - [{}]({}) - :beer: - [{}]({})**".format(
            recommended_cocktails.index[0], df.loc[recommended_cocktails.index[0]]['link'], 
            recommended_cocktails.index[1], df.loc[recommended_cocktails.index[1]]['link'], 
            recommended_cocktails.index[2], df.loc[recommended_cocktails.index[2]]['link'],
            recommended_cocktails.index[3], df.loc[recommended_cocktails.index[3]]['link'],
            recommended_cocktails.index[4], df.loc[recommended_cocktails.index[4]]['link']))
    
    
    fig, ax = plt.subplots()
    ax.barh(recommended_cocktails.index, recommended_cocktails.values)
    ax.invert_yaxis()
    ax.set_title('Similarities to given cocktail')
    st.pyplot(fig)
    
  except:
  
    try:
      # input api_url directly to the post method, don't assign it to a variable. DELETE this line.
      #api_url = os.environ.get("api_url")
      response = requests.post(api_url, json = user_input)
      response_ = response.json()["body"]
      st.markdown("**Given Cocktail is** {}".format(response_))
      
    except:
      st.markdown("**The given cocktail couldn't be found in the database. Also, the embedding model is not currently in service, please use the [first version of the application](https://cocktail-recommender.herokuapp.com/).**")
      
  
  

