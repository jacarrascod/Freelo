import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("¿Cuánto cobrar por mi freelo?")

# Section 1: Monthly Expenses
st.header("Primero revisemos tus gastos mensuales")

# Initialize session state for expenses if not already
if "expenses" not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=["N°", "Nombre de gasto", "Valor"])

# Function to add a new expense
def add_expense(name, value):
    if name and value > 0:  # Ensure name is not empty and value is positive
        new_row = {"N°": len(st.session_state.expenses) + 1, "Nombre de gasto": name, "Valor": value}
        st.session_state.expenses = pd.concat([st.session_state.expenses, pd.DataFrame([new_row])], ignore_index=True)

# Function to clear all expenses
def clear_expenses():
    st.session_state.expenses = pd.DataFrame(columns=["N°", "Nombre de gasto", "Valor"])

# Form to add expenses
with st.form(key="expense_form"):
    expense_name = st.text_input("Nombre del gasto")
    expense_value = st.number_input("Valor del gasto", min_value=0.0, format="%.2f")
    submit_button = st.form_submit_button(label="Agregar gasto")

if submit_button:
    add_expense(expense_name, expense_value)

# Display expenses with an index column starting from 1
if not st.session_state.expenses.empty:
    # Clean the DataFrame by resetting index and removing any extra columns
    st.session_state.expenses = st.session_state.expenses.loc[:, ["N°", "Nombre de gasto", "Valor"]]
    st.dataframe(st.session_state.expenses, use_container_width=True)

# Button to clear all expenses, placed outside the form and only shown if there are expenses
if len(st.session_state.expenses) > 0:
    col1, col2 = st.columns([3, 1])
    with col2:
        clear_button = st.button("Limpiar")
    
    if clear_button:
        clear_expenses()

# Calculate total expenses
total_expenses = st.session_state.expenses["Valor"].sum()
st.write(f"<div style='text-align: right;'>**Total de gastos mensuales: S/. {total_expenses:.2f}**</div>", unsafe_allow_html=True)

# Section 2: Savings Percentage
st.header("Ahorro")
st.subheader("¿Qué porcentaje de mis ingresos quiero ahorrar?")
savings_percentage = st.slider("Elige el porcentaje de ahorro", min_value=0, max_value=99, value=10, step=1)

# Income Calculation
try:
    income = total_expenses / (1 - (savings_percentage / 100))
except ZeroDivisionError:
    income = 0

st.write(f"**Mensualmente debes ganar: S/. {income:.2f}**")

# Income breakdown
daily_income = income / 20
hourly_income = income / 160

st.write(f"Esto equivale a: \n- **S/. {daily_income:.2f} diarios** \n- **S/. {hourly_income:.2f} por hora**")

st.caption("*Se consideran 8 horas laborales de lunes a viernes.")

# Section 3: Freelo duration
st.header("¿Cuánto dura tu freelo?")
freelo_hours = st.number_input("Ingresa la cantidad de horas laborales que estimas que te tomará este freelo", min_value=1, step=1)

# Calculate the minimum price for the freelo
if freelo_hours > 0 and hourly_income > 0:
    min_freelo_price = freelo_hours * hourly_income
    st.markdown(f"\n\n### ***Por este freelo deberías cobrar como mínimo: S/. {min_freelo_price:.2f}***\n\n")

    # Additional comment about minimum price
    st.markdown("\n*Ten en cuenta que este es un valor referencial MINIMO. Sugerimos que establezcas tu precio tomando también en cuenta tu experiencia y el valor que le generas al cliente*\n\n")

# Pie Chart
st.subheader("\n\nDistribución de ingresos")
labels = ["Gastos", "Ahorro"]
values = [total_expenses, income - total_expenses]

# Prevent division by zero in case of unexpected values
if total_expenses > 0 and income > 0:
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90, colors=["#ff9999", "#66b3ff"])
    ax.axis("equal")
    st.pyplot(fig)
else:
    st.warning("No se puede generar el gráfico de distribución. Verifica los valores.")