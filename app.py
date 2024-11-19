import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import openai
import requests  # Import requests for ScraperAPI calls

# Set API keys
SCRAPERAPI_KEY = "df2cc6999b7e073dfc974034d1658c04"
OPENAI_API_KEY = "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"

# Authenticate OpenAI API
openai.api_key = OPENAI_API_KEY

# Scopes for Google Sheets API
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Authenticate with Google Sheets using service account credentials
def authenticate_google_sheets():
    try:
        # Load credentials.json file
        creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
        client = gspread.authorize(creds)
        return client
    except FileNotFoundError:
        st.error("credentials.json file not found. Please upload it to the working directory.")
    except Exception as e:
        st.error(f"Authentication error: {e}")
    return None

# Fetch data from a Google Sheet
def get_google_sheet_data(sheet_name):
    client = authenticate_google_sheets()
    if client:
        try:
            sheet = client.open(sheet_name).sheet1  # Open the first worksheet
            data = sheet.get_all_records()  # Fetch all records
            return pd.DataFrame(data)  # Convert to DataFrame
        except gspread.exceptions.SpreadsheetNotFound:
            st.error(f"Google Sheet '{sheet_name}' not found. Ensure the Service Account has access.")
        except Exception as e:
            st.error(f"Failed to load Google Sheet: {e}")
    return None

# Update Google Sheet with DataFrame
def update_google_sheet(sheet_name, df):
    client = authenticate_google_sheets()
    if client:
        try:
            sheet = client.open(sheet_name).sheet1
            sheet.clear()  # Clear existing data
            sheet.insert_row(df.columns.tolist(), 1)  # Add headers
            sheet.insert_rows(df.values.tolist(), 2)  # Add data rows
            st.success("Google Sheet updated successfully!")
        except gspread.exceptions.SpreadsheetNotFound:
            st.error(f"Google Sheet '{sheet_name}' not found. Ensure the Service Account has access.")
        except Exception as e:
            st.error(f"Failed to update Google Sheet: {e}")

# Function to perform web search using ScraperAPI
def perform_scraperapi_search(query):
    url = f"http://api.scraperapi.com"
    params = {
        "api_key": SCRAPERAPI_KEY,
        "url": f"https://www.google.com/search?q={query}"
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.text  # You can parse the response if needed
        else:
            st.warning(f"ScraperAPI returned status code {response.status_code}")
            return None
    except Exception as e:
        st.warning(f"Error with ScraperAPI: {e}")
        return None

# Main Application
def main():
    st.title("AI Web Search Agent")

    # Upload CSV or connect to Google Sheet
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
    sheet_name = st.text_input("Enter Google Sheet Name")

    df = None

    # Load CSV file if uploaded
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("CSV Data Preview:")
        st.write(df.head())

    # Load Google Sheet if name provided
    if sheet_name:
        df = get_google_sheet_data(sheet_name)
        if df is not None:
            st.write("Google Sheet Data Preview:")
            st.write(df.head())

    # Ensure data is loaded
    if df is None:
        st.info("Please upload a CSV file or provide a Google Sheet name.")
        return

    # Query Input for Search
    selected_column = st.selectbox("Select a column for entities", df.columns)
    query_template = st.text_input("Enter query template (use {entity})", "Get information about {entity}")

    if selected_column and query_template:
        # Display example query
        example_query = query_template.format(entity=df[selected_column].iloc[0])
        st.write(f"Example query: {example_query}")

        # Perform web search for each entity
        search_results = {}
        for entity in df[selected_column]:
            query = query_template.format(entity=entity)
            result = perform_scraperapi_search(query)
            if result:
                search_results[entity] = result
            else:
                search_results[entity] = "Error fetching data"

        # Display extracted information
        extracted_info = {entity: search_results[entity] for entity in search_results}
        st.write("Extracted Information:")
        st.write(pd.DataFrame(extracted_info.items(), columns=["Entity", "Extracted Data"]))

        # Allow Google Sheet updates
        if st.checkbox("Update Google Sheet with Results"):
            update_google_sheet(sheet_name, pd.DataFrame(extracted_info.items(), columns=["Entity", "Extracted Data"]))

if __name__ == "__main__":
    main()

