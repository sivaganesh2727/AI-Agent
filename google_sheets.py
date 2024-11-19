#Contains functions to authenticate with and interact with Google Sheets.
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import streamlit as st

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def authenticate_google_sheets():
    try:
        creds = Credentials.from_service_account_file('config/credentials.json', scopes=SCOPES)
        client = gspread.authorize(creds)
        return client
    except FileNotFoundError:
        st.error("`credentials.json` file not found in config directory.")
    except Exception as e:
        st.error(f"Authentication error: {e}")
    return None

def get_google_sheet_data(sheet_name):
    client = authenticate_google_sheets()
    if client:
        try:
            sheet = client.open(sheet_name).sheet1
            data = sheet.get_all_records()
            return pd.DataFrame(data)
        except gspread.exceptions.SpreadsheetNotFound:
            st.error(f"Google Sheet '{sheet_name}' not found.")
        except Exception as e:
            st.error(f"Failed to load Google Sheet: {e}")
    return None

def update_google_sheet(sheet_name, df):
    client = authenticate_google_sheets()
    if client:
        try:
            sheet = client.open(sheet_name).sheet1
            sheet.clear()
            sheet.insert_row(df.columns.tolist(), 1)
            sheet.insert_rows(df.values.tolist(), 2)
            st.success("Google Sheet updated successfully!")
        except gspread.exceptions.SpreadsheetNotFound:
            st.error(f"Google Sheet '{sheet_name}' not found.")
        except Exception as e:
            st.error(f"Failed to update Google Sheet: {e}")
