import json
from arreglo import Arreglo

class Maestro(Arreglo):
    def __init__(self, nombre=None, apellido=None, cedula=None, especialidad=None, años_experiencia=None, id=None):
        if nombre is None and apellido is None and cedula is None and especialidad is None and años_experiencia is None:
            super().__init__()
            self.es_arreglo = True
        else:
            self.id = cedula
            self.nombre = nombre
            self.apellido = apellido
            self.cedula = cedula
            self.especialidad = especialidad
            self.años_experiencia = años_experiencia
            self.es_arreglo = False

    def es_maestro(self, dic):
        campos = {"nombre", "apellido", "cedula", "especialidad", "años_experiencia"}
        return campos.issubset(dic.keys())

    def actualizarExperiencia(self, años):
        self.años_experiencia = años

    def convADiccionario(self):
        if self.es_arreglo:
            return super().mostrar_diccionario()
        diccionario = self.__dict__.copy()
        diccionario.pop('es_arreglo', None)
        return diccionario

    def imprimir_diccionario(self):
        if not self.es_arreglo:
            print(json.dumps(self.convADiccionario(), indent=4))

    def __str__(self):
        if self.es_arreglo:
            return super().__str__()
        return (
            f"Maestro: {self.nombre} {self.apellido}\n"
            f"Especialidad: {self.especialidad}\n"
            f"Años de experiencia: {self.años_experiencia}"
        )

    def instanciarDesdeJson(self, datos):

        if isinstance(datos, list):
            for d in datos:
                if self.es_maestro(d):
                    maestro = Maestro(**d)
                    self.agregar(maestro)
                else:
                    return False
        elif isinstance(datos, dict):
            if self.es_maestro(datos):
                maestro = Maestro(**datos)
                self.agregar(maestro)
        else:
            return False
        return True

    def leerJson(self, archivo):
        with open(archivo, 'r', encoding='utf-8') as f:
            datos = json.load(f)
            return self.instanciarDesdeJson(datos)

if __name__ == "__main__":
    maestro1 = Maestro("Danna", "Martinez", "C98766", "Programadora", 10)
    maestro2 = Maestro("Daniel", "Garcia", "C98765", "Programador", 10)
    maestro3 = Maestro("Juan", "Chavez", "C98777", "Programador-master", 10)

    maestros = Maestro()
    maestros.agregar(maestro1, maestro2, maestro3)

    print(maestro1)
    maestro1.imprimir_diccionario()

    maestro1.actualizarExperiencia(12)

    maestros.eliminar("C98765")

    maestros.crearJson("maestros.json")

    print(maestros)
    print(maestros.convADiccionario())

    print("===============================================")
    instanciaTemporal = Maestro()
    instanciaTemporal.leerJson("maestros.json")
    instanciaTemporal.mostrar_diccionario()
