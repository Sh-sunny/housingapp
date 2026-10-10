from pathlib import Path

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Read data
df = pd.read_csv(Path(__file__).parent / "housing.csv")

# Title
st.title("California Housing Data (1990) by Shaxinru")

# House value filter
house_value_filter = st.slider(
    "Minimal Median House Value",
    min_value=0,
    max_value=500001,
    value=200000
)

st.subheader("See more filters in the sidebar:")

# Location filter
location_types = df["ocean_proximity"].dropna().unique().tolist()

location_filter = st.sidebar.multiselect(
    "Choose the location type",
    options=location_types,
    default=location_types
)

# Income filter
income_filter = st.sidebar.radio(
    "Choose income level",
    options=["Low", "Medium", "High"]
)

# Apply filters
df = df[df["median_house_value"] >= house_value_filter]
df = df[df["ocean_proximity"].isin(location_filter)]

if income_filter == "Low":
    df = df[df["median_income"] <= 2.5]
elif income_filter == "Medium":
    df = df[
        (df["median_income"] > 2.5)
        & (df["median_income"] < 4.5)
    ]
else:
    df = df[df["median_income"] >= 4.5]

# Map and histogram
if df.empty:
    st.info("No districts match these filters. Please adjust the filters.")
else:
    st.map(df[["latitude", "longitude"]].dropna())

    st.subheader("Distribution of Median House Value")

    fig, ax = plt.subplots()
    ax.hist(df["median_house_value"].dropna(), bins=30)
    ax.set_xlabel("Median House Value (USD)")
    ax.set_ylabel("Number of Districts")

    st.pyplot(fig)
    plt.close(fig)