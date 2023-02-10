import streamlit as st
import pandas as pd
import os
from datetime import datetime
import seaborn as sns
from pathlib import Path
from pandas_profiling import ProfileReport
from pandas_profiling.utils.cache import cache_zipped_file
from streamlit_pandas_profiling import st_profile_report


st.markdown("# KPMG Data Analysis System")
st.sidebar.markdown("# 1111Page 1")
st.write('Data Overview')

Transactions = pd.read_excel('KPMG_VI_New_raw_data_update_final.xlsx',sheet_name= 'Transactions')
Transactions.columns = Transactions.iloc[0,:]
Transactions  = Transactions.iloc[1:,:]
Transactions.dropna(subset=['product_first_sold_date'], inplace=True)
Transactions.product_first_sold_date = Transactions.product_first_sold_date.apply(lambda x: datetime.fromtimestamp(x))
Transactions.transaction_date = Transactions.transaction_date.astype('string')
Transactions['transaction_month'] = Transactions.transaction_date.apply(lambda x: x[5:7])

profile = ProfileReport(
    Transactions, title="Profile Report of the Transaction Sheet", explorative=True
)
st_profile_report(profile)
#profile.to_file(Path("uci_bank_marketing_report.html"))

# brand count
st.write('')
Tran_counts = Transactions.groupby(['brand'],as_index=False)['list_price'].count()
Tran_counts.columns = ['brand', 'count']
# brand revenue
Tran_brand = Transactions.groupby(['brand'],as_index=False)[['list_price','standard_cost']].sum()
Tran_brand['profit'] = Tran_brand['list_price'] - Tran_brand['standard_cost']
Tran_brand = Tran_brand.merge(Tran_counts, on = ['brand'])
Tran_brand['list_price_avg'] = Tran_brand['list_price'] / Tran_brand['count']
Tran_brand['profit_avg'] = Tran_brand['profit'] / Tran_brand['count']
Tran_brand['profit_rate'] = 1- Tran_brand['standard_cost']/Tran_brand['list_price']

Tran_brand
