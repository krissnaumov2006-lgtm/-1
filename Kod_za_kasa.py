import streamlit as st

# 1. Настройки за мобилни устройства
st.set_page_config(page_title="Levro", layout="centered")

# CSS за изчистен дизайн и компактност
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stNumberInput { margin-bottom: -15px !important; }
    
    .item-calculation { 
        font-size: 16px; 
        font-weight: bold; 
        color: #FFFFFF; 
        margin-top: 5px;
        margin-bottom: 10px;
        text-align: left;
    }

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

n_items = st.number_input("Брой артикули:", min_value=1, step=1, value=1, key=f"n_{st.session_state.reset_counter}")

total_eur = 0.0

st.write("### Сметка")

for i in range(1, n_items + 1):
    col_price, col_qty = st.columns([3, 2])
    
    with col_price:
        price = st.number_input(
            f"Цена в евро € (Арт. {i})", 
            min_value=0.0, step=0.10, format="%.2f", 
            value=None, 
            placeholder="0.00",
            key=f"p_{i}_{st.session_state.reset_counter}"
        )
    
    with col_qty:
        qty = st.number_input(
            f"Брой", 
            min_value=1, step=1, value=1, 
            key=f"q_{i}_{st.session_state.reset_counter}"
        )
    
    if price:
        item_total = price * qty
        total_eur += item_total
        st.markdown(f"<div class='item-calculation'>{qty} бр. х {price:.2f} € = {item_total:.2f} €</div>", unsafe_allow_html=True)
    
    st.markdown("<hr style='margin: 5px 0px; opacity: 0.1;'>", unsafe_allow_html=True)

# --- ОБЩИ РЕЗУЛТАТИ ---
st.divider()
total_bgn = total_eur * 1.95583

col_res1, col_res2 = st.columns(2)
with col_res1:
    st.metric("ОБЩО EUR", f"{total_eur:.2f} €")
with col_res2:
    st.metric("ОБЩО BGN", f"{total_bgn:.2f} лв.")

# --- ПЛАЩАНЕ И РЕСТО (ОБНОВЕНО) ---
if total_eur > 0:
    st.subheader("💶 Плащане")
    currency = st.radio("Валута:", ("BGN", "EUR"), horizontal=True, key=f"curr_{st.session_state.reset_counter}")
    
    if currency == "BGN":
        given = st.number_input("Дадени лв:", min_value=0.0, step=1.0, value=None, placeholder="0.00", key=f"gb_{st.session_state.reset_counter}")
        if given is not None:
            if given >= total_bgn:
                diff_bgn = given - total_bgn
                st.success(f"**РЕСТО:** {diff_bgn:.2f} лв. / {diff_bgn / 1.95583:.2f} €")
            else:
                st.warning(f"**Оставащи:** {total_bgn - given:.2f} лв.")
    else:
        given = st.number_input("Дадени €:", min_value=0.0, step=1.0, value=None, placeholder="0.00", key=f"ge_{st.session_state.reset_counter}")
        if given is not None:
            if given >= total_eur:
                diff_eur = given - total_eur
                st.success(f"**РЕСТО:** {diff_eur:.2f} € / {diff_eur * 1.95583:.2f} лв.")
            else:
                st.warning(f"**Оставащи:** {total_eur - given:.2f} €")
            






















