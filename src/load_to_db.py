import sys
import os
from src.database import SessionLocal, engine, Base
from schema.models import (
    CountryModel,
    InvoiceModel,
    CustomerModel,
    ProductModel,
    TransactionModel,
)
from src.clean_data import clean_and_transform_data, normalize_table
import pandas as pd
import warnings

warnings.filterwarnings("ignore")


def load_countries(session, df):
    """
    Loads country data into the database session.

    Parameters
    ----------
    session: sqlalchemy.orm.Session
        The SQLAlchemy session to which the data will be added.
    df: pandas.DataFrame
        DataFrame containing 'CountryID' and 'CountryName' columns.
    """
    countries = [
        CountryModel(country_id=row["CountryID"], country_name=row["CountryName"])
        for _, row in df.iterrows()
    ]
    session.add_all(countries)
    print(f"Added {len(df)} rows to 'countries' table (not committed yet).")


def load_customers(session, df):
    """
    Loads customer data into the database session.

    Parameters
    ----------
    session: sqlalchemy.orm.Session
        The SQLAlchemy session to which the data will be added.
    df: pandas.DataFrame
        DataFrame containing 'CustomerID', 'CountryID', and 'CustomerType'.
    """
    customers = [
        CustomerModel(
            customer_id=row["CustomerID"],
            country_id=row["CountryID"],
            customer_type=row["CustomerType"],
        )
        for _, row in df.iterrows()
    ]
    session.add_all(customers)
    print(f"Added {len(df)} rows to 'customers' table (not committed yet).")


def load_products(session, df):
    """
    Loads product data into the database session.

    Parameters
    ----------
    session: sqlalchemy.orm.Session
        The SQLAlchemy session to which the data will be added.
    df: pandas.DataFrame
        DataFrame containing 'StockCode' and 'Description'.
    """
    products = [
        ProductModel(stock_code=row["StockCode"], description=row["Description"])
        for _, row in df.iterrows()
    ]
    session.add_all(products)
    print(f"Added {len(df)} rows to 'products' table (not committed yet).")


def load_invoices(session, df):
    """
    Loads invoice data into the database session.

    Parameters
    ----------
    session: sqlalchemy.orm.Session
        The SQLAlchemy session to which the data will be added.
    df: pandas.DataFrame
        DataFrame containing 'InvoiceNo', 'InvoiceDate', and 'CustomerID'.
    """
    invoices = [
        InvoiceModel(
            invoice_no=row["InvoiceNo"],
            invoice_date=row["InvoiceDate"],
            customer_id=row["CustomerID"],
        )
        for _, row in df.iterrows()
    ]
    session.add_all(invoices)
    print(f"Added {len(df)} rows to 'invoices' table (not committed yet).")


def load_transactions(session, df):
    """
    Loads transaction data into the database session.

    Parameters
    ----------
    session: sqlalchemy.orm.Session
        The SQLAlchemy session to which the data will be added.
    df: pandas.DataFrame
        DataFrame with transaction data including:
        'InvoiceNo', 'StockCode', 'LineNo', 'Quantity', 'UnitPrice',
        'TotalAmount', and 'TransactionType'.
    """
    transactions = [
        TransactionModel(
            invoice_no=row["InvoiceNo"],
            stock_code=row["StockCode"],
            line_no=row["LineNo"],
            quantity=row["Quantity"],
            unit_price=row["UnitPrice"],
            total_amount=row["TotalAmount"],
            transaction_type=row["TransactionType"],
        )
        for _, row in df.iterrows()
    ]
    session.add_all(transactions)
    print(f"Added {len(df)} rows to 'transactions' table (not committed yet).")


if __name__ == "__main__":

    data_file = "data/data.csv"
    if not os.path.exists(data_file):
        print(f"Data file {data_file} not found!")
        sys.exit(1)

    try:
        print("Loading and processing data...")
        df = pd.read_csv(data_file, encoding="latin1")
        clean_df = clean_and_transform_data(df)
        (
            countries_table,
            invoices_table,
            customers_table,
            products_table,
            transactions_table,
        ) = normalize_table(clean_df)

        Base.metadata.drop_all(bind=engine)  # in case it's not the first time running
        Base.metadata.create_all(bind=engine)

        session = SessionLocal()

        print("Loading data into database...")
        load_countries(session, countries_table)
        load_customers(session, customers_table)
        load_products(session, products_table)
        load_invoices(session, invoices_table)
        load_transactions(session, transactions_table)

        session.commit()
        print("All data successfully loaded into the database.")

    except Exception as e:
        print(f"Error occurred: {e}")
        session.rollback()
        sys.exit(1)
    finally:
        session.close()
