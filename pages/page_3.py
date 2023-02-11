import streamlit as st
import pandas as pd
import numpy as np

st.markdown("#  3 🎉")
st.sidebar.markdown("Contact & Controller🎉")
import streamlit as st

st.sidebar.camera_input(
  '##wCreate your mugshot for your own Report'
)

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

st.sidebar.text_area('Contact Infomation', 
                      'Please leave your contact information on here! You would get compelete report!!')

# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)


@st.experimental_memo
def load_data(url):
    df = pd.read_csv(url)
    return df

df = load_data("https://github.com/plotly/datasets/raw/master/uber-rides-data1.csv")
st.dataframe(df)

st.button("Rerun")
