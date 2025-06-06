import json
from arreglo import Arreglo

class Alumno(Arreglo):
    def __init__(self, nombre=None, apellido=None, edad=None, matricula=None, promedio=None, materias=None):
        if nombre is None and apellido is None and edad is None and matricula is None and promedio is None:
            super().__init__()
            self.es_arreglo = True
        else:
            self.id = matricula 
            self.nombre = nombre
            self.apellido = apellido
            self.edad = edad
            self.matricula = matricula
            self.promedio = promedio
            self.materias = materias if materias else []
            self.es_arreglo = False

    def es_alumno(self, dic):
        campos = {"nombre", "apellido", "edad", "matricula", "promedio"}
        return campos.issubset(dic.keys())

    def actualizar_promedio(self, promedio):
        self.promedio = promedio

    def convADiccionario(self):
        if self.es_arreglo:
            return self.mostrar_diccionario()
        dic = self.__dict__.copy()
        dic.pop('es_arreglo', None)
        return dic

    def imprimir_diccionario(self):
        if not self.es_arreglo:
            print(json.dumps(self.convADiccionario(), indent=4))

    def __str__(self):
        if self.es_arreglo:
            return f"Total de alumnos: {super().__str__()}"
        return (
            f"Alumno: {self.nombre} {self.apellido}, {self.edad} años\n"
            f"Matrícula: {self.matricula}, Promedio: {self.promedio}, Materias: {self.materias}"
        )

    def instanciarDesdeJson(self,datos):
        
        if isinstance(datos, list):
            for item in datos:
                if self.es_alumno(item):
                    alumno = Alumno(
                        nombre=item.get('nombre'),
                        apellido=item.get('apellido'),
                        edad=item.get('edad'),
                        matricula=item.get('matricula'),
                        promedio=item.get('promedio'),
                        materias=item.get('materias', [])
                    )
                    self.agregar(alumno)
                else:
                    return False
        elif isinstance(datos, dict):
            if self.es_alumno(datos):
                alumno = Alumno(
                    nombre=datos.get('nombre'),
                    apellido=datos.get('apellido'),
                    edad=datos.get('edad'),
                    matricula=datos.get('matricula'),
                    promedio=datos.get('promedio'),
                    materias=datos.get('materias', [])
                )
                self.agregar(alumno)
            else:
                return False
        else:
            return False
        return True


if __name__ == "__main__":
    alumno1 = Alumno("Saul", "Pérez", 18, "23170140", 8.5)
    alumno2 = Alumno("Azael", "González", 19, "23170141", 9.2, materias=["Programación", "Matemáticas"])

    print("Alumnos individuales:")
    print(alumno1)
    print(alumno2)
    alumno1.imprimir_diccionario()

    print("Operaciones con arreglo de alumnos")
    alumnos = Alumno()
    alumnos.agregar(alumno1)
    alumnos.agregar(alumno2)
    print(f"Cantidad de alumnos en el arreglo: {alumnos}")

    alumno3 = Alumno("Maria", "López", 20, "23170142", 9.8, materias=["Historia", "Física"])
    alumnos.agregar(alumno3)
    print(f"Después de agregar un alumno más: {alumnos}")

    alumnos.eliminar("23170140")
    print(f"Después de eliminar el primer alumno: {alumnos}")

    alumno2.actualizar_promedio(9.5)
    print(f"Después de actualizar el promedio: {alumno2}")

    alumnos.crearJson("alumnos.json")
    alumnos.mostrar_diccionario()

    print("================================================")
    instancia = Alumno()
    instancia.leerJson("alumnos.json")
    instancia.mostrar_diccionario()
