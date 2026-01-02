import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session

st.set_page_config(
    page_title="Inventory Heatmap & Stock-Out Alerts",
    layout="wide"
)

st.title("Inventory Heatmap & Stock-Out Alerts for Essential Goods")
st.caption(
    "AI for Good Hackathon | Snowflake Native App"
)

session = get_active_session()

query = """
SELECT
    location,
    item,
    opening_stock,
    received,
    issued,
    closing_stock,
    lead_time_days,
    issue_date
FROM DAILY_INVENTORY
"""
df = session.sql(query).to_pandas()

df["avg_daily_issue"] = df["issued"]
df["days_to_stockout"] = (
    df["closing_stock"] / df["avg_daily_issue"]
).round(2)

df["recommended_reorder_qty"] = (
    (df["avg_daily_issue"] * df["lead_time_days"] * 1.5)
    - df["closing_stock"]
).clip(lower=0).round(0)

df["priority_level"] = df.apply(
    lambda x:
        "CRITICAL" if x["days_to_stockout"] <= x["lead_time_days"]
        else "WARNING" if x["days_to_stockout"] <= x["lead_time_days"] * 2
        else "SAFE",
    axis=1
)

st.subheader("Inventory Heatmap (Stock Levels)")

heatmap_df = df.pivot_table(
    index="location",
    columns="item",
    values="closing_stock",
    aggfunc="mean"
).fillna(0)

st.dataframe(
    heatmap_df.style.background_gradient(
        cmap="RdYlGn",
        axis=None
    ),
    use_container_width=True
)

st.subheader("Priority Stock-Out Alerts")

alerts_df = df[
    ["location", "item", "closing_stock",
     "days_to_stockout", "recommended_reorder_qty", "priority_level"]
].sort_values("days_to_stockout")

st.dataframe(alerts_df, use_container_width=True)

csv = alerts_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Procurement CSV",
    data=csv,
    file_name="priority_stock_reorder_list.csv",
    mime="text/csv"
)

st.markdown(
    """
    ---
    Built using Snowflake + Streamlit  
    Challenge: Inventory Heatmap & Stock-Out Alerts for Essential Goods
    """
)
