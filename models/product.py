from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, Table, Text
from sqlalchemy.sql.sqltypes import Float

from config.db import meta

brands = Table(
    "brands",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String(100)),
)

categories = Table(
    "categories",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String(100)),
)

products = Table(
    "products",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String(100)),
    Column("brand_id", Integer, ForeignKey("brands.id"), nullable=False),
    Column("category_id", Integer, ForeignKey("categories.id"), nullable=False),
    Column("image", Text),
    Column("qty", Integer, default=0),
    Column("price", Float),
)
