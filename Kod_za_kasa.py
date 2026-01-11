import streamlit as st

# 1. Настройки за мобилни устройства
st.set_page_config(
    page_title="Levro", 
    page_icon="💳", 
    layout="centered"
)

# Оптимизация на интерфейса
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stNumberInput input { font-size: 18px !important; }
    .item-row { font-size: 16px; font-weight: bold; color: #1E88E5; margin-bottom: 10px; }
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

# --- ВЪВЕЖДАНЕ ---
n_items = st.number_input("Брой различни стоки:", min_value=1, step=1, value=1, key=f"n_{st.session_state.reset_counter}")

total_eur = 0.0

st.write("### Сметка")

for i in range(1, n_items + 1):
    col_price, col_qty = st.columns([3, 2])
    
    with col_price:
        price = st.number_input(
            f"Цена € (Арт. {i})", 
            min_value=0.0, 
            format="%.2f", 
            value=None, 
            placeholder="0.00 €", 
            key=f"p_{i}_{st.session_state.reset_counter}"
        )
    
    with col_qty:
        qty = st.number_input(
            f"Брой", 
            min_value=1, 
            value=1, 
            key=f"q_{i}_{st.session_state.reset_counter}"
        )
    
    # Показваме резултата за конкретния артикул под него
    if price is not None:
        item_total = price * qty
        total_eur += item_total
        # Форматиран надпис: "3 бр. х 2.00 € = 6.00 €"
        st.markdown(f"<div class='item-row'>👉 {qty} бр. х {price:.2f} € = {item_total:.2f} €</div>", unsafe_allow_html=True)
    st.divider()

# --- ОБЩИ РЕЗУЛТАТИ ---
total_bgn = total_eur * 1.95583

st.metric("ОБЩО ЕВРО", f"{total_eur:.2f} €")
st.metric("ОБЩО ЛЕВА", f"{total_bgn:.2f} лв.")

# --- ПЛАЩАНЕ ---
if total_eur > 0:
    st.subheader("💶 Плащане")
    # Вече използваме стандартния radio за по-добра стабилност на всички телефони
    currency = st.radio("Валута:", ("BGN", "EUR"), horizontal=True, key=f"curr_{st.session_state.reset_counter}")
    
    if currency == "BGN":
        given = st.number_input("Сума от клиента (лв):", min_value=0.0, value=None, placeholder="Въведи сума...", key=f"gb_{st.session_state.reset_counter}")
        if given and given >= total_bgn:
            change_bgn = given - total_bgn
            st.success(f"РЕСТО: {change_bgn:.2f} лв.")
            st.info(f"В ЕВРО: {change_bgn/1.95583:.2f} €")
        elif given:
            st.warning(f"Още {total_bgn - given:.2f} лв.")
            
    else:
        given = st.number_input("Сума от клиента (€):", min_value=0.0, value=None, placeholder="Въведи сума...", key=f"ge_{st.session_state.reset_counter}")
        if given and given >= total_eur:
            change_eur = given - total_eur
            st.success(f"РЕСТО: {change_eur:.2f} €")
            st.info(f"В ЛЕВА: {change_eur * 1.95583:.2f} лв.")
        elif given:
            st.warning(f"Още {total_eur - given:.2f} €")











