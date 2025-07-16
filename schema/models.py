from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    PrimaryKeyConstraint
)

from scripts.database import Base


class CountryModel(Base):
    __tablename__ = "countries"

    CountryID = Column(String, primary_key=True, index=True)
    CountryName = Column(String)


class InvoiceModel(Base):
    __tablename__ = "invoices"

    InvoiceNo = Column(String, primary_key=True, index=True)
    InvoiceDate = Column(DateTime, index=True)
    CustomerID = Column(Integer, ForeignKey("customers.CustomerID"), index=True)


class CustomerModel(Base):
    __tablename__ = "customers"

    CustomerID = Column(Integer, primary_key=True, index=True)
    CountryID = Column(String, ForeignKey("countries.CountryID"), index=True)
    CustomerType = Column(String, index=True)


class ProductModel(Base):
    __tablename__ = "products"

    StockCode = Column(String, primary_key=True, index=True)
    Description = Column(String)


class TransactionModel(Base):
    __tablename__ = "transactions"

    InvoiceNo = Column(String, ForeignKey("invoices.InvoiceNo"), index=True)
    StockCode = Column(String, ForeignKey("products.StockCode"), index=True)
    LineNo = Column(Integer, index=True)
    Quantity = Column(Integer, index=True)
    UnitPrice = Column(Float, index=True)
    TotalAmount = Column(Float, index=True)
    TransactionType = Column(String)

    __table_args__ = (PrimaryKeyConstraint("InvoiceNo", "StockCode", "LineNo"),)
