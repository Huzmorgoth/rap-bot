import streamlit as st
from TwitterBotClass import TwitterBotClass

img = 'content/background.png'
font_loc = 'content/googlefonts/Roboto/Roboto-Bold.ttf'
no_first_term = ['and', 'or', 'but', 'of', 'are', 'is', '.', ',']
bot_class = TwitterBotClass()
st.header('Rap Bot:')
user_input = st.text_input('Suggest a word for the bot to rap on:')
im, respo = bot_class.execute_code(user_input, img, font_loc, no_first_term)
generate_sum = st.button('Generate Rap')
if generate_sum:
    rap = respo
    st.subheader('Here is the rap:')
    st.write(rap)
