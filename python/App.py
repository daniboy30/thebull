import streamlit as st
from alumnoApp import AlumnoApp 

class InstanciasAlumnosApp:
    def __init__(self):
        st.set_page_config(page_title="Gestor de Alumnos", layout="wide")
        st.title("Gestor de Alumnos")

        self.instancias_key = "instancias_alumnos"
        if self.instancias_key not in st.session_state:
            st.session_state[self.instancias_key] = {}

    def render(self):
        app_alumnos = AlumnoApp()
        app_alumnos.instancias = st.session_state[self.instancias_key]
        app_alumnos.render()
        st.session_state[self.instancias_key] = app_alumnos.instancias

if __name__ == "__main__":
    app = InstanciasAlumnosApp()
    app.render()