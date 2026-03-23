import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend-service:8000")

st.set_page_config(page_title="Shop", layout="wide")

# ===== ИКОНКИ =====
def get_icon(name):
    icons = {
        "Ноутбук": "💻",
        "Смартфон": "📱",
        "Наушники": "🎧",
        "Клавиатура": "⌨️",
        "Мышь": "🖱️",
        "Монитор": "🖥️",
        "Часы": "⌚",
        "Планшет": "📲",
    }
    return icons.get(name, "📦")

# ===== КОРЗИНА (SIDEBAR) =====
st.sidebar.title("🧺 Корзина")

try:
    cart_res = requests.get(f"{BACKEND_URL}/cart")
    cart = cart_res.json()
except:
    cart = []

total = sum([item["price"] for item in cart])

for item in cart:
    st.sidebar.write(f"{item['name']} — {item['price']} ₽")

st.sidebar.markdown("---")
st.sidebar.success(f"Итого: {total} ₽")

if st.sidebar.button("🛒 Оформить заказ"):
    requests.delete(f"{BACKEND_URL}/cart")
    st.sidebar.success("Заказ оформлен!")
    st.rerun()

# ===== НАВИГАЦИЯ =====
page = st.sidebar.radio("Меню", ["Каталог", "Корзина"])

# ===== КАТАЛОГ =====
def show_catalog():
    st.title("🛍️ Каталог")

    res = requests.get(f"{BACKEND_URL}/products")
    data = res.json()

    search = st.text_input("🔍 Поиск")

    categories = list(set([i["category"] for i in data]))
    category = st.selectbox("Категория", ["Все"] + categories)

    filtered = []
    for item in data:
        if search.lower() not in item["name"].lower():
            continue
        if category != "Все" and item["category"] != category:
            continue
        filtered.append(item)

    cols = st.columns(4)

    for i, item in enumerate(filtered):
        with cols[i % 4]:
            st.markdown(f"## {get_icon(item['name'])}")
            st.markdown(f"**{item['name']}**")
            st.write(f"💰 {item['price']} ₽")

            if item["quantity"] == 0:
                st.error("Нет в наличии")
            else:
                if st.button("В корзину", key=f"add_{item['id']}"):
                    requests.post(f"{BACKEND_URL}/cart", params={"product_id": item["id"]})
                    st.success("В корзине")
                    st.rerun()

            with st.expander("Подробнее"):
                st.write(f"📦 Осталось: {item['quantity']}")
                st.write(f"🏷️ {item['category']}")

# ===== КОРЗИНА СТРАНИЦА =====
def show_cart():
    st.title("🧺 Корзина")

    if not cart:
        st.info("Корзина пустая")
        return

    for item in cart:
        col1, col2 = st.columns([5,1])

        with col1:
            st.write(f"{item['name']} — {item['price']} ₽")

        with col2:
            if st.button("❌", key=item["cart_id"]):
                requests.delete(f"{BACKEND_URL}/cart/{item['cart_id']}")
                st.rerun()

    st.success(f"Итого: {total} ₽")

    if st.button("🛒 Оформить заказ"):
        requests.delete(f"{BACKEND_URL}/cart")
        st.success("Заказ оформлен!")
        st.rerun()

# ===== ROUTER =====
if page == "Каталог":
    show_catalog()
else:
    show_cart()