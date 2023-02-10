import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
st.markdown("# Page 2 ❄️")
st.sidebar.markdown("Page 2")

Transactions = pd.read_excel('KPMG_VI_New_raw_data_update_final.xlsx',sheet_name= 'Transactions')
Transactions.columns = Transactions.iloc[0,:]
Transactions  = Transactions.iloc[1:,:]
Transactions.dropna(subset=['product_first_sold_date'], inplace=True)
Transactions.product_first_sold_date = Transactions.product_first_sold_date.apply(lambda x: datetime.fromtimestamp(x))
Transactions.transaction_date = Transactions.transaction_date.astype('string')
Transactions['transaction_month'] = Transactions.transaction_date.apply(lambda x: x[5:7])
# brand count
st.write('- Each brand has different marketing strategy and target populations, their sales statistics are hence different.')
st.write('- Understanding these difference is important when organizing any business activities.')
st.write('### Suggestions')
st.write('- Regular Data Audits: Conducting periodic assessments to eliminate invalid data and ensure the uniqueness of the information.
- Clear Data Collection Guidelines: Establishing explicit protocols for collecting data.
- Cross-Checking Procedures: Implementing cross-referencing techniques between different data fields.
- Consistent Naming Conventions: Setting clear guidelines for naming data fields across the organization.
- Data Validation: Implementing checks to verify the accuracy of specific data types in designated columns.')


Tran_counts = Transactions.groupby(['brand'],as_index=False)['list_price'].count()
Tran_counts.columns = ['brand', 'count']
# brand revenue
Tran_brand = Transactions.groupby(['brand'],as_index=False)[['list_price','standard_cost']].sum()
Tran_brand['profit'] = Tran_brand['list_price'] - Tran_brand['standard_cost']
Tran_brand = Tran_brand.merge(Tran_counts, on = ['brand'])
Tran_brand['list_price_avg'] = Tran_brand['list_price'] / Tran_brand['count']
Tran_brand['profit_avg'] = Tran_brand['profit'] / Tran_brand['count']
Tran_brand['profit_rate'] = 1- Tran_brand['standard_cost']/Tran_brand['list_price']
st.dataframe(Tran_brand.style.highlight_max(axis=0, color = 'lightblue'))

# Customer payment count
CustomerAddress = pd.read_excel('KPMG_VI_New_raw_data_update_final.xlsx',sheet_name= 'CustomerAddress')
CustomerAddress.columns = CustomerAddress.iloc[0,:]
CustomerAddress  = CustomerAddress.iloc[1:,:]
Customer_counts = Transactions.groupby(['customer_id'],as_index=False)['list_price'].count()
Customer_counts.columns = ['customer_id', 'bill_count']
# Customer payment revenue
Cutomer_brand = Transactions.groupby(['customer_id'],as_index=False)[['list_price','standard_cost']].sum()
Cutomer_brand['profit'] = Cutomer_brand['list_price'] - Cutomer_brand['standard_cost']
Cutomer_brand = Cutomer_brand.merge(Customer_counts, on = ['customer_id'])
Cutomer_brand['list_price_avg'] = Cutomer_brand['list_price'] / Cutomer_brand['bill_count']
Cutomer_brand['profit_avg'] = Cutomer_brand['profit'] / Cutomer_brand['bill_count']
Cutomer_brand['profit_rate'] = 1- Cutomer_brand['standard_cost']/Cutomer_brand['list_price']
Cutomer_brand = Cutomer_brand.merge(CustomerAddress[['customer_id', 'property_valuation']], on = 'customer_id')
st.write('- Pay closely attention to customer purchase frequency as we want to keep our customers and expand their consumptions.')
fig, ax = plt.subplots(figsize = (10,6))
Cutomer_brand.hist(['bill_count'] , ax = ax)
ax.set_title('')
st.title('Purchase Frequency Counts')
st.pyplot(fig)

fig1, ax1 = plt.subplots(figsize = (10,6))
Cutomer_brand.plot.scatter(['list_price_avg'], ['profit_avg'], 
                           figsize = (16,9),
                           c = Cutomer_brand.property_valuation,
                           ax = ax1
                           )
ax1.set_title('')
st.title('Price versus Profit')
st.pyplot(fig1)
