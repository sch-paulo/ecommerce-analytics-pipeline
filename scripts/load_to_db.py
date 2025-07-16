from scripts.database import SessionLocal, engine, Base
from schema.models import CountryModel, InvoiceModel, CustomerModel, ProductModel, TransactionModel
from scripts.clean_data import clean_and_transform_data, normalize_table
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

def load_countries(session, df):
    countries = [
        CountryModel(CountryID=row['CountryID'], 
                     CountryName=row['CountryName'])
        for _, row in df.iterrows()
    ]
    session.add_all(countries)
    print(f"Added {len(df)} rows to 'countries' table (not committed yet).")

def load_customers(session, df):
    customers = [
        CustomerModel(CustomerID=row['CustomerID'], 
                      CountryID=row['CountryID'], 
                      CustomerType=row['CustomerType'])
        for _, row in df.iterrows()
    ]
    session.add_all(customers)
    print(f"Added {len(df)} rows to 'customers' table (not committed yet).")

def load_products(session, df):
    products = [
        ProductModel(StockCode=row['StockCode'], 
                     Description=row['Description'])
        for _, row in df.iterrows()
    ]
    session.add_all(products)
    print(f"Added {len(df)} rows to 'products' table (not committed yet).")

def load_invoices(session, df):
    invoices = [
        InvoiceModel(InvoiceNo=row['InvoiceNo'], 
                     InvoiceDate=row['InvoiceDate'], 
                     CustomerID=row['CustomerID'])
        for _, row in df.iterrows()
    ]
    session.add_all(invoices)
    print(f"Added {len(df)} rows to 'invoices' table (not committed yet).")

def load_transactions(session, df):
    transactions = [
        TransactionModel(InvoiceNo=row['InvoiceNo'], 
                         StockCode=row['StockCode'], 
                         LineNo=row['LineNo'], 
                         Quantity=row['Quantity'], 
                         UnitPrice=row['UnitPrice'], 
                         TotalAmount=row['TotalAmount'], 
                         TransactionType=row['TransactionType'])
        for _, row in df.iterrows()
    ]
    session.add_all(transactions)
    print(f"Added {len(df)} rows to 'transactions' table (not committed yet).")

if __name__ == "__main__":
    df = pd.read_csv('data/data.csv', encoding='latin1')
    clean_df = clean_and_transform_data(df)
    countries_table, invoices_table, customers_table, products_table, transactions_table = normalize_table(clean_df)

    Base.metadata.drop_all(bind=engine) # in case it's not the first time running
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()

    try:
        load_countries(session, countries_table)
        load_customers(session, customers_table)
        load_products(session, products_table)
        load_invoices(session, invoices_table)
        load_transactions(session, transactions_table)

        session.commit()
        print('All data sucessfully loaded into the database.')
    except Exception as e:
        session.rollback()
        print(f'Error occured: {e}')
    finally:
        session.close()