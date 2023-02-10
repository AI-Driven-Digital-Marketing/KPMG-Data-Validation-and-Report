import streamlit as st
import pandas as pd
import os
from datetime import datetime
import seaborn as sns
from pathlib import Path
from pandas_profiling import ProfileReport
from pandas_profiling.utils.cache import cache_zipped_file
from streamlit_pandas_profiling import st_profile_report


st.markdown("# Data Quality Check")
st.sidebar.markdown("# Data Quality Check")
tab1, tab2, tab3, tab4 = st.tabs(["Transaction", "New Customer", "Customer Demo", 'CustomerAddress'])

@st.cache_resource 
def profiling_transaction(sheet):
    df = pd.read_excel('KPMG_VI_New_raw_data_update_final.xlsx',sheet_name= sheet)
    if sheet != 'CustomerDemographic':
        df.columns = df.iloc[0,:]
        df  = df.iloc[1:,:]
        df = df.loc[:,~df.columns.isna()]



    profile = ProfileReport(
        df, title="Profile Report of the Transaction Sheet", explorative=True
    )
    return profile

with tab1:
    profile = profiling_transaction('Transactions')
    st_profile_report(profile)

    
with tab2:
    profile = profiling_transaction('NewCustomerList')
    st_profile_report(profile)    
    
with tab3:
    profile = profiling_transaction('CustomerDemographic')
    st_profile_report(profile) 
    
with tab4:
    profile = profiling_transaction('CustomerAddress')
    st_profile_report(profile) 
