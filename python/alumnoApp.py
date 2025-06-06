import os
import streamlit as st
from alumno import Alumno

class AlumnoApp:
    def __init__(self):
        self.instancias = {}
        if os.path.exists("alumnos.json"):
            alumnos = Alumno()
            alumnos.leerJson("alumnos.json")
            self.instancias["alumno"] = alumnos
            st.info("json cargado correctamente")

    def formulario_alumno(self):
        nombre = st.text_input("Nombre", key="nombre")
        apellido = st.text_input("Apellido", key="apellido")
        edad = st.number_input("Edad", key="edad")
        matricula = st.text_input("Matrícula", key="matricula")
        promedio = st.number_input("Promedio", key="promedio")
        materias = st.text_area("Materias (separadas por comas)", key="materias", value="")
        materias_lista = [m.strip() for m in materias.split(",") if m.strip()]
        return Alumno(nombre, apellido, edad, matricula, promedio, materias_lista)

    def crear_instancia_vacia(self):
        st.subheader("Formulario de Instancia de Alumnos")
        with st.form("formulario_instancias"):
            nombre = st.text_input("Nombre de la instancia")
            crear_instancia = st.form_submit_button("Crear instancia")
            if crear_instancia:
                if nombre and nombre not in self.instancias:
                    self.instancias[nombre] = Alumno()
                    st.success(f"Instancia '{nombre}' creada.")
                    st.rerun()
                else:
                    st.error("El nombre de la instancia ya existe")

    def tarjetas_instancias(self):
        st.subheader("Instancias de alumnos existentes")
        if not self.instancias:
            st.info("No hay instancias registradas.")
            return

        cols = st.columns(min(4, len(self.instancias)))
        for i, (nombre, instancia) in enumerate(self.instancias.items()):
            with cols[i % len(cols)]:
                st.markdown(
                    f"""
                    <div style='
                        display:flex;flex-direction:column;align-items:center;
                        justify-content:center;width:256px;height:128px;
                        background:#262730;color:#fff;border:2.5px solid #585858;
                        border-radius:20px;text-align:center;'>
                        <div style="font-size:1.15em;font-weight:600;">{nombre}</div>
                        <div style="font-size:.93em;opacity:0.8;">Alumnos: <b>{len(instancia.items)}</b></div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                if st.button("Mostrar alumnos", key=f"mostrar_{nombre}"):
                    st.session_state["instancia_mostrando"] = nombre

    def tabla_alumnos(self, instancia):
        st.subheader("Alumnos registrados")
        alumnos = instancia.items
        if not alumnos:
            st.info("No hay alumnos en esta instancia.")
            return

        for idx, al in enumerate(alumnos):
            with st.expander(f"{al.nombre} {al.apellido} (Matrícula: {al.matricula})", expanded=True):
                nuevo_nombre = st.text_input("Nombre", al.nombre, key=f"edit_nombre_{al.matricula}")
                nuevo_apellido = st.text_input("Apellido", al.apellido, key=f"edit_apellido_{al.matricula}")
                nueva_edad = st.number_input("Edad", 0, 120, al.edad, value=int(al.edad), key=f"edit_edad_{al.matricula}")
                nueva_matricula = st.text_input("Matrícula", value=al.matricula, key=f"edit_matricula_{al.matricula}")
                nuevo_promedio = st.number_input("Promedio", 0.0, 10.0, al.promedio, step=0.1, key=f"edit_prom_{al.matricula}")
                materias_default = ", ".join(al.materias)
                nuevas_materias = st.text_area("Materias (separadas por coma)", value=materias_default, key=f"edit_materias_{al.matricula}")
                materias = [m.strip() for m in nuevas_materias.split(",") if m.strip()]
                col1, col2 = st.columns(2)
                if col1.button("Guardar", key=f"save_{al.matricula}"):
                    matriculas_existentes = [a.matricula for i, a in enumerate(alumnos) if i != idx]
                    if nueva_matricula in matriculas_existentes:
                        st.error("La matrícula ya existe.")
                    else:
                        al.nombre = nuevo_nombre
                        al.apellido = nuevo_apellido
                        al.edad = nueva_edad
                        al.matricula = nueva_matricula
                        al.promedio = nuevo_promedio
                        al.materias = materias
                        st.success("Alumno actualizado.")
                        st.rerun()

                if col2.button("Eliminar", key=f"del_{al.matricula}"):
                    instancia.eliminar(al.matricula)
                    st.warning("Alumno eliminado.")
                    st.rerun()

    def agregar(self, instancia):
        st.subheader("Agregar nuevo alumno")
        with st.form("agregar_alumno"):
            nuevo_alumno = self.formulario_alumno()
            agregar = st.form_submit_button("Agregar alumno")
            if agregar:
                matriculas_existentes = [al.matricula for al in instancia.items]
                if nuevo_alumno.matricula in matriculas_existentes:
                    st.error("La matrícula ya existe en esta instancia.")
                else:
                    instancia.agregar(nuevo_alumno)
                    st.success("Alumno agregado correctamente")
                    st.rerun()

    def opciones(self, instancia, instancia_actual):
        if st.button("Guardar instancia como JSON", key=f"guardar_{instancia_actual}"):
            instancia.crearJson("instancia_alumnos.json")
            st.success(f"Instancia '{instancia_actual}' guardada.")

        if st.button("Mostrar como diccionario", key=f"dict_{instancia_actual}_alumno"):
            st.json(instancia.convADiccionarios())

        if st.button("Ocultar alumnos"):
            st.session_state["instancia_mostrando"] = None

    def render(self):
        self.crear_instancia_vacia()
        st.markdown("---")
        self.tarjetas_instancias()

        instancia_actual = st.session_state.get("instancia_mostrando")
        if instancia_actual:
            st.markdown("---")
            st.subheader(f"Instancia activa: {instancia_actual}")
            instancia = self.instancias[instancia_actual]
            self.tabla_alumnos(instancia)
            self.agregar(instancia)
            self.opciones(instancia, instancia_actual)