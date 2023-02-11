import streamlit as st
import pandas as pd
import numpy as np

st.markdown("# KPMG Data Analysis Platform 🎉")
st.sidebar.markdown("Contact & Controller🎉")
import streamlit as st



# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

st.sidebar.text_area('Contact Infomation', 
                      'Please leave your contact information on here! You would get compelete report!!')

# add mugshot to sidebar
mugshot = st.sidebar.camera_input(
  '## Create your mugshot for your own Report'
)
# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)
#####################Main page###

tab1, tab2, tab3 = st.tabs(["Why us?" , "Solutions & Anticipations", "About this Platform"])

with tab1:
    col1, col2 = st.columns(2,gap = "medium")
    with col1:
       st.image('src/IMG_5301 2.JPG')

    with col2:
        '''
- 1. Deep understanding your data profile: 
    KYC,KYB and Know your data!
- 2. Check your data Quality:
    Ensure your data quality from 6 dimensions and not be deceived!
- 3. Powerful Analytics tools:
   Analyze your data set in multiple dimensions and give you the most comprehensive advice！
- 4. Intelligent Suggestion: 
    Intelligently provide valuable insights for your preprocessing procedure.
- 5. Visualization and Dashboard!
    Quick, colorful, informative dashboard to let you aim your target users.

        '''
    
with tab2:
    
    col1, col2 = st.columns(2)
    with col1:
       st.image("https://static.streamlit.io/examples/cat.jpg")

    with col2:
       st.title('Problems and Solutions')
       '''
        我们很牛逼
        1.提供
        2.提供b
        3.提供
        '''

with tab3:
    
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://static.streamlit.io/examples/cat.jpg")

    with col2:
        '''
        Your personal Report is here
        '''
        st.image(mugshot, width=150)





# @st.experimental_memo
# def load_data(url):
#     df = pd.read_csv(url)
#     return df

# df = load_data("https://github.com/plotly/datasets/raw/master/uber-rides-data1.csv")
# st.dataframe(df)

# st.button("Rerun")
