import streamlit as st

# Настройки на страницата - Името в таба на браузъра
st.set_page_config(page_title="Levro - Дигитален касиер", page_icon="💳")

# Главно заглавие на приложението
st.title("💳 Твоят дигитален касиер Levro")
st.write("Бързо и точно пресмятане на покупки в EUR и BGN.")

# Инициализация на състоянието за общата сума
if 'total_sum' not in st.session_state:
    st.session_state.total_sum = 0.0

# ---- СТРАНИЧНА ПАНЕЛ: ВЪВЕЖДАНЕ НА АРТИКУЛИ ----
with st.sidebar:
    st.header("🛒 Нова покупка")
    num_items = st.number_input("Брой артикули:", min_value=1, step=1, value=1)
    
    current_sum = 0.0
    for i in range(1, num_items + 1):
        # Минимална цена 0.01 според изискването
        price = st.number_input(f"Цена на артикул {i} (€):", min_value=0.01, step=0.10, key=f"item_{i}")
        current_sum += price
    
    st.session_state.total_sum = current_sum
    st.divider()
    st.write("💡 *Въведете цените в евро, приложението ще ги пресметне автоматично в лева.*")

# ---- ОСНОВЕН ЕКРАН: ИНФОРМАЦИЯ ЗА СМЕТКАТА ----
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Общо в EUR", value=f"{round(st.session_state.total_sum, 2)} EUR")

with col2:
    # Фиксиран курс 1.95583
    total_bgn = st.session_state.total_sum * 1.95583
    st.metric(label="Общо в BGN", value=f"{round(total_bgn, 2)} BGN")

st.divider()

# ---- ПЛАЩАНЕ И РЕСТО ----
if st.session_state.total_sum > 0:
    st.subheader("💶 Плащане")
    payment_currency = st.radio("Изберете валута, в която плаща клиента:", ("BGN", "EUR"), horizontal=True)

    if payment_currency == "BGN":
        bill_bgn = st.session_state.total_sum * 1.95583
        customer_money = st.number_input("Сума, подадена от клиента (BGN):", min_value=0.0, step=0.50)
        
        if 0 < customer_money < bill_bgn:
            st.warning(f"Още {round(bill_bgn - customer_money, 2)} BGN са нужни.")
        elif customer_money >= bill_bgn:
            change_bgn = customer_money - bill_bgn
            change_eur = change_bgn / 1.95583
            
            st.success("Плащането е прието!")
            st.markdown("### **Ресто:**")
            st.info(f"{round(change_eur, 2)} EUR")
            st.info(f"{round(change_bgn, 2)} BGN")

    else: # EUR
        customer_money = st.number_input("Сума, подадена от клиента (EUR):", min_value=0.0, step=0.50)
        
        if 0 < customer_money < st.session_state.total_sum:
            st.warning(f"Още {round(st.session_state.total_sum - customer_money, 2)} EUR са нужни.")
        elif customer_money >= st.session_state.total_sum:
            change_eur = customer_money - st.session_state.total_sum
            change_bgn = change_eur * 1.95583
            
            st.success("Плащането е прието!")
            st.markdown("### **Ресто:**")
            st.info(f"{round(change_eur, 2)} EUR")
            st.info(f"{round(change_bgn, 2)} BGN")
else:
    st.info("Добавете артикули от менюто вляво, за да започнете.")


