import json
from maestro import Maestro

class MaestroApp:
    def __init__(self):
        self.json_loaded = False
        self.maestros = Maestro()
        try:
            self.maestros.leerJson("maestros.json")
            print("Datos cargados desde 'maestros.json'.")
            self.json_loaded = True
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def correr(self):
        while True:
            print("==== Gestor de Maestros ====")
            print("1) Listar todos los maestros")
            print("2) Agregar un nuevo maestro")
            print("3) Editar un maestro existente")
            print("4) Eliminar un maestro")
            print("5) Mostrar como diccionarios")
            print("6) Salir")
            opcion = input().strip()

            if opcion == "1":
                self.listar_maestros()
            elif opcion == "2":
                self.agregar_maestro()
            elif opcion == "3":
                self.editar_maestro()
            elif opcion == "4":
                self.eliminar_maestro()
            elif opcion == "5":
                self.mostrar_como_diccionarios()
            elif opcion == "6":
                print("Saliendo...")
                break
            else:
                print("Opción no válida. Intenta de nuevo.")

    def listar_maestros(self):
        if not self.maestros.items:
            print("No hay maestros registrados.")
            return
        print("=== LISTA DE MAESTROS ===")
        for m in self.maestros.items:
            print(f"ID: {getattr(m, 'id', 'N/A')}")
            print(f"Nombre: {m.nombre} {m.apellido}")
            print(f"Cédula: {m.cedula}")
            print(f"Especialidad: {m.especialidad}")
            print(f"Años de experiencia: {m.años_experiencia}")
            print("-" * 40)

    def agregar_maestro(self):
        print("Agregar Nuevo Maestro")
        nombre = input("Nombre: ").strip()
        apellido = input("Apellido: ").strip()
        cedula = input("Cédula: ").strip()
        especialidad = input("Especialidad: ").strip()
        try:
            años = int(input("Años de experiencia: ").strip())
        except ValueError:
            print("ERROR: Años inválido.")
            return

        # Validaciones
        if not nombre or not apellido or not cedula or not especialidad:
            print("ERROR: Todos los campos son obligatorios.")
            return
        if any(ma.cedula == cedula for ma in self.maestros.items):
            print("ERROR: Ya existe un maestro con esa cédula.")
            return

        # Crear maestro y asignar ID
        next_id = self._obtener_id()
        nuevo = Maestro(nombre, apellido, cedula, especialidad, años)
        setattr(nuevo, 'id', next_id)
        self.maestros.agregar(nuevo)
        print(f"OK: Maestro agregado con ID {next_id}.")
        if self.json_loaded:
            self.guardar_datos()
        else:
            print("Aviso: No se cargó JSON previamente. Los cambios no se guardarán.")

    def _obtener_id(self):
        if not self.maestros.items:
            return 1
        ids = []
        for a in self.maestros.items:
            try:
                ids.append(int(getattr(a, 'id', 0)))
            except (ValueError, TypeError):
                ids.append(0)
        return max(ids) + 1

    def editar_maestro(self):
        if not self.maestros.items:
            print("No hay maestros para editar.")
            return
        self.listar_maestros()
        id_buscar = input("Ingrese ID del maestro a editar: ").strip()
        maestro = next((m for m in self.maestros.items if str(getattr(m, 'id', '')) == id_buscar), None)
        if not maestro:
            print("ERROR: Maestro no encontrado.")
            return

        print("--- Editar Maestro ---")
        nuevo_nombre = input(f"Nombre [{maestro.nombre}]: ").strip() or maestro.nombre
        nuevo_apellido = input(f"Apellido [{maestro.apellido}]: ").strip() or maestro.apellido
        cedula_nueva = input(f"Cédula [{maestro.cedula}]: ").strip() or maestro.cedula
        especialidad_nueva = input(f"Especialidad [{maestro.especialidad}]: ").strip() or maestro.especialidad
        años_raw = input(f"Años de experiencia [{maestro.años_experiencia}]: ").strip()

        maestro.nombre = nuevo_nombre
        maestro.apellido = nuevo_apellido
        if cedula_nueva != maestro.cedula and any(m.cedula == cedula_nueva for m in self.maestros.items if m is not maestro):
            print("ERROR: Cédula duplicada. Se conserva la anterior.")
        else:
            maestro.cedula = cedula_nueva
        maestro.especialidad = especialidad_nueva
        if años_raw:
            try:
                maestro.años_experiencia = int(años_raw)
            except ValueError:
                print("ERROR: Años inválido. Se conserva el anterior.")

        print("OK: Maestro actualizado.")
        if self.json_loaded:
            self.guardar_datos()

    def eliminar_maestro(self):
        if not self.maestros.items:
            print("No hay maestros para eliminar.")
            return
        self.listar_maestros()
        id_eliminar = input("Ingrese ID del maestro a eliminar: ").strip()
        if self.maestros.eliminar(id_eliminar):
            print("OK: Maestro eliminado.")
            if self.json_loaded:
                self.guardar_datos()
        else:
            print("ERROR: No se pudo eliminar el maestro.")

    def guardar_datos(self):
        try:
            self.maestros.crearJson("maestros.json")
            print("OK: Datos guardados en 'maestros.json'.")
        except Exception as e:
            print(f"ERROR al guardar datos: {e}")

    def mostrar_como_diccionarios(self):
        lista = self.maestros.convADiccionarios()
        print(json.dumps(lista, indent=2, ensure_ascii=False))
