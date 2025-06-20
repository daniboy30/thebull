import json
from grupo import Grupo
from alumno import Alumno
from maestro import Maestro
from alumnoApp import AlumnoApp
from arreglo import Arreglo  # Importar Arreglo al inicio

class GrupoApp:
    def __init__(self):
        self.json_loaded = False  # SOLO PARA GRUPOS

        self.maestros = Maestro()
        try:
            self.maestros.leerJson("maestros.json")
            print("Maestros cargados desde 'maestros.json'.")
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        self.alumnos = Alumno()
        try:
            self.alumnos.leerJson("alumnos.json")
            print("Alumnos cargados desde 'alumnos.json'.")
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        self.grupos = Grupo()
        try:
            self.grupos.leerJson("grupos.json")
            print("Grupos cargados desde 'grupos.json'.")
            self.json_loaded = True
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def correr(self):
        while True:
            print("==== Gestor de Grupos ====")
            print("1) Listar todos los grupos")
            print("2) Crear nuevo grupo")
            print("3) Seleccionar grupo existente")
            print("4) Mostrar como diccionario")
            print("5) Salir")
            opcion = input("Opción: ").strip()

            if opcion == "1":
                self.listar_grupos()
            elif opcion == "2":
                self.crear_grupo()
            elif opcion == "3":
                self.menu_grupo()
            elif opcion == "4":
                self.mostrar_como_diccionarios()
                if self.json_loaded:
                    self.guardar_datos()
            elif opcion == "5":
                print("Saliendo...")
                if self.json_loaded:
                    self.guardar_datos()
                break
            else:
                print("Opción no válida. Intenta de nuevo.")

    def listar_grupos(self):
        if not self.grupos.items:
            print("No hay grupos registrados.")
            return
        print("=== LISTA DE GRUPOS ===")
        for g in self.grupos.items:
            maestro_nombre = f"{g.maestro.nombre} {g.maestro.apellido}" if g.maestro else "N/A"
            print(f"ID: {g.id} | Nombre: {g.nombre} | Maestro: {maestro_nombre} | Alumnos: {len(g.alumnos.items)}")
        print("-" * 40)

    def crear_grupo(self):
        print("=== Crear Nuevo Grupo ===")
        nombre = input("Nombre: ").strip()
        ciclo = input("Ciclo escolar: ").strip()
        salon = input("Salón: ").strip()
        if not self.maestros.items:
            print("ERROR: No hay maestros registrados.")
            return
        print("Selecciona un maestro:")
        for m in self.maestros.items:
            print(f"ID: {getattr(m, 'id')} | {m.nombre} {m.apellido}")
        id_m = input("ID maestro: ").strip() #pido id del maestro
        maestro = next((m for m in self.maestros.items if str(getattr(m, 'id', '')) == id_m), None)#busco el maestro por ID
        if not maestro:
            print("ERROR: Maestro no encontrado.")
            return

        alumnos = Arreglo()#creo un arreglo para los alumnos
        app_al = AlumnoApp(alumnos=alumnos, alumnos_global=self.alumnos)#mi interfaz de alumnos
        app_al.correr()#inicio la interfaz de alumnos


        next_id = self._obtener_id()# obtengo el siguiente ID para el grupo
        nuevo = Grupo(nombre, ciclo, salon, maestro, alumnos)#creo un nuevo grupo
        setattr(nuevo, 'id', next_id)#le asigno el ID al grupo
        self.grupos.agregar(nuevo) #agrego el grupo a mi arreglo de grupos
        total = len(nuevo.alumnos.items) # obtengo el total de alumnos en el grupo
        print(f"Grupo '{nombre}' (ID {next_id}) creado con {total} alumno(s).")
        if self.json_loaded:
            self.guardar_datos()
        else:
            print("No se cargó JSON de grupos. Los cambios no se guardarán.")

    def menu_grupo(self):
        if not self.grupos.items:
            print("No hay grupos para seleccionar.")
            return
        self.listar_grupos()
        id_g = input("Ingrese ID del grupo: ").strip()
        grupo = next((g for g in self.grupos.items if str(g.id) == id_g), None)
        if not grupo:
            print("ERROR: Grupo no encontrado.")
            return
        app_al = AlumnoApp(alumnos=grupo.alumnos)
        app_al.correr()
        if self.json_loaded:
            self.guardar_datos()

    def _obtener_id(self):
        if not self.grupos.items:
            return 1
        ids = []
        for g in self.grupos.items:
            try:
                ids.append(int(g.id))
            except (ValueError, TypeError):
                ids.append(0)
        return max(ids) + 1

    def guardar_datos(self):
        try:
            datos = [g.convADiccionario() for g in self.grupos.items]
            with open("grupos.json", 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=4)
            print("Grupos guardados en 'grupos.json'.")
        except Exception as e:
            print(f"ERROR al guardar grupos: {e}")

    def mostrar_como_diccionarios(self):
        lista = [g.convADiccionario() for g in self.grupos.items]
        print(json.dumps(lista, indent=2, ensure_ascii=False))
