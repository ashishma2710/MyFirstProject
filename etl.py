import requests # type: ignore
import pandas as pd # type: ignore 
from sqlalchemy import create_engine # type: ignore

# MySQL connection
username = "ashish"
password = "Maurya271097"
host = "localhost"
port = 3306
database = "sales_project"

def extract()-> dict:
    response = requests.get(
        'https://api.restcountries.com/countries/v5?response_fields=names.common&response_fields=population&limit=100&offset=200',
  headers={'Authorization': 'Bearer rc_live_fbdf5f3b470549c4b07815ac72fa0f55'}
  )
    print("Status Code:", response.status_code)
    data=response.json()
    return data

def transform(data: dict) -> pd.DataFrame:
    countries = data['data']['objects']

    rows = []

    for country in countries:
        rows.append({
            'country': country['names']['common'],
            'population': country['population']
        })

    df = pd.DataFrame(rows)

    print(df)
    return df

def load(df: pd.DataFrame)-> None:
    engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}")
    df.to_sql('countries', con=engine, if_exists='append', index=False)
    print("Data loaded into the database successfully.")

data=extract()
data1=transform(data)
data2=load(data1)
