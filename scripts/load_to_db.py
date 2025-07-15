from database import engine
from schema.models import Base, CountryModel, InvoiceModel, CustomerModel, ProductModel, TransactionModel
from clean_data import clean_and_transform_data, normalize_table
import pandas as pd

def load_data_to_db(df: pd.DataFrame, table_name: str):
    try: 
        df.to_sql(table_name, con=engine, if_exists='append', index=False)
        print(f"Successfully loaded {len(df)} rows to {table_name}.")
    except Exception as e:
        print(f"Error loading data into '{table_name}': {e}")

if __name__ == "__main__":
    df = pd.read_csv('data/data.csv')
    clean_df = clean_and_transform_data(df)
    countries_table, invoices_table, customers_table, products_table, transactions_table = normalize_table(clean_df)

    Base.metadata.create_all(bind=engine)

    dict_tables = {
        'countries': countries_table, 
        'customers': customers_table, 
        'products': products_table, 
        'invoices': invoices_table, 
        'transactions': transactions_table
        }
    
    for item in dict_tables:
        print(f"Loading data into '{item}' table...")
        load_data_to_db(dict_tables[item], item)