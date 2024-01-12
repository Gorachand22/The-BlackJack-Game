# art.py
import streamlit as st

def display_logo():
    st.image("images/logo.png", width=300) 

def display_card_image(card_value):
    if card_value == 11 or card_value ==   1:
        st.image("images/A.png", width=100)
    
    else: st.image(f"images/{card_value}.png", width=100)
