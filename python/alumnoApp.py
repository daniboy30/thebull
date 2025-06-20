import os
import json
from alumno import Alumno

import os
import json
from alumno import Alumno

class AlumnoApp:
    def __init__(self, alumnos=None, alumnos_global=None):  # Ahora alumnos es opcional
        self.json_loaded = False  # Bandera para controlar si se cargó JSON exitosamente
        if alumnos is None:
            self.alumnos = Alumno()
            try:
                self.alumnos.leerJson("alumnos.json")
                print("Datos cargados desde 'alumnos.json'.")
                self.json_loaded = True
            except (FileNotFoundError, json.JSONDecodeError):
                pass
        else:
            self.alumnos = alumnos
            self.alumnos_global = alumnos_global or alumnos

    def correr(self):
        while True:
            print("==== Gestor de Alumnos ====")
            print("1) Listar todos los alumnos")
            print("2) Agregar un nuevo alumno")
            print("3) Editar un alumno existente")
            print("4) Eliminar un alumno")
            print("5) Mostrar como diccionarios")
            print("6) Salir")
            opcion = input().strip()

            if opcion == "1":
                self.listar_alumnos()
            elif opcion == "2":
                self.agregar_alumno()
            elif opcion == "3":
                self.editar_alumno()
            elif opcion == "4":
                self.eliminar_alumno()
            elif opcion == "5":
                self.mostrar_como_diccionarios()
            elif opcion == "6":
                print("Saliendo...")
                if self.json_loaded:
                    self.guardar_datos()
                break
            else:
                print("Opción no válida. Intenta de nuevo.")

    def listar_alumnos(self):
        if not self.alumnos.items:
            print("No hay alumnos registrados.")
            return
        print("=== LISTA DE ALUMNOS ===")
        for al in self.alumnos.items:
            materias_str = ", ".join(al.materias)
            print(f"ID: {getattr(al, 'id')}")
            print(f"Nombre: {al.nombre} {al.apellido}")
            print(f"Edad: {al.edad}")
            print(f"Matrícula: {al.matricula}")
            print(f"Promedio: {al.promedio}")
            print(f"Materias: {materias_str}")
            print("-" * 40)

    def agregar_alumno(self):
        print("¿Qué tipo de alumno deseas agregar?")
        print("1) Alumno nuevo")
        print("2) Alumno ya registrado")
        opcion = input("Selecciona una opción: ").strip()
        if opcion == "2":
            if not self.alumnos_global.items:
                print("No hay alumnos registrados en el sistema.")
                return
            print("=== Alumnos registrados disponibles ===")
            for a in self.alumnos_global.items:
                print(f"ID: {a.id} | Matrícula: {a.matricula} | {a.nombre} {a.apellido}")
            print("-" * 40)
            busqueda = input("Ingresa ID o matrícula del alumno que deseas agregar: ").strip()
            alumno_existente = next(
                (a for a in self.alumnos_global.items if str(getattr(a, 'id', '')) == busqueda or a.matricula == busqueda),
                None
            ) #busco el alumno por ID o matrícula
            if not alumno_existente:
                print("ERROR: Alumno no encontrado.")
                return

            if any(a.matricula == alumno_existente.matricula for a in self.alumnos.items):
                print("Este alumno ya fue agregado a este grupo.")
                return

            self.alumnos.agregar(alumno_existente)
            print(f"Alumno {alumno_existente.nombre} {alumno_existente.apellido} agregado al grupo.")
            return

        elif opcion != "1":
            print("Opción no válida.")
            return

        # Flujo original: alumno nuevo
        print("Agregar Nuevo Alumno")
        nombre = input("Nombre: ").strip()
        apellido = input("Apellido: ").strip()
        try:
            edad = int(input("Edad: ").strip())
        except ValueError:
            print("ERROR: Edad inválida.")
            return
        matricula = input("Matrícula: ").strip()
        try:
            promedio = float(input("Promedio (0 - 10): ").strip())
        except ValueError:
            print("ERROR: Promedio inválido.")
            return
        materias = [m.strip() for m in input("Materias (separadas por coma): ").split(",") if m.strip()]

        if not nombre or not apellido or not matricula:
            print("ERROR: Nombre, Apellido y Matrícula son obligatorios.")
            return
        if any(a.matricula == matricula for a in self.alumnos.items):
            print("ERROR: Ya existe un alumno con esa matrícula en este grupo.")
            return

        next_id = self._obtener_id()
        nuevo = Alumno(nombre, apellido, edad, matricula, promedio, materias)
        setattr(nuevo, 'id', next_id)
        self.alumnos.agregar(nuevo)
        print(f"Alumno nuevo agregado con ID {next_id}.")

        if self.json_loaded:
            self.guardar_datos()
        else:
            print("Aviso: No se cargó JSON previamente. Los cambios no se guardarán.")


    def _obtener_id(self):
        if not self.alumnos.items:
            return 1
        ids = [] #lista vacia para guardar mis ids
        for a in self.alumnos.items: # Recorro mi arreglo de alumnos
            try:
                ids.append(int(getattr(a, 'id', 0))) # guardo mi id entero en mi lista de ids
            except (ValueError, TypeError):
                ids.append(0)
        return max(ids) + 1 #al maximo id le sumo 1 para que sea el siguiente id disponible

    def editar_alumno(self):
        if not self.alumnos.items:
            print("No hay alumnos para editar.")
            return
        self.listar_alumnos()
        id_buscar = input("Ingrese ID del alumno a editar: ").strip()
        alumno = next((a for a in self.alumnos.items if str(getattr(a, 'id', '')) == id_buscar), None)
        if not alumno:
            print("ERROR: Alumno no encontrado.")
            return
        print("--- Editar Alumno (si no quieres cambiarlo solo da espacio---")
        nuevo_nombre = input(f"Nombre [{alumno.nombre}]: ").strip() or alumno.nombre
        nuevo_apellido = input(f"Apellido [{alumno.apellido}]: ").strip() or alumno.apellido
        edad_nueva = input(f"Edad [{alumno.edad}]: ").strip()
        if edad_nueva:
            try:
                alumno.edad = int(edad_nueva)
            except ValueError:
                print("ERROR: Edad inválida. Se mantiene el valor anterior.")
        matricula_nueva = input(f"Matrícula [{alumno.matricula}]: ").strip() or alumno.matricula
        if matricula_nueva != alumno.matricula and any(a.matricula == matricula_nueva for a in self.alumnos.items if a is not alumno):
            print("ERROR: Matrícula duplicada. Se conserva la anterior.")
        else:
            alumno.matricula = matricula_nueva
        promedio_nuevo = input(f"Promedio [{alumno.promedio}]: ").strip()
        if promedio_nuevo:
            try:
                alumno.promedio = float(promedio_nuevo)
            except ValueError:
                print("ERROR: Promedio inválido. Se conserva el anterior.")
        materias_nuevas = input(f"Materias [{', '.join(alumno.materias)}]: ").strip()
        if materias_nuevas:
            alumno.materias = [m.strip() for m in materias_nuevas.split(",") if m.strip()]
        alumno.nombre = nuevo_nombre
        alumno.apellido = nuevo_apellido
        print("OK: Alumno actualizado.")
        if self.json_loaded:
            self.guardar_datos()

    def eliminar_alumno(self):
        if not self.alumnos.items:
            print("No hay alumnos para eliminar.")
            return
        self.listar_alumnos()
        id_eliminar = input("Ingrese ID del alumno a eliminar: ").strip()
        if self.alumnos.eliminar(id_eliminar):
            print("OK: Alumno eliminado.")
            if self.json_loaded:
                self.guardar_datos()
        else:
            print("ERROR: No se pudo eliminar el alumno.")

    def guardar_datos(self):
        try:
            self.alumnos.crearJson("alumnos.json")
        except Exception as e:
            print(f"ERROR al guardar datos: {e}")

    def mostrar_como_diccionarios(self):
        lista = self.alumnos.convADiccionarios()
        print(json.dumps(lista, indent=2, ensure_ascii=False))

