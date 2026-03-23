from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker
import os
import time
import uuid

# ===== ОЖИДАНИЕ БД =====
time.sleep(5)

DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "postgres-service")
DB_NAME = os.getenv("DB_NAME", "sales_db")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ===== МОДЕЛЬ =====
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    category = Column(String)

Base.metadata.create_all(bind=engine)

app = FastAPI()

# ===== КОРЗИНА =====
cart = []

# ===== НАЧАЛЬНЫЕ ДАННЫЕ =====
def seed_data():
    db = SessionLocal()
    if db.query(Product).count() == 0:
        products = [
            Product(name="Ноутбук", price=80000, quantity=5, category="Техника"),
            Product(name="Смартфон", price=50000, quantity=10, category="Техника"),
            Product(name="Наушники", price=7000, quantity=15, category="Аксессуары"),
            Product(name="Клавиатура", price=4000, quantity=8, category="Аксессуары"),
            Product(name="Мышь", price=2500, quantity=12, category="Аксессуары"),
            Product(name="Монитор", price=20000, quantity=6, category="Техника"),
            Product(name="Часы", price=15000, quantity=9, category="Гаджеты"),
            Product(name="Планшет", price=30000, quantity=7, category="Техника"),
        ]
        db.add_all(products)
        db.commit()
    db.close()

seed_data()

# ===== API =====

@app.get("/products")
def get_products():
    db = SessionLocal()
    data = db.query(Product).order_by(Product.id).all()
    db.close()
    return data

@app.post("/cart")
def add_to_cart(product_id: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product or product.quantity <= 0:
        db.close()
        return {"error": "Нет в наличии"}

    product.quantity -= 1
    db.commit()

    cart.append({
        "cart_id": str(uuid.uuid4()),
        "product_id": product.id,
        "name": product.name,
        "price": product.price
    })

    db.close()
    return {"message": "ok"}

@app.get("/cart")
def get_cart():
    return cart

@app.delete("/cart/{cart_id}")
def remove_from_cart(cart_id: str):
    db = SessionLocal()

    for item in cart:
        if item["cart_id"] == cart_id:
            product = db.query(Product).filter(Product.id == item["product_id"]).first()
            if product:
                product.quantity += 1

            cart.remove(item)
            break

    db.commit()
    db.close()

    return {"message": "removed"}

@app.delete("/cart")
def clear_cart():
    cart.clear()
    return {"message": "cleared"}