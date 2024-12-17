import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# Title
st.title('Unlocking Business Growth: Harness ML to Predict Customer Lifetime Value')
st.text("")

# Subtitle
st.markdown("Welcome to our Customer Lifetime Value Analysis app! With our intuitive interface and powerful data visualization capabilities, you can now easily analyze and understand the potential each customer holds for your business.")
st.markdown("""
            * Gain valuable insights into customer spending patterns and forecast their long-term value with our advanced ML algorithms. 
            * Explore the visual representation of this data, enabling you to make informed strategic decisions and optimize your business strategies.
            * Empower your team with the tools they need to maximize customer value and drive profitability. 
            """)
st.markdown("You can find the source code in my [GitHub Repository](https://github.com/opal-1996)")
st.markdown("If you are seeking additional content pertaining to data science, I invite you to peruse my personal blog - [Qin's DataHub](https://qinyang.hashnode.dev/)")


# Data overview
st.subheader("Data Overview")
df = pd.read_csv("CLV_results.csv")

col1, col2, col3, col4 = st.columns(4)
col1.metric(":blue[Unique Customers]", str(df.customer_id.nunique()))
col2.metric(":blue[Actual Purchase Value]", str(round(df["spend_90_day"].sum())))
col3.metric(":blue[Predicted Purchase Value]", str(round(df["predicted_spend_90_day"].sum())))
col4.metric(":blue[Prediction Period]", "90 Days")

# Raw data
st.markdown("")
see_data = st.expander('You can click here to see the raw data first 👉')
with see_data:
    st.dataframe(data=df.reset_index(drop=True))

# Match finder
st.subheader("Currently Selected Data")

min_purchase_actual, max_purchase_actual = st.select_slider('Try to toggle the slider below to visualize data from specific range:', sorted(df["spend_90_day"].unique()), value=(0, 593.88))
def data_by_actual_purchase(df):
    return df[(df["spend_90_day"] >= min_purchase_actual) & (df["spend_90_day"] <= max_purchase_actual)]
filtered_df_by_actual_purchase = data_by_actual_purchase(df)

import plotly.express as px
fig = px.scatter(filtered_df_by_actual_purchase, x="spend_90_day", y="predicted_spend_90_day", color="pred_spend_90_day_prob", size="spend_90_day",
                 hover_name="customer_id", log_x=True, size_max=60)
st.plotly_chart(fig, use_container_width=True)

row3_spacer1, row3_1, row3_spacer2 = st.columns((1.3, 4, 1))
with row3_1:
    col1, col2, col3 = st.columns(3)
    col1.metric(":blue[Unique Customers]", str(filtered_df_by_actual_purchase.customer_id.nunique()), "Under Selected Range")
    col2.metric(":blue[Actual Purchase Value]", str(round(filtered_df_by_actual_purchase["spend_90_day"].sum())), "Under Selected Range")
    col3.metric(":blue[Predicted Purchase Value]", str(round(filtered_df_by_actual_purchase["predicted_spend_90_day"].sum())), "Under Selected Range")

st.download_button(
    label="Download selected data as CSV",
    data=filtered_df_by_actual_purchase.to_csv().encode('utf-8'),
    file_name='data.csv',
    mime='text/csv',
)

st.text("")
st.text("")
st.text("")
st.markdown("Made by Qin Yang.")
