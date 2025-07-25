from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    PrimaryKeyConstraint,
)

from src.database import Base


class CountryModel(Base):
    __tablename__ = "countries"

    country_id = Column(String, primary_key=True, index=True)
    country_name = Column(String)


class InvoiceModel(Base):
    __tablename__ = "invoices"

    invoice_no = Column(String, primary_key=True, index=True)
    invoice_date = Column(DateTime, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), index=True)


class CustomerModel(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    country_id = Column(String, ForeignKey("countries.country_id"), index=True)
    customer_type = Column(String, index=True)


class ProductModel(Base):
    __tablename__ = "products"

    stock_code = Column(String, primary_key=True, index=True)
    description = Column(String)


class TransactionModel(Base):
    __tablename__ = "transactions"

    invoice_no = Column(String, ForeignKey("invoices.invoice_no"), index=True)
    stock_code = Column(String, ForeignKey("products.stock_code"), index=True)
    line_no = Column(Integer, index=True)
    quantity = Column(Integer, index=True)
    unit_price = Column(Float, index=True)
    total_amount = Column(Float, index=True)
    transaction_type = Column(String)

    __table_args__ = (PrimaryKeyConstraint("invoice_no", "stock_code", "line_no"),)
