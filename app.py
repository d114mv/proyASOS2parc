import streamlit as st

st.set_page_config(
    page_title="Simulador de Planificación",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .algorithm-card {
        padding: 2rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin: 1rem 0;
        cursor: pointer;
        transition: transform 0.3s ease;
    }
    .algorithm-card:hover {
        transform: translateY(-5px);
    }
    .developer-card {
        background: #2e3440;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #88c0d0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">🧠 Simulador de Algoritmos de Planificación</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🚀 Selecciona un Algoritmo")
        
        # Tarjetas de algoritmos
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("## ⚡ SRT\n\nShortest Remaining Time", use_container_width=True, key="srt"):
                st.switch_page("pages/2_⚡_SRT.py")
            
            if st.button("## 🟡 SJF\n\nShortest Job First", use_container_width=True, key="sjf"):
                st.switch_page("pages/3_🟡_SJF.py")
        
        with col_b:
            st.info("""
            ### 📋 Características:
            - **Entrada interactiva** de procesos
            - **Visualización en tiempo real**
            - **Métricas de rendimiento**
            - **Diagramas de Gantt interactivos**
            """)
    
    with col2:
        st.markdown("### 👥 Desarrollado por:")
        developers = [
            "Muriel Vargas Dilan Itamar",
            "Quintana Callejas Marco Antonio", 
            "Murillo Rodriguez Juan Rodolfo",
            "Aduviri Calizaya Leonel"
        ]
        
        for dev in developers:
            st.markdown(f'<div class="developer-card">🧑‍💻 {dev}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()