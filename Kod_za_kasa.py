import streamlit as st

st.set_page_config(page_title="Levro", page_icon="💳", layout="centered")

# Скриване на излишните менюта
st.markdown("<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>", unsafe_allow_html=True)

st.title("💳 Levro")

if st.button("🔄 НОВА СМЕТКА", use_container_width=True):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

st.divider()

# --- ВЪВЕЖДАНЕ НА АРТИКУЛИ ---
num_rows = st.number_input("Брой различни видове стоки:", min_value=1, step=1, value=1)

total_eur = 0.0

st.write("### Сметка:")
# Използваме колони за цена и количество на един ред
for i in range(1, num_rows + 1):
    col_price, col_qty = st.columns([2, 1]) # Цената е по-широка от количеството
    
    with col_price:
        price = st.number_input(
            f"Цена {i} (€)", 
            min_value=0.0, 
            format="%.2f", 
            value=None, 
            placeholder="0.00", 
            key=f"p_{i}"
        )
    
    with col_qty:
        qty = st.number_input(
            f"Брой {i}", 
            min_value=1, 
            step=1, 
            value=1, 
            key=f"q_{i}"
        )
    
    if price:
        total_eur += (price * qty)

# --- РЕЗУЛТАТИ ---
st.divider()
total_bgn = total_eur * 1.95583

st.metric("ОБЩО ЕВРО", f"{total_eur:.2f} €")
st.metric("ОБЩО ЛЕВА", f"{total_bgn:.2f} лв.")

# --- ПЛАЩАНЕ ---
if total_eur > 0:
    st.subheader("💶 Плащане")
    currency = st.radio("Валута:", ("BGN", "EUR"), horizontal=True)
    
    if currency == "BGN":
        given = st.number_input("Дадени от клиента (BGN):", min_value=0.0, value=None, placeholder="0.00", step=0.50)
        if given and given >= total_bgn:
            change_bgn = given - total_bgn
            st.success(f"РЕСТО: {change_bgn:.2f} лв. / {change_bgn/1.95583:.2f} €")
    else:
        given = st.number_input("Дадени от клиента (EUR):", min_value=0.0, value=None, placeholder="0.00", step=0.50)
        if given and given >= total_eur:
            change_eur = given - total_eur
            st.success(f"РЕСТО: {change_eur:.2f} € / {change_eur*1.95583:.2f} лв.")



