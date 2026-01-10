import streamlit as st

# Настройки на страницата
st.set_page_config(page_title="Дигитална Каса", page_icon="💰")

st.title("💰 Система за плащане (EUR/BGN)")
st.write("Въведете детайлите на покупката по-долу:")

# Инициализация на състоянието (за да не се нулира при всяко кликване)
if 'total_sum' not in st.session_state:
    st.session_state.total_sum = 0.0

# ---- ВЪВЕЖДАНЕ НА АРТИКУЛИ ----
with st.sidebar:
    st.header("🛒 Добавяне на артикули")
    num_items = st.number_input("Брой артикули:", min_value=1, step=1, value=1)
    
    current_sum = 0.0
    for i in range(1, num_items + 1):
        price = st.number_input(f"Цена на артикул {i} (€):", min_value=0.0, step=0.10, key=f"item_{i}")
        if price < 1.0 and price > 0:
            st.warning("Минималната цена е 1 евро.")
        current_sum += price
    
    st.session_state.total_sum = current_sum

# ---- ОСНОВЕН ЕКРАН ----
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Обща сума (EUR)", value=f"{round(st.session_state.total_sum, 2)} €")

with col2:
    st.metric(label="Обща сума (BGN)", value=f"{round(st.session_state.total_sum * 1.95583, 2)} лв.")

st.divider()

# ---- ИЗБОР НА ВАЛУТА И ПЛАЩАНЕ ----
payment_currency = st.radio("Изберете валута за плащане:", ("BGN", "EUR"))

if st.session_state.total_sum > 0:
    if payment_currency == "BGN":
        bill_bgn = st.session_state.total_sum * 1.95583
        customer_money = st.number_input("Сума дадена от клиента (лв.):", min_value=0.0, step=0.50)
        
        if customer_money < bill_bgn and customer_money > 0:
            st.error(f"Недостатъчно! Трябват още {round(bill_bgn - customer_money, 2)} лв.")
        elif customer_money >= bill_bgn:
            change_bgn = customer_money - bill_bgn
            change_eur = change_bgn / 1.95583
            
            st.success("Плащането е успешно!")
            st.subheader("Ресто:")
            st.info(f"💶 {round(change_eur, 2)} EUR")
            st.info(f"🇧🇬 {round(change_bgn, 2)} BGN")

    else: # EUR
        customer_money = st.number_input("Сума дадена от клиента (€):", min_value=0.0, step=0.50)
        
        if customer_money < st.session_state.total_sum and customer_money > 0:
            st.error(f"Недостатъчно! Трябват още {round(st.session_state.total_sum - customer_money, 2)} €")
        elif customer_money >= st.session_state.total_sum:
            change_eur = customer_money - st.session_state.total_sum
            change_bgn = change_eur * 1.95583
            
            st.success("Плащането е успешно!")
            st.subheader("Ресто:")
            st.info(f"💶 {round(change_eur, 2)} EUR")
            st.info(f"🇧🇬 {round(change_bgn, 2)} BGN")
