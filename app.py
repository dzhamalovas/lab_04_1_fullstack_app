import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend-service:8000")

st.set_page_config(
    page_title="Shop",
    page_icon="🛍️",
    layout="wide"
)

# ===== ЭМОДЗИ КАК ФОТО =====
def get_icon(category):
    icons = {
        "Техника": "💻",
        "Аксессуары": "🎧",
        "Гаджеты": "⌚"
    }
    return icons.get(category, "📦")

# ===== КОРЗИНА В SIDEBAR =====
st.sidebar.title("🧺 Корзина")

cart_res = requests.get(f"{BACKEND_URL}/cart")
cart = cart_res.json() if cart_res.status_code == 200 else []

total = 0

for item in cart:
    st.sidebar.write(f"{item['name']} — {item['price']} ₽")
    total += item["price"]

st.sidebar.markdown("---")
st.sidebar.success(f"Итого: {total} ₽")

if st.sidebar.button("🛒 Оформить заказ"):
    requests.delete(f"{BACKEND_URL}/cart")
    st.sidebar.success("Заказ оформлен!")

# ===== КАТАЛОГ =====
st.title("🛍️ Каталог товаров")

res = requests.get(f"{BACKEND_URL}/products")

if res.status_code != 200:
    st.error("Ошибка загрузки")
    st.stop()

data = res.json()

# ===== ПОИСК =====
search = st.text_input("🔍 Поиск")

# ===== ФИЛЬТР =====
categories = list(set([item["category"] for item in data]))
selected_category = st.selectbox("Категория", ["Все"] + categories)

# ===== ФИЛЬТРАЦИЯ =====
filtered = []

for item in data:
    if search.lower() not in item["name"].lower():
        continue
    if selected_category != "Все" and item["category"] != selected_category:
        continue
    filtered.append(item)

# ===== СЕТКА =====
cols = st.columns(4)

for i, item in enumerate(filtered):
    with cols[i % 4]:
        st.markdown(f"## {get_icon(item['category'])}")
        st.markdown(f"**{item['name']}**")
        st.write(f"💰 {item['price']} ₽")

        if st.button("Добавить", key=item["id"]):
            requests.post(f"{BACKEND_URL}/cart", params={"product_id": item["id"]})
            st.success("Добавлено!")

        # ===== КАРТОЧКА (детали) =====
        with st.expander("Подробнее"):
            st.write(f"📦 Осталось: {item['quantity']}")
            st.write(f"🏷️ Категория: {item['category']}")