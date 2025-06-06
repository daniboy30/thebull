import json
from alumno import Alumno
from maestro import Maestro
from arreglo import Arreglo
from pprint import pprint

class Grupo(Arreglo):
    _id_counter = 1

    def __init__(self, nombre: str = None, ciclo_escolar: str = None, salon: str = None, maestro: Maestro = None):
        if nombre is None and ciclo_escolar is None and salon is None and maestro is None:
            super().__init__()
            self.es_arreglo = True
        else:
            self.id = Grupo._id_counter
            Grupo._id_counter += 1
            self.nombre = nombre
            self.ciclo_escolar = ciclo_escolar
            self.salon = salon
            self.maestro = maestro
            self.alumnos = Alumno()
            self.es_
            self.es_arreglo = False

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
        print(json.dumps(self.convADiccionario(), indent=4, ensure_ascii=False))

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


    def es_grupo(self, dic):
        campos = {"id", "nombre", "ciclo_escolar", "salon", "maestro", "alumnos"}
        return campos.issubset(dic.keys())

    def instanciarDesdeJson(self, datos):
        if isinstance(datos, list):
            for d in datos:
                grupo = Grupo()  
                grupo.id = d.get("id", 0)
                grupo.nombre = d.get("nombre")
                grupo.ciclo_escolar = d.get("ciclo_escolar")
                grupo.salon = d.get("salon")
                    
                if "maestro" in d and d["maestro"]:
                    grupo.maestro = Maestro(**d["maestro"])
                else:
                    grupo.maestro = None

                grupo.alumnos = Alumno()
                if "alumnos" in d and d["alumnos"]:
                    grupo.alumnos.instanciarDesdeJson(d["alumnos"])
                    """
                    for alumno_dict in d["alumnos"]:
                        alumno_data = alumno_dict.copy()
                        alumno_data.pop('id', None)
                        alumno = Alumno(**alumno_data)
                        grupo.alumnos.agregar(alumno)
                    """
                self.agregar(grupo)
            return True
        elif isinstance(datos, dict):
            self.id = datos.get("id", 0)
            self.nombre = datos.get("nombre")
            self.ciclo_escolar = datos.get("ciclo_escolar")
            self.salon = datos.get("salon")

            
            if "maestro" in datos and datos["maestro"]:
                self.maestro = Maestro(**datos["maestro"])
            else:
                self.maestro = None

            
            self.alumnos = Alumno()
            if "alumnos" in datos and datos["alumnos"]:
                for alumno_dict in datos["alumnos"]:
                    alumno = Alumno(**alumno_dict)
                    self.alumnos.agregar(alumno)
            return True
        return False


if __name__ == "__main__":
    grupos_desde_json = Grupo()
    grupos_desde_json.leerJson('grupos.json')
    grupos_desde_json.mostrar_diccionario()