import pandas as pd
from config.country_map import COUNTRY_MAP
import warnings

warnings.filterwarnings("ignore")


def clean_and_transform_data(df: pd.DataFrame):
    """
    Cleans and enriches raw transactional data for normalization.

    Steps performed:
    - Removes duplicate rows.
    - Converts date columns.
    - Fills missing customer IDs and descriptions.
    - Infers customer and transaction types.
    - Computes total transaction amount.
    - Maps countries to internal IDs.

    Parameters
    ----------
    df: pandas.DataFrame
        Raw transactional data.

    Returns
    -------
    pandas.DataFrame
        Transformed and cleaned DataFrame ready for normalization.
    """
    df = df.drop_duplicates()

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["CustomerID"] = df["CustomerID"].fillna(0).astype(int)

    description_mapping = (
        df.dropna(subset=["Description"])
        .drop_duplicates("StockCode")
        .set_index("StockCode")["Description"]
    )
    df["Description"] = df["Description"].fillna(
        df["StockCode"].map(description_mapping)
    )
    df["Description"] = df["Description"].fillna("UNKNOWN PRODUCT")

    df["CustomerType"] = "Client"
    df.loc[df["CustomerID"] == 0, "CustomerType"] = "Guest"

    df["TransactionType"] = "Sale"
    df.loc[df["Quantity"] < 0, "TransactionType"] = "Return/Cancellation"
    df.loc[df["UnitPrice"] < 0, "TransactionType"] = "Adjustment"

    df["TotalAmount"] = df["Quantity"] * df["UnitPrice"]
    df["CountryID"] = df["Country"].map(COUNTRY_MAP)

    return df


def normalize_table(df: pd.DataFrame):
    """
    Normalizes a transactional DataFrame into separate dimension and fact tables.

    Parameters
    ----------
    df: pandas.DataFrame
        Cleaned transactional DataFrame.

    Returns
    -------
    tuple of pandas.DataFrame
        A tuple containing:
        - countries_table (CountryID, CountryName)
        - invoices_table (InvoiceNo, InvoiceDate, CustomerID)
        - customers_table (CustomerID, CountryID, CustomerType)
        - products_table (StockCode, Description)
        - transactions_table (InvoiceNo, StockCode, Quantity, UnitPrice,
          TotalAmount, TransactionType, LineNo)
    """
    countries_table = (
        df[["CountryID", "Country"]].drop_duplicates().reset_index(drop=True)
    )
    countries_table = (
        df[["CountryID", "Country"]].groupby("CountryID").first().reset_index()
    )
    countries_table = countries_table.rename(columns={"Country": "CountryName"})

    invoices_table = df[["InvoiceNo", "InvoiceDate", "CustomerID"]]
    invoices_table = invoices_table.groupby("InvoiceNo").first().reset_index()

    customers_table = df[["CustomerID", "CountryID", "CustomerType"]]
    customers_table = customers_table.groupby("CustomerID").first().reset_index()

    products_table = df[["StockCode", "Description"]]
    products_table = (
        products_table.groupby("StockCode")["Description"]
        .apply(lambda x: x.mode()[0])
        .reset_index()
    )

    transactions_table = df[
        [
            "InvoiceNo",
            "StockCode",
            "Quantity",
            "UnitPrice",
            "TotalAmount",
            "TransactionType",
        ]
    ]
    transactions_table["LineNo"] = (
        transactions_table.groupby("InvoiceNo").cumcount() + 1
    )

    return (
        countries_table,
        invoices_table,
        customers_table,
        products_table,
        transactions_table,
    )


if __name__ == "__main__":
    df = pd.read_csv("data/data.csv", encoding="latin1")
    df = clean_and_transform_data(df)
    (
        countries_table,
        invoices_table,
        customers_table,
        products_table,
        transactions_table,
    ) = normalize_table(df)
    print(
        countries_table,
        invoices_table,
        customers_table,
        products_table,
        transactions_table,
    )
