import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session

# ---------------------------------
# Page config
# ---------------------------------
st.set_page_config(
    page_title="Inventory Heatmap & Stock-Out Alerts",
    layout="wide"
)

st.title("Inventory Heatmap & Stock-Out Alerts for Essential Goods")
st.caption("AI for Good | Snowflake Native App")
st.caption("Lower values indicate higher stock-out risk")

# ---------------------------------
# Snowflake session
# ---------------------------------
session = get_active_session()

# ---------------------------------
# Load inventory data
# ---------------------------------
query = """
SELECT
    location,
    item,
    opening_stock,
    received,
    issued,
    closing_stock,
    lead_time_days
FROM DAILY_INVENTORY
"""
df = session.sql(query).to_pandas()

# ---------------------------------
# Derived metrics
# ---------------------------------
df["avg_daily_issue"] = df["ISSUED"]

df["days_to_stockout"] = (
    df["CLOSING_STOCK"] / df["avg_daily_issue"]
).round(2)

df["recommended_reorder_qty"] = (
    (df["avg_daily_issue"] * df["LEAD_TIME_DAYS"] * 1.5)
    - df["CLOSING_STOCK"]
).clip(lower=0).round(0)

df["priority_level"] = df.apply(
    lambda x:
        "CRITICAL" if x["days_to_stockout"] <= x["LEAD_TIME_DAYS"]
        else "WARNING" if x["days_to_stockout"] <= x["LEAD_TIME_DAYS"] * 2
        else "SAFE",
    axis=1
)

# ---------------------------------
# Inventory Heatmap (Snowflake-safe)
# ---------------------------------
st.subheader("Inventory Heatmap (Stock Levels)")

heatmap_df = df.pivot_table(
    index="LOCATION",
    columns="ITEM",
    values="CLOSING_STOCK",
    aggfunc="mean"
).fillna(0)

st.dataframe(
    heatmap_df,
    use_container_width=True
)

st.caption("Higher numbers = healthier stock | Lower numbers = higher risk")

# ---------------------------------
# Priority Stock-Out Alerts
# ---------------------------------
st.subheader("Priority Stock-Out Alerts")

alerts_df = df[
    [
        "LOCATION",
        "ITEM",
        "CLOSING_STOCK",
        "days_to_stockout",
        "recommended_reorder_qty",
        "priority_level"
    ]
].sort_values("days_to_stockout")

st.dataframe(alerts_df, use_container_width=True)

# ---------------------------------
# Export CSV
# ---------------------------------
st.subheader("Export Actionable Reorder List")

csv = alerts_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Procurement CSV",
    data=csv,
    file_name="priority_stock_reorder_list.csv",
    mime="text/csv"
)

# ---------------------------------
# Footer
# ---------------------------------
st.markdown(
    """
    ---
    **Built using Snowflake + Streamlit**  
    Challenge: Inventory Heatmap & Stock-Out Alerts for Essential Goods  
    Purpose: Reduce stock-outs and waste for hospitals, NGOs, and public systems
    """
)
