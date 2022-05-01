import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit


st.set_page_config(page_title="Bike Sales Dashboard", page_icon=":bar_chart:", layout="wide")

# ---- READ CSV ----
@st.cache
def get_data():
    return pd.read_csv('bike_sales_data.csv', parse_dates=['Date'])

df = get_data()
df = df.iloc[:,1:]


# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")

country = st.sidebar.multiselect(
    "Select the Country:",
    options=df["Country"].unique(),
    default=df["Country"].unique()
)
gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Customer_Gender"].unique(),
    default=df["Customer_Gender"].unique()
)
year = st.sidebar.slider(
     'Select a range of Year:',
     2011, 2016, (2014, 2016))
st.sidebar.write('Values:', year)


df_selection = df.query(
    "Country == @country & Customer_Gender == @gender & @year[0] <= Year <= @year[1] "
)

#---- Plotly things ----

sales_per_year = df_selection.groupby(by='Year')['Profit'].sum()
sales_per_year = pd.DataFrame({'Year':sales_per_year.index, 'Total Profit':sales_per_year.values})

bikes = df_selection['Product_Category'].value_counts()
bikes = pd.DataFrame({'Product Category':bikes.index, 'Count':bikes.values})


subbikes = df_selection.groupby(by='Product_Category')['Sub_Category'].value_counts().to_frame(name='Count').reset_index()

#subbikes = pd.DataFrame({'Sub Category':subbikes.index, 'Count':subbikes.values})

year_fig = px.line(sales_per_year, 
    x='Year', 
    y='Total Profit', 
    title='Sales per Year', 
    template="plotly_white")
    
year_fig.update_traces(line=dict(color="#e694ff", width=3))

fig = px.pie(bikes, 
    values='Count', 
    names='Product Category', 
    title='Product Category', 
    color='Product Category', 
    template="plotly_white")

fig2 = px.bar(subbikes, y='Count', x='Product_Category', color='Sub_Category', title='Sales by Categories', template="plotly_white")






st.title(":bar_chart: Bike Sales Dashboard")
st.markdown("##")


# ---- MAIN ----
st.image('https://images.unsplash.com/photo-1505705694340-019e1e335916?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1332&q=80', 
    use_column_width=True)

st.plotly_chart(year_fig, use_container_width=True)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig, use_container_width=True)
right_column.plotly_chart(fig2, use_container_width=True)

