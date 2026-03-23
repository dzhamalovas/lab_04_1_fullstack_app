import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend-service:8000")

st.set_page_config(
    page_title="Product Catalog",
    page_icon="🛍️",
    layout="wide"
)

# ===== SIDEBAR =====
st.sidebar.title("🛍️ Магазин")
page = st.sidebar.radio("Меню", ["Каталог", "Корзина"])

# ===== КАТАЛОГ =====
def show_catalog():
    st.title("🛒 Каталог товаров")

    res = requests.get(f"{BACKEND_URL}/products")

    if res.status_code != 200:
        st.error("Ошибка загрузки")
        return

    data = res.json()

    if not data:
        st.info("Нет товаров")
        return

    # ===== ПОИСК =====
    search = st.text_input("🔍 Поиск товара")

    # ===== ФИЛЬТР =====
    categories = list(set([item["category"] for item in data]))
    selected_category = st.selectbox("📂 Категория", ["Все"] + categories)

    # ===== ФИЛЬТРАЦИЯ =====
    filtered = []

    for item in data:
        if search.lower() not in item["name"].lower():
            continue
        if selected_category != "Все" and item["category"] != selected_category:
            continue
        filtered.append(item)

    # ===== ВЫВОД =====
    cols = st.columns(3)

    for i, item in enumerate(filtered):
        with cols[i % 3]:
            st.markdown(f"### {item['name']}")
            st.write(f"💰 {item['price']} ₽")
            st.write(f"📦 Осталось: {item['quantity']}")
            st.write(f"🏷️ {item['category']}")

            if st.button(f"Добавить {item['id']}"):
                requests.post(f"{BACKEND_URL}/cart", params={"product_id": item["id"]})
                st.success("Добавлено!")

# ===== КОРЗИНА =====
def show_cart():
    st.title("🧺 Корзина")

    res = requests.get(f"{BACKEND_URL}/cart")

    if res.status_code != 200:
        st.error("Ошибка")
        return

    cart = res.json()

    if not cart:
        st.info("Корзина пустая")
        return

    total = 0

    for item in cart:
        col1, col2 = st.columns([4, 1])

        with col1:
            st.write(f"🛍️ {item['name']} — {item['price']} ₽")

        with col2:
            if st.button("❌", key=f"del_{item['id']}"):
                requests.delete(f"{BACKEND_URL}/cart/{item['id']}")
                st.rerun()

        total += item["price"]

    st.success(f"💳 Итого: {total} ₽")

    if st.button("Очистить корзину"):
        requests.delete(f"{BACKEND_URL}/cart")
        st.rerun()

# ===== ROUTER =====
if page == "Каталог":
    show_catalog()

elif page == "Корзина":
    show_cart()