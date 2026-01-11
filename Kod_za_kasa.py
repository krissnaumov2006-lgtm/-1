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
    
    /* Сближаване на полетата */
    .stNumberInput { margin-bottom: -10px !important; }
    
    /* Бял текст за сметката */
    .item-calculation { 
        font-size: 18px; 
        font-weight: bold; 
        color: #FFFFFF; 
        padding: 0px;
        margin-top: 5px;
        margin-bottom: 15px;
        text-align: left;
    }
    
    /* Увеличаване на бутоните + и - за по-лесно натискане на телефон */
    button[step="1"], button[step="0.01"] {
        min-height: 40px !important;
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

# --- ВЪВЕЖДАНЕ НА ОБЩИЯ БРОЙ ВИДОВЕ СТОКИ ---
# Тук също имаш + и - за добавяне на нови редове
n_items = st.number_input(
    "Брой различни стоки:", 
    min_value=1, 
    step=1, 
    value=1, 
    key=f"n_{st.session_state.reset_counter}"
)

total_eur = 0.0

st.write("### Сметка")

for i in range(1, n_items + 1):
    col_price, col_qty = st.columns([3, 2])
    
    with col_price:
        # Цена със стъпка 0.10 или ръчно въвеждане
        price = st.number_input(
            f"Цена € (Арт. {i})", 
            min_value=0.0, 
            step=0.10, 
            format="%.2f", 
            value=None, 
            placeholder="0.00 €", 
            key=f"p_{i}_{st.session_state.reset_counter}"
        )
    
    with col_qty:
        # Бройка със стъпка 1 (бутони + и -)
        qty = st.number_input(
            f"Брой", 
            min_value=1, 
            step=1,
            value=1, # Сложих 1 по подразбиране, за да работят + и - веднага
            key=f"q_{i}_{st.session_state.reset_counter}"
        )
    
    if price is not None:
        item_total = price * qty
        total_eur += item_total
        st.markdown(f"<div class='item-calculation'>{qty} бр. х {price:.2f} € = {item_total:.2f} €</div>", unsafe_allow_html=True)

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
        given = st.number_input(
            "Сума от клиента (лв):", 
            min_value=0.0, 
            step=1.0, # Бутони за левове
            value=None, 
            placeholder="Въведи сума...", 
            key=f"gb_{st.session_state.reset_counter}"
        )
        if given and given >= total_bgn:
            change_bgn = given - total_bgn
            st.success(f"РЕСТО: {change_bgn:.2f} лв.")
            st.info(f"В ЕВРО: {change_bgn/1.95583:.2f} €")
        elif given:
            st.warning(f"Още {total_bgn - given:.2f} лв.")
            
    else:
        given = st.number_input(
            "Сума от клиента (€):", 
            min_value=0.0, 
            step=1.0, # Бутони за евро
            value=None, 
            placeholder="Въведи сума...", 
            key=f"ge_{st.session_state.reset_counter}"
        )
        if given and given >= total_eur:
            change_eur = given - total_eur
            st.success(f"РЕСТО: {change_eur:.2f} €")
            st.info(f"В ЛЕВА: {change_eur * 1.95583:.2f} лв.")
        elif given:
            st.warning(f"Още {total_eur - given:.2f} €")

















