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
    '''
    Takeaway & Insights
    1. **Data accuracy:**
    Inconsistencies and inaccuracies in the data. For data birth, a lot of record has date of birth Over 120 years old and the max one even have 174 years old.
    It seems that this table have long time historical data which is updated with time goes by, but without check the death situation.
    2.**Data completeness:** Some column in the dataset where contains null values.(It seems need data cleaning)
    3. **Data consistency:** Some tables have incorrect data types, for this demographic table, the DOB should be timestamp, but the checkresult shows that it contain some non-numeric value.(We need conduct some data cleaning and data type transformation before do visualization and ml)
    4. **Data timelines:** transaction dataset seems good, and it has no problems with data currency.
    5. **Data validity:** Some data points in the dataset are invalid, for example, one record in date of
    birth in the Customer Demographic sheet making them 174 years old, which is not be used, need go back to data source.
    6. **Data uniqueness:** By conduct quality checking, we could not find any duplicate data in the dataset.
        '''

    
    st.write('### Suggestions')
    st.write('- Regular Data Audits: Conducting periodic assessments to eliminate invalid data and ensure the uniqueness of the information.')
    st.write('- Clear Data Collection Guidelines: Establishing explicit protocols for collecting data.')
    st.write('- Cross-Checking Procedures: Implementing cross-referencing techniques between different data fields.')
    st.write('- Consistent Naming Conventions: Setting clear guidelines for naming data fields across the organization.')
    st.write('- Data Validation: Implementing checks to verify the accuracy of specific data types in designated columns.')
