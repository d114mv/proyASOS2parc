import streamlit as st

st.set_page_config(
    page_title="Inicio - Simulador Planificación",
    page_icon="🏠"
)

st.title("🏠 Página de Inicio")

st.markdown("""
## Bienvenido al Simulador de Algoritmos de Planificación

Este sistema te permite simular y visualizar el comportamiento de diferentes 
algoritmos de planificación de procesos en sistemas operativos.

### 📊 Algoritmos Disponibles:

#### ⚡ SRT (Shortest Remaining Time)
- **Preemptivo** por naturaleza
- Selecciona el proceso con **menor tiempo restante**
- Ideal para **tiempos de respuesta cortos**

#### 🟡 SJF (Shortest Job First)  
- **No preemptivo**
- Ejecuta primero los procesos **más cortos**
- Minimiza el **tiempo de espera promedio**

### 🎯 Cómo usar:
1. Selecciona un algoritmo en el sidebar
2. Ingresa los procesos (llegada y duración)
3. Ejecuta la simulación
4. Analiza los resultados y métricas

---

*Desarrollado como proyecto académico*
""")

# Navegación en sidebar
st.sidebar.title("Navegación")
if st.sidebar.button("⚡ Ir a SRT"):
    st.switch_page("pages/2_⚡_SRT.py")
if st.sidebar.button("🟡 Ir a SJF"):
    st.switch_page("pages/3_🟡_SJF.py")