import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
st.markdown("# Page 2 ❄️")
st.sidebar.markdown("Page 2")


st.markdown("1. **Data accuracy:**
Inconsistencies and inaccuracies in the data. For data birth, a lot of record has date of birth Over 120 years old and the max one even have 174 years old.
It seems that this table have long time historical data which is updated with time goes by, but without check the death situation.
2.**Data completeness:** Some column in the dataset where contains null values.(It seems need data cleaning)
3. **Data consistency:** Some tables have incorrect data types, for this demographic table, the DOB should be timestamp, but the checkresult shows that it contain some non-numeric value.(We need conduct some data cleaning and data type transformation before do visualization and ml)
4. **Data timelines:** transaction dataset seems good, and it has no problems with data currency.
5. **Data validity:** Some data points in the dataset are invalid, for example, one record in date of
birth in the Customer Demographic sheet making them 174 years old, which is not be used, need go back to data source.
6. **Data uniqueness:** By conduct quality checking, we could not find any duplicate data in the dataset.")

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
Cutomer_brand.hist(['bill_count'] , ax =ax)
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
import streamlit as st

st.text_area(
  'Takeaway：',
  'This is what I really wanted to say'
)

