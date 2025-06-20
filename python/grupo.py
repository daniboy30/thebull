import json
from alumno import Alumno
from maestro import Maestro
from arreglo import Arreglo

class Grupo(Arreglo):
    _id_counter = 1

    def __init__(self,
                 nombre: str = None,
                 ciclo_escolar: str = None,
                 salon: str = None,
                 maestro: Maestro = None,
                 alumnos: list = None):
        """
        Constructor dual:
        - Sin parámetros: crea un contenedor vacío de grupos (es_arreglo=True).
        - Con datos: crea un grupo individual, asignando maestro y lista de alumnos opcional.
        """
        # Caso contenedor
        if nombre is None and ciclo_escolar is None and salon is None and maestro is None and alumnos is None:
            super().__init__()
            self.es_arreglo = True
            return

        # Caso grupo individual
        self.id = Grupo._id_counter
        Grupo._id_counter += 1
        self.nombre = nombre
        self.ciclo_escolar = ciclo_escolar
        self.salon = salon
        self.maestro = maestro
        # Inicializa contenedor de alumnos
        self.alumnos = Alumno()
        # Agrega lista inicial si se proporciona
        if alumnos:
            for a in alumnos:
                self.alumnos.agregar(a)
        self.es_arreglo = False

    def convADiccionario(self):
        if self.es_arreglo:
            return self.convADiccionarios()

        alumnos_list = [a.convADiccionario() for a in self.alumnos.items]
        maestro_dict = self.maestro.convADiccionario() if self.maestro else None

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

    def es_grupo(self, dic):
        campos = {"id", "nombre", "ciclo_escolar", "salon", "maestro", "alumnos"}
        return campos.issubset(dic.keys())

    def instanciarDesdeJson(self, datos):
        # Aplanar listas anidadas
        if isinstance(datos, list):
            flat = []
            for elem in datos:
                if isinstance(elem, list):
                    flat.extend(elem)
                else:
                    flat.append(elem)
            datos = flat

            for d in datos:
                if not isinstance(d, dict):
                    continue
                grupo = Grupo()
                grupo.id = d.get("id", 0)
                grupo.nombre = d.get("nombre")
                grupo.ciclo_escolar = d.get("ciclo_escolar")
                grupo.salon = d.get("salon")

                # Maestro
                grupo.maestro = Maestro(**d["maestro"]) if d.get("maestro") else None

                # Alumnos
                grupo.alumnos = Alumno()
                if d.get("alumnos"):
                    grupo.alumnos.instanciarDesdeJson(d["alumnos"])

                self.agregar(grupo)
            return True

        # Caso único dict
        if isinstance(datos, dict):
            self.id = datos.get("id", 0)
            self.nombre = datos.get("nombre")
            self.ciclo_escolar = datos.get("ciclo_escolar")
            self.salon = datos.get("salon")

            self.maestro = Maestro(**datos["maestro"]) if datos.get("maestro") else None

            self.alumnos = Alumno()
            if datos.get("alumnos"):
                for alumno_dict in datos["alumnos"]:
                    alumno = Alumno(**alumno_dict)
                    self.alumnos.agregar(alumno)
            return True

        return False

if __name__ == "__main__":
    grupos = Grupo()
    grupos.leerJson('grupos.json')
    grupos.mostrar_diccionario()