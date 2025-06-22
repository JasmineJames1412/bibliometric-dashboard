import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set the page title
st.title("Bibliometric Analysis Dashboard")

# Load the Heart Disease Dataset (now as CSV)
@st.cache_data
def load_heart_data():
    try:
        # Read as CSV instead of Excel
        heart_df = pd.read_csv("heart_disease_dataset.csv")  # Updated file name
        required_cols = ["Title", "Authors", "Year", "Publisher", "Citations", "Link"]
        for col in required_cols:
            if col not in heart_df.columns:
                heart_df[col] = "N/A"
        return heart_df
    except FileNotFoundError:
        st.error("Error: 'heart disease dataset.csv' not found. Please place the file in the same folder.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading 'heart disease dataset.csv': {e}")
        return pd.DataFrame()

# Load the Author Details Dataset
@st.cache_data
def load_author_data():
    try:
        author_df = pd.read_excel("author_details_output.xlsx", engine='openpyxl')
        if 'Citations Per Year' in author_df.columns:
            author_df['Citations Per Year'] = author_df['Citations Per Year'].apply(
                lambda x: eval(x) if isinstance(x, str) and '{' in x else x
            )
            if not isinstance(author_df['Citations Per Year'].iloc[0], dict):
                st.warning("Citations Per Year data format may not be correct. Please check the Excel file.")
        required_cols = ["Name", "Affiliation", "Interests", "Cited by", "H-Index", "i10-Index", "Citations Per Year"]
        for col in required_cols:
            if col not in author_df.columns:
                author_df[col] = "N/A"
        return author_df
    except FileNotFoundError:
        st.error("Error: 'author_details_output.xlsx' not found. Please place the file in the same folder.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading 'author_details_output.xlsx': {e}")
        return pd.DataFrame()

# Load the data
heart_data = load_heart_data()
author_data = load_author_data()

# Topic-wise Bibliometric Analysis
st.header("Topic-wise Bibliometric Analysis")

if not heart_data.empty:
    year_range = st.slider("Select Year Range", min_value=int(heart_data["Year"].min()), 
                           max_value=int(heart_data["Year"].max()), 
                           value=(int(heart_data["Year"].min()), int(heart_data["Year"].max())))
    filtered_heart_data = heart_data[(heart_data["Year"] >= year_range[0]) & (heart_data["Year"] <= year_range[1])]

    st.subheader("Articles Table")
    st.write(filtered_heart_data)

    st.subheader("Articles Published Per Year")
    articles_per_year = filtered_heart_data["Year"].value_counts().sort_index()
    plt.figure(figsize=(10, 5))
    plt.bar(articles_per_year.index, articles_per_year.values)
    plt.xlabel("Year")
    plt.ylabel("Number of Articles")
    plt.title("Articles Published Per Year")
    st.pyplot(plt)

    st.subheader("Average Citations Per Year")
    avg_citations_per_year = filtered_heart_data.groupby("Year")["Citations"].mean()
    plt.figure(figsize=(10, 5))
    plt.plot(avg_citations_per_year.index, avg_citations_per_year.values, marker='o')
    plt.xlabel("Year")
    plt.ylabel("Average Citations")
    plt.title("Average Citations Per Year")
    st.pyplot(plt)

else:
    st.write("No heart disease data available to display.")

# Author-wise Bibliometric Analysis
st.header("Author-wise Bibliometric Analysis")

if not author_data.empty:
    st.subheader("Author Details")
    for index, row in author_data.iterrows():
        st.write(f"**Name:** {row['Name']}")
        st.write(f"Affiliation: {row['Affiliation']}")
        st.write(f"Interests: {row['Interests']}")
        st.write(f"Cited by: {row['Cited by']}")
        st.write(f"H-Index: {row['H-Index']}")
        st.write(f"i10-Index: {row['i10-Index']}")

        st.subheader("Citations Per Year")
        if isinstance(row['Citations Per Year'], dict):
            years = list(row['Citations Per Year'].keys())
            citations = list(row['Citations Per Year'].values())
            plt.figure(figsize=(10, 5))
            plt.plot(years, citations, marker='o')
            plt.xlabel("Year")
            plt.ylabel("Citations")
            plt.title(f"Citations Per Year for {row['Name']}")
            st.pyplot(plt)
        else:
            st.write(f"Citations Per Year data for {row['Name']} is not in the expected format. Check the Excel file.")

else:
    st.write("No author data available to display.")