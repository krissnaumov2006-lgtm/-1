import streamlit as st

# Настройки на приложението
st.set_page_config(page_title="Levro", page_icon="💳", layout="centered")

# Скриване на излишните менюта за чист App вид
st.markdown("<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>", unsafe_allow_html=True)

# Инициализиране на брояч за нулиране (ако не съществува)
if 'reset_counter' not in st.session_state:
    st.session_state.reset_counter = 0

st.title("💳 Levro")
st.write("Твоят дигитален касиер")

# --- БУТОН ЗА НОВА СМЕТКА ---
if st.button("🔄 НОВА СМЕТКА (Изчисти всичко)", use_container_width=True):
    # Увеличаваме брояча, за да принудим Streamlit да пресъздаде всички полета празни
    st.session_state.reset_counter += 1
    # Изчистваме старите данни от паметта
    for key in list(st.session_state.keys()):
        if key != 'reset_counter':
            del st.session_state[key]
    st.rerun()

st.divider()

# --- ВЪВЕЖДАНЕ НА АРТИКУЛИ ---
# Добавяме суфикс от брояча към ключа на всяко поле
num_items = st.number_input("Брой артикули:", min_value=1, step=1, value=1, key=f"num_{st.session_state.reset_counter}")

total_eur = 0.0

st.write("### Въведи цени (€):")
for i in range(1, num_items + 1):
    price = st.number_input(
        f"Артикул {i}", 
        min_value=0.0, 
        step=0.01, 
        format="%.2f", 
        value=None, 
        placeholder="Пиши цена тук...",
        key=f"item_{i}_{st.session_state.reset_counter}"
    )
    if price:
        total_eur += price

# --- РЕЗУЛТАТИ ---
st.divider()
total_bgn = total_eur * 1.95583

col1, col2 = st.columns(2)
with col1:
    st.metric("ОБЩО EUR", f"{total_eur:.2f} €")
with col2:
    st.metric("ОБЩО BGN", f"{total_bgn:.2f} лв.")

# --- ПЛАЩАНЕ ---
if total_eur > 0:
    st.markdown("---")
    st.subheader("💶 Плащане")
    currency = st.radio("Валута на плащане:", ("BGN", "EUR"), horizontal=True, key=f"curr_{st.session_state.reset_counter}")
    
    if currency == "BGN":
        given = st.number_input("Сума от клиента (BGN):", min_value=0.0, value=None, placeholder="Въведи сума...", step=0.50, key=f"given_bgn_{st.session_state.reset_counter}")
        if given and given >= total_bgn:
            change_bgn = given - total_bgn
            st.success(f"РЕСТО: {change_bgn:.2f} лв. / {change_bgn/1.95583:.2f} €")
        elif given:
            st.warning(f"Недостиг: {total_bgn - given:.2f} лв.")
            
    else: # EUR
        given = st.number_input("Сума от клиента (EUR):", min_value=0.0, value=None, placeholder="Въведи сума...", step=0.50, key=f"given_eur_{st.session_state.reset_counter}")
        if given and given >= total_eur:
            change_eur = given - total_eur
            st.success(f"РЕСТО: {change_eur:.2f} € / {change_eur*1.95583:.2f} лв.")
        elif given:
            # ТУК БЕШЕ ГРЕШКАТА - ВЕЧЕ Е КОРИГИРАНО:
            st.warning(f"Недостиг: {total_eur - given:.2f} €")









