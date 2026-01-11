import streamlit as st

# 1. Настройки за мобилни устройства
st.set_page_config(page_title="Levro", layout="centered")

# CSS за изчистен дизайн, бели букви и компактност
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Сближаване на елементите */
    .stNumberInput { margin-bottom: -15px !important; }
    
    /* Стил за изчислението - Бял текст */
    .item-calculation { 
        font-size: 16px; 
        font-weight: bold; 
        color: #FFFFFF; 
        margin-top: 5px;
        margin-bottom: 10px;
        text-align: left;
    }

    /* Настройка на височината на полетата за телефон */
    div[data-baseweb="input"] {
        height: 45px !important;
    }
    </style>
    """, unsafe_allow_html=True)

if 'reset_counter' not in st.session_state:
    st.session_state.reset_counter = 0

st.title("💳 Levro")

# --- БУТОН ЗА НОВА СМЕТКА ---
if st.button("🔄 НОВА СМЕТКА", use_container_width=True, type="primary"):
    st.session_state.reset_counter += 1
    for key in list(st.session_state.keys()):
        if key != 'reset_counter':
            del st.session_state[key]
    st.rerun()

st.divider()

# Регулиране на броя редове
n_items = st.number_input("Брой видове стоки:", min_value=1, step=1, value=1, key=f"n_{st.session_state.reset_counter}")

total_eur = 0.0

st.write("### Сметка")

for i in range(1, n_items + 1):
    # РАЗМЕНЕНИ: Цена (Ляво - 3 части), Брой (Дясно - 2 части)
    col_price, col_qty = st.columns([3, 2])
    
    with col_price:
        # Празно поле за цена (без нули за триене)
        price = st.number_input(
            f"Цена € (Арт. {i})", 
            min_value=0.0, step=0.10, format="%.2f", 
            value=None, 
            placeholder="0.00",
            key=f"p_{i}_{st.session_state.reset_counter}"
        )
    
    with col_qty:
        # Брой с бутони + и - (започва от 1)
        qty = st.number_input(
            f"Брой", 
            min_value=1, step=1, value=1, 
            key=f"q_{i}_{st.session_state.reset_counter}"
        )
    
    # Показване на сметката веднага под тях
    if price:
        item_total = price * qty
        total_eur += item_total
        st.markdown(f"<div class='item-calculation'>{qty} бр. х {price:.2f} € = {item_total:.2f} €</div>", unsafe_allow_html=True)
    
    # Тънка линия между артикулите
    st.markdown("<hr style='margin: 5px 0px; opacity: 0.1;'>", unsafe_allow_html=True)

# --- ОБЩИ РЕЗУЛТАТИ ---
st.divider()
total_bgn = total_eur * 1.95583

col_res1, col_res2 = st.columns(2)
with col_res1:
    st.metric("ОБЩО EUR", f"{total_eur:.2f} €")
with col_res2:
    st.metric("ОБЩО BGN", f"{total_bgn:.2f} лв.")

# --- ПЛАЩАНЕ ---
if total_eur > 0:
    st.subheader("💶 Плащане")
    currency = st.radio("Валута:", ("BGN", "EUR"), horizontal=True, key=f"curr_{st.session_state.reset_counter}")
    
    if currency == "BGN":
        given = st.number_input("Дадени лв:", min_value=0.0, step=1.0, value=None, placeholder="0.00", key=f"gb_{st.session_state.reset_counter}")
        if given and given >= total_bgn:
            st.success(f"РЕСТО: {given - total_bgn:.2f} лв.")
    else:
        given = st.number_input("Дадени €:", min_value=0.0, step=1.0, value=None, placeholder="0.00", key=f"ge_{st.session_state.reset_counter}")
        if given and given >= total_eur:
            st.success(f"РЕСТО: {given - total_eur:.2f} €")
            




















