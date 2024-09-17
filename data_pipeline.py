import pandas as pd
import requests
from sqlalchemy import create_engine
from models import DataModel
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('API_KEY')
DATABASE_URI = os.getenv('DATABASE_URI')

def extract_data():
    # Example: Fetch data from an API
    response = requests.get(f'https://api.example.com/data?api_key={API_KEY}')
    api_data = response.json()

    # Read data from a CSV file
    csv_data = pd.read_csv('data.csv')

    # Read data from a SQL database
    engine = create_engine(DATABASE_URI)
    sql_data = pd.read_sql('SELECT * FROM table_name', engine)

    return api_data, csv_data, sql_data

def transform_data(api_data, csv_data, sql_data):
    # Convert API data to DataFrame
    df_api = pd.DataFrame(api_data)

    # Data cleaning and transformation
    df_api['date'] = pd.to_datetime(df_api['date'])
    csv_data.dropna(inplace=True)
    sql_data.rename(columns={'old_name': 'new_name'}, inplace=True)

    # Data aggregation
    df = pd.concat([df_api, csv_data, sql_data], ignore_index=True)
    df_grouped = df.groupby('category').sum()

    return df_grouped

def load_data(df):
    engine = create_engine(DATABASE_URI)
    df.to_sql('processed_data', engine, if_exists='replace')

if __name__ == '__main__':
    api_data, csv_data, sql_data = extract_data()
    processed_data = transform_data(api_data, csv_data, sql_data)
    load_data(processed_data)
    print("Data pipeline executed successfully.")
