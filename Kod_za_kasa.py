import streamlit as st

# 1. Настройки на страницата
st.set_page_config(page_title="Levro", page_icon="💳")

# Инициализиране на брояч за пълно нулиране
if 'cnt' not in st.session_state:
    st.session_state.cnt = 0

st.title("💳 Levro")

# 2. БУТОН ЗА НОВА СМЕТКА
if st.button("🔄 НОВА СМЕТКА", use_container_width=True):
    st.session_state.cnt += 1
    st.rerun()

st.divider()

# 3. ВЪВЕЖДАНЕ
# Ключовете се променят спрямо st.session_state.cnt, за да се чистят полетата
n = st.number_input("Брой стоки:", min_value=1, step=1, value=1, key=f"n_{st.session_state.cnt}")

total_eur = 0.0

for i in range(1, n + 1):
    val = st.number_input(
        f"Цена {i} (€):", 
        min_value=0.0, 
        format="%.2f", 
        value=None, 
        placeholder="0.00", 
        key=f"i_{i}_{st.session_state.cnt}"
    )
    if val:
        total_eur += val

# 4. РЕЗУЛТАТИ
st.divider()
total_bgn = total_eur * 1.95583

st.metric("ОБЩО EUR", f"{total_eur:.2f} €")
st.metric("ОБЩО BGN", f"{total_bgn:.2f} лв.")

# 5. ПЛАЩАНЕ И РЕСТО
if total_eur > 0:
    st.subheader("💶 Плащане")
    valuta = st.radio("Валута:", ("BGN", "EUR"), horizontal=True, key=f"v_{st.session_state.cnt}")
    
    if valuta == "BGN":
        plateno = st.number_input("Дадени лв:", min_value=0.0, value=None, placeholder="0.00", key=f"p_b_{st.session_state.cnt}")
        if plateno and plateno >= total_bgn:
            resto_bgn = plateno - total_bgn
            st.success(f"РЕСТО: {resto_bgn:.2f} лв.")
            st.info(f"В ЕВРО: {resto_bgn/1.95583:.2f} €")
        elif plateno:
            st.warning(f"Още {total_bgn - plateno:.2f} лв.")
            
    else:
        plateno = st.number_input("Дадени €:", min_value=0.0, value=None, placeholder="0.00", key=f"p_e_{st.session_state.cnt}")
        if plateno and plateno >= total_eur:
            resto_eur = plateno - total_eur
            st.success(f"РЕСТО: {resto_eur:.2f} €")
            st.info(f"В ЛЕВА: {resto_eur * 1.95583:.2f} лв.")
        elif plateno:
            st.warning(f"Още {total_eur - plateno:.2f} €")









