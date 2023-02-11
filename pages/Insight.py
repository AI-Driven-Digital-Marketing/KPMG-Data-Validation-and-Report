import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
#st.set_page_config(layout="wide")
tab1, tab2, tab3 = st.tabs(["Company&Brand Insights", 'Customer Insights',"Conclusion"])
with tab1:
    st.markdown("# Company&Brand Insights")
    st.sidebar.markdown("Company&Brand Insights")

    #Shit hole begin
    @st.cache_resource 
    def read_excelData():
        transactions = pd.read_excel('KPMG_VI_New_raw_data_update_final.xlsx',sheet_name='Transactions',header=1)
        NewCustomer = pd.read_excel('KPMG_VI_New_raw_data_update_final.xlsx',sheet_name='NewCustomerList',header=1)
        Demographic  = pd.read_excel('KPMG_VI_New_raw_data_update_final.xlsx',sheet_name='CustomerDemographic')
        CustomerAddress = pd.read_excel('KPMG_VI_New_raw_data_update_final.xlsx',sheet_name='CustomerAddress',header=1)


        Transactions = pd.read_excel('KPMG_VI_New_raw_data_update_final.xlsx',sheet_name= 'Transactions')
        Transactions.columns = Transactions.iloc[0,:]
        Transactions  = Transactions.iloc[1:,:]
        Transactions.dropna(subset=['product_first_sold_date'], inplace=True)
        Transactions.product_first_sold_date = Transactions.product_first_sold_date.apply(lambda x: datetime.fromtimestamp(x))
        Transactions.transaction_date = Transactions.transaction_date.astype('string')
        Transactions['transaction_month'] = Transactions.transaction_date.apply(lambda x: x[5:7])
        Transactions.product_id = Transactions.product_id.astype('string')
        return transactions,NewCustomer,Demographic,CustomerAddress,Transactions
    transactions,NewCustomer,Demographic,CustomerAddress,Transactions = read_excelData()
    product_summary = Transactions.groupby(['product_id'],as_index=False).aggregate(
                {'list_price':'mean',
                 'brand':'first',
                'standard_cost':'mean',
                'transaction_id':'count'})
    product_summary.sort_values(by=['list_price','standard_cost'],inplace=True,ascending=[False, True])
    product_summary = product_summary.rename({'transaction_id': 'count'}, axis=1)
    brands_name = Transactions.brand.unique()
    chosen_brand = st.selectbox(
        'Choose brand here:',
        brands_name)

    brand_fig, ax = plt.subplots(1,2,figsize=(16, 9))
    ax[0].yaxis.tick_right()
    sns.barplot(data=product_summary[product_summary.brand == chosen_brand], 
                  x="list_price", 
                  y="product_id", 
                      ax = ax[0],
                      color = 'green'
                 )
    sns.barplot(data=product_summary[product_summary.brand == chosen_brand], 
                  x="standard_cost", 
                  y="product_id", 
                      ax = ax[0],
                      color = 'orange'

                 )
    sns.barplot(data=product_summary[product_summary.brand == chosen_brand], 
                  x="count", 
                  y="product_id", 
                      ax = ax[1],
                      color = 'lightblue'
                 )
    ax[0].legend(['price','cost'],fontsize=14)
    ax[0].invert_xaxis()
    leg = ax[0].get_legend()
    leg.legendHandles[0].set_color('green')
    leg.legendHandles[1].set_color('orange')
    ax[1].legend(['Count'], fontsize = 14)
    leg1 = ax[1].get_legend()
    leg1.legendHandles[0].set_color('lightblue')
    st.pyplot(brand_fig)
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
    st.dataframe(Tran_brand.style.highlight_max(axis=0, color = 'lightblue'))


    #---------------Bing Start -----------------------------
    #Brand Selling proportion
    brand_sell = transactions.groupby('brand').count().reset_index().iloc[:,0:2]
    brand_sell.columns = ['brand','sells_num']


    labels = list(brand_sell['brand'])
    data = list(brand_sell['sells_num'])

    #Creating fig and ax
    fig, ax = plt.subplots(figsize = (10,6))

    #define Seaborn color palette to use
    colors = sns.color_palette('pastel')[0:6]

    #create pie chart
    plt.pie(data, labels = labels, colors = colors, autopct='%.0f%%')
    plt.tight_layout()

    ax.set_title('')
    st.title('Brand Selling Proportion')
    st.pyplot(fig)

    #Insight
    st.write('- Brands are cutting market evenly. Solex is taking biggest cut with number of 21%, followed by Giant Bicycles and WeareA2B.')

    #---------------Bing End -----------------------------


    #---------------Bing Online vs Brand Start -----------------------------

    #Online order
    st.write('## Brands Online Sells Analysis')
    brand_online_sold = pd.DataFrame(transactions[transactions['online_order']==1.0]['brand'].value_counts()).reset_index()
    brand_offline_sold = pd.DataFrame(transactions[transactions['online_order']==0]['brand'].value_counts()).reset_index()

    cols = ['brand','online_sold','offline_sold']
    brand_online_vs_offline = brand_online_sold.merge(brand_offline_sold,how='inner',on = 'index').set_axis(cols,axis=1)
    st.dataframe(brand_online_vs_offline)

    st.write('For all the brands, online proportion and offline are closed, which proves the importance of off line store in Bike market.')

    #---------------Bing Online vs Brand End -------------------------------



    #---------------Bing Average Profit of brands in different class Start -------------------------------

    st.write('## Average Profit of brands in different class')
    transactions['profit'] = transactions['list_price'] - transactions['standard_cost']

    profit = transactions.groupby(['brand','product_class']).mean()[['list_price','standard_cost','profit']]
    #profit = transactions.groupby(['brand']).mean()[['profit']]

    profit.reset_index(inplace=True)
    my_order = ['low','medium','high']

    profit['product_class'] = profit['product_class'].astype('category')
    profit['product_class'].cat.reorder_categories(my_order, inplace= True)
    profit.sort_values(['brand','product_class'])

    fig, ax = plt.subplots(figsize = (10,6))
    sns.barplot(data = profit, x = 'brand',y = 'profit',hue='product_class',)
    plt.tight_layout()
    st.pyplot(fig)
    st.write('OHM and Solex have amazing profit on low class products.\
    \nTrek and Weare A2B mainly focus on medium class.\
    \nGiant and Nocro are not competitive in profits compared to their opposite. With similar share of markets, company is making much less revenue.')



    #---------------Bing Average Profit of brands in different class End -------------------------------




    #---------------Bing Rich Customer Industry Start -------------------------------
with tab2:
    st.markdown("# Customers Insights")
    st.sidebar.markdown("Customers Insights")
    #st.write('## Valuable Customers Industry Source')
    Rich_Ind = Demographic[(Demographic['wealth_segment'] == 'Affluent Customer')|(Demographic['wealth_segment'] == 'High Net Worth')].groupby('job_industry_category').count().reset_index().iloc[:,0:2]

    labels = list(Rich_Ind['job_industry_category'])
    data = list(Rich_Ind['customer_id'])

    #define Seaborn color palette to use
    colors = sns.color_palette('pastel')[0:10]

    fig, ax = plt.subplots(figsize = (10,6))

    #create pie chart
    plt.pie(data, labels = labels, colors = colors, autopct='%.0f%%')
    plt.tight_layout()

    ax.set_title('')
    st.title('Valuable Customers in Industry')
    st.pyplot(fig)

    st.write('Proportion of valuable customers is having similer pattern with all-customers industry pattern.\
    \n No strong evidence indicating that customers from certain areas having higher willingness to pay.')

    #---------------Bing Rich Customer Industry End -------------------------------


    # Customer payment count
    Customer_counts = Transactions.groupby(['customer_id'],as_index=False)['list_price'].count()
    Customer_counts.columns = ['customer_id', 'bill_count']
    # Customer payment revenue
    Cutomer_brand = Transactions.groupby(['customer_id'],as_index=False)[['list_price','standard_cost']].sum()
    Cutomer_brand['profit'] = Cutomer_brand['list_price'] - Cutomer_brand['standard_cost']
    Cutomer_brand = Cutomer_brand.merge(Customer_counts, on = ['customer_id'])
    Cutomer_brand['list_price_avg'] = Cutomer_brand['list_price'] / Cutomer_brand['bill_count']
    Cutomer_brand['profit_avg'] = Cutomer_brand['profit'] / Cutomer_brand['bill_count']
    Cutomer_brand['profit_rate'] = 1- Cutomer_brand['standard_cost']/Cutomer_brand['list_price']
    Cutomer_brand = Cutomer_brand.merge(CustomerAddress[['customer_id', 'property_valuation']], 
                                        on = 'customer_id'
                                       )
    Cutomer_brand
    st.write('- Pay closely attention to customer purchase frequency as we want to keep our customers and expand their consumptions.')
    fig, ax = plt.subplots(figsize = (10,6))
    Cutomer_brand.hist(['bill_count'] , ax = ax)
    ax.set_title('')
    ax.set_xlabel('Frequency')
    ax.set_ylabel('Customer counts')
    st.title('Purchase Frequency Counts')
    st.pyplot(fig)
    st.write('- Most customers bought 5 products for this year.')
    fig1, ax1 = plt.subplots(figsize = (10,6))
    Cutomer_brand.plot.scatter(['list_price_avg'], ['profit_avg'], 
                               figsize = (16,9),
                               c = Cutomer_brand.property_valuation,
                               ax = ax1
                               )
    ax1.set_title('')
    ax1.set_xlabel('Average Purchase Price')
    ax1.set_ylabel('Average Profit')
    st.title('Price versus Profit')
    st.pyplot(fig1)
    st.write('- The deeper the color, the richer the customer. Hence, the property doesn\'t has direct impact to purchase')
with tab3:
    '''
    ### Company&Brand
    - WeareA2B has dedicated its efforts towards the medium and low classes, resulting in significant achievements.

    - WeareA2B boasts a profit rate of 66.1%, the highest among its competitors. Despite having the highest average list price, the company's products also have the lowest cost, leading to its high profitability.

    - OHM and Solex have established themselves as key players in the low-class market segment. Their product offerings and strategies are geared towards meeting the demands of consumers in this category, making them a popular choice for those seeking value for money. This strong focus on the low-class segment has proven successful for both companies, solidifying their position in this competitive market.

    - Despite having a comparable market share, Giant and Nocro have underperformed in terms of profits. The main contributor to this issue is the combination of low list prices and high costs. To improve profitability, the companies are advised to explore cost-cutting measures within their supply chains.
    ### Customers
    - The majority of WeareA2B's customer base is individuals in middle age, around 40 years old, with a balanced representation of both male and female customers.
    - The majority of  customers come from the Manufacturing, Financial Services, and Health industries, which suggests that these buyers may have a passion for mechanics or place a high value on a healthy lifestyle.
    - The car ownership rate among customers is approximately 50%, which is lower compared to the 87% rate in Australia. Bikes could be a viable alternative for cars in specific areas.
    - Upon analyzing the high-value customers, it is noted that their industries and car ownership rates are comparable. As such, these factors should not be heavily considered when developing marketing strategies.
    '''
    st.text_area('Comment & Note', 
                      'You Can Leave Your Own NOTE and Comment on Here!!')
