from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    warehouses = relationship("Warehouse", back_populates="company")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    location = Column(String)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    company = relationship("Company", back_populates="warehouses")
    inventory_items = relationship("Inventory", back_populates="warehouse")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    sku = Column(String, unique=True, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    is_bundle = Column(Boolean, default=False, nullable=False)
    low_stock_threshold = Column(Integer, nullable=False, default=20)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    bundle_components = relationship(
        "ProductBundle",
        foreign_keys="ProductBundle.bundle_id",
        back_populates="bundle",
    )
    parent_bundles = relationship(
        "ProductBundle",
        foreign_keys="ProductBundle.product_id",
        back_populates="product",
    )
    inventory_items = relationship("Inventory", back_populates="product")
    supplier_products = relationship("SupplierProduct", back_populates="product")


class ProductBundle(Base):
    __tablename__ = "product_bundles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    bundle_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    bundle = relationship("Product", foreign_keys=[bundle_id], back_populates="bundle_components")
    product = relationship("Product", foreign_keys=[product_id], back_populates="parent_bundles")


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    product = relationship("Product", back_populates="inventory_items")
    warehouse = relationship("Warehouse", back_populates="inventory_items")


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    contact_email = Column(Text)

    supplier_products = relationship("SupplierProduct", back_populates="supplier")


class SupplierProduct(Base):
    __tablename__ = "supplier_products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    cost_price = Column(Numeric(10, 2), nullable=False)

    supplier = relationship("Supplier", back_populates="supplier_products")
    product = relationship("Product", back_populates="supplier_products")
