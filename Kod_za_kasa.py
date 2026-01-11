import streamlit as st

st.set_page_config(page_title="Levro Pro", page_icon="💳")

# Инициализиране на състоянието
if 'items' not in st.session_state:
    st.session_state.items = [{"price": 0.0, "qty": 1}]

st.title("💳 Levro Pro")

# --- БУТОНИ ЗА БЪРЗО ДОБАВЯНЕ ---
st.write("### Бързо добавяне:")
col_a, col_b, col_c = st.columns(3)
with col_a:
    if st.button("+ 1.00 €"): st.session_state.items.append({"price": 1.0, "qty": 1})
with col_b:
    if st.button("+ 2.00 €"): st.session_state.items.append({"price": 2.0, "qty": 1})
with col_c:
    if st.button("🔄 НУЛИРАЙ"): 
        st.session_state.items = [{"price": 0.0, "qty": 1}]
        st.rerun()

st.divider()

# --- СПИСЪК С АРТИКУЛИ ---
total_eur = 0.0
for i, item in enumerate(st.session_state.items):
    c1, c2, c3 = st.columns([3, 2, 1])
    with c1:
        new_price = st.number_input(f"Цена {i+1} (€)", min_value=0.0, value=item["price"], key=f"p_{i}")
    with c2:
        new_qty = st.number_input(f"Брой", min_value=1, value=item["qty"], key=f"q_{i}")
    with c3:
        st.write(f"**{new_price * new_qty:.2f}**")
    total_eur += (new_price * new_qty)

if st.button("➕ Добави нов ред"):
    st.session_state.items.append({"price": 0.0, "qty": 1})
    st.rerun()

# --- ОБОБЩЕНИЕ ---
st.divider()
st.metric("ОБЩО EUR", f"{total_eur:.2f} €")
st.metric("ОБЩО BGN", f"{total_eur * 1.95583:.2f} лв.")








