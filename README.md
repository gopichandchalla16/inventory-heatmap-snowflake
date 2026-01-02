# Inventory Heatmap & Stock-Out Alerts for Essential Goods

AI for Good Hackathon – Snowflake Native App

## Problem
Hospitals, NGOs, and public distribution systems often face stock-outs or overstocking
because inventory data is scattered across systems. Stock risks are identified too late,
leading to shortages of critical supplies like medicines and food.

## Solution
This project is a Snowflake-native inventory monitoring application that:
- Visualizes stock levels using an inventory heatmap
- Detects early stock-out risks using lead-time aware logic
- Calculates days-to-stockout
- Recommends reorder quantities
- Assigns priority levels for procurement teams
- Exports actionable CSV reports for quick procurement decisions

## Key Features
- Inventory Heatmap by location and item
- Priority Stock-Out Alerts (CRITICAL / WARNING / SAFE)
- Days-to-stockout calculation
- Recommended reorder quantity
- CSV export for procurement teams
- Built entirely using Snowflake + Streamlit

## Technology Stack
- Snowflake Worksheets & SQL
- Snowflake Snowpark
- Streamlit (Snowflake Native App)
- Dynamic inventory calculations

## How to Run
This app runs directly inside Snowflake as a Streamlit app.
No external setup required.

## Impact
Helps reduce stock-outs of essential goods, minimize waste, and support
data-driven procurement decisions for healthcare and social organizations.
