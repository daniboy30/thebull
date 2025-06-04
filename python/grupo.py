import json
from alumno import Alumno
from maestro import Maestro
from arreglo import Arreglo
from pprint import pprint

class Grupo(Arreglo):
    def __init__(self, nombre: str = None, ciclo_escolar: str = None, salon: str = None, maestro: Maestro = None):
        self.id = 0
        self.nombre = nombre
        self.ciclo_escolar = ciclo_escolar
        self.salon = salon
        self.alumnos = Alumno()
        self.maestro = maestro
        self.es_arreglo = False

        if nombre is None and ciclo_escolar is None and salon is None and maestro is None:
            super().__init__()
            self.es_arreglo = True

    def convADiccionario(self):
        if self.es_arreglo:
            return self.convADiccionarios()

        alumnos_list = []
        if hasattr(self.alumnos, 'items'):
            for a in self.alumnos.items:
                alumnos_list.append(a.convADiccionario())

        maestro_dict = None
        if self.maestro:
            maestro_dict = self.maestro.convADiccionario()

        return {
            "id": self.id,
            "nombre": self.nombre,
            "ciclo_escolar": self.ciclo_escolar,
            "salon": self.salon,
            "alumnos": alumnos_list,
            "maestro": maestro_dict
        }

    def mostrar_diccionario(self):
        print(self.convADiccionario())

    def __str__(self):
        if self.es_arreglo:
            return super().__str__()
        return (
            f"Grupo: {self.nombre}, Ciclo: {self.ciclo_escolar}, Salón: {self.salon}, "
            f"Maestro: {self.maestro.nombre if self.maestro else 'Sin asignar'}, "
            f"Alumnos: {len(self.alumnos.items)}"
        )

    """def leerJson(self, nombre_archivo):
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            return json.load(archivo)"""

    def crear_maestro(self, data):
        if not data:
            return None
        return Maestro(
            nombre=data.get("nombre"),
            apellido=data.get("apellido"),
            cedula=data.get("cedula"),
            especialidad=data.get("especialidad"),
            años_experiencia=data.get("años_experiencia")
        )

    def crear_alumnos(self, lista):
        alumnos = Alumno()
        alumnos.crear_desde_dict(lista)
        """
        for a in lista:
            nuevo = Alumno(
                nombre=a.get("nombre"),
                apellido=a.get("apellido"),
                edad=a.get("edad"),
                matricula=a.get("matricula"),
                promedio=a.get("promedio"),
                materias=a.get("materias", [])
            )
            alumnos.agregar(nuevo)
        """
        return alumnos

    def crear_desde_dict(self, data):
        grupo = Grupo(
            nombre=data.get("nombre"),
            ciclo_escolar=data.get("ciclo_escolar"),
            salon=data.get("salon"),
            maestro=self.crear_maestro(data.get("maestro"))
        )
        grupo.alumnos = self.crear_alumnos(data.get("alumnos", []))
        grupo.id = data.get("id", 0)
        return grupo

    def es_grupo(self, dic):
        campos = {"id", "nombre", "ciclo_escolar", "salon", "maestro", "alumnos"}
        return campos.issubset(dic.keys())


    def instanciarDesdeJson(self, datos):
        if isinstance(datos, str):
            # Si es un archivo, primero lo abrimos
            try:
                with open(datos, 'r', encoding='utf-8') as archivo:
                    datos = json.load(archivo)
            except Exception as e:
                print(f"Error al leer archivo JSON: {e}")
                return False

        if isinstance(datos, list):
            for item in datos:
                if self.es_grupo(item):
                    grupo = self.crear_desde_dict(item)
                    self.agregar(grupo)
                else:
                    return False
        elif isinstance(datos, dict):
            if self.es_grupo(datos):
                grupo = self.crear_desde_dict(datos)
                self.agregar(grupo)
            else:
                return False
        else:
            return False
        return True


        

if __name__ == "__main__":
    alumno1 = Alumno(nombre="Saul", apellido="Pérez", edad=18, matricula="23170140", promedio=8.5)
    alumno2 = Alumno(nombre="Azael", apellido="González", edad=19, matricula="23170141", promedio=9.2)
    alumno3 = Alumno(nombre="Jesús", apellido="Ramírez", edad=18, matricula="23170142", promedio=7.8)

    maestro1 = Maestro(nombre="Daniel", apellido="Garcia", cedula="C98765", especialidad="Programador", años_experiencia=10)

    grupo_matematicas = Grupo(nombre="TSU", ciclo_escolar="2025-A", salon="14", maestro=maestro1)
    grupo_matematicas.alumnos.agregar(alumno1)
    grupo_matematicas.alumnos.agregar(alumno2)
    grupo_matematicas.alumnos.agregar(alumno3)

    grupos = Grupo()
    grupos.agregar(grupo_matematicas)

    print(grupo_matematicas)
    grupo_matematicas.mostrar_diccionario()
    print(grupos)

    grupos.crearJson("grupos.json")

    print("==============================================================")
    grupos_desde_json = Grupo()
    grupos_desde_json.instanciarDesdeJson("grupos.json")
    print(grupos_desde_json)
    grupos_desde_json.mostrar_diccionario()

    