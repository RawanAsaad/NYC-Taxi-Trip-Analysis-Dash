# 🚖 NYC Taxi Dashboard – Interactive Data Visualization using Dash

This project is an interactive dashboard for analyzing NYC Taxi trips using Plotly Dash. Users can explore trip trends by vendor, fare amounts, pickup locations, and trip characteristics with dynamic filters and visualizations.

> ✅ Developed by Rawan Asaad Hemdan | Data Science Student | April 2025

---

## 📂 Project Overview

This app allows users to explore NYC Taxi data with the following features:

- 🔻 Filter by **Taxi Vendor**, **Fare Amount**, and **Pickup Date**
- 📊 View real-time statistics (Trip Count + Avg Fare)
- 🗺️ Interactive map of **pickup locations**
- 📈 Scatter plot of **Trip Duration vs Distance**
- 📉 Histogram of **Fare Distribution per Vendor**
- 📋 Summary table showing frequent pickup points and payment types

---

## 🛠️ Technologies Used

| Tool | Purpose |
|------|---------|
| **Python** | Core logic and data handling |
| **Pandas** | Data preprocessing |
| **Plotly Express** | Visualizations (map, histograms, scatter) |
| **Dash** | Web app interface |
| **Dash Bootstrap Components** | Responsive layout and UI |

---

## 📁 Files Included

| File | Description |
|------|-------------|
| `Taxi_Dash.py` | Full Dash app source code (Steps 1–3) |
| `ny_taxi.csv` | NYC Taxi trip data (cleaned sample) |
| `README.md` | Project overview |
| `instructions.txt` | Project instructions |

---

## 🚀 How to Run the App

1. Make sure you have Python installed.
2. Install required libraries:

```bash
pip install dash pandas plotly dash-bootstrap-components
