from alumnoApp import AlumnoApp
from maestroApp import MaestroApp
from grupoApp import GrupoApp

def main():
    while True:
        print("==== Sistema de Gestión ====")
        print("1) Módulo Alumnos")
        print("2) Módulo Maestros")
        print("3) Módulo Grupos")
        print("4) Salir")
        opcion = input().strip()

        if opcion == "1":
            # Instancia AlumnoApp sin argumentos -> cargará alumnos.json si existe
            app = AlumnoApp()
            app.correr()
        elif opcion == "2":
            app_m = MaestroApp()
            app_m.correr()
        elif opcion == "3":
            app_g = GrupoApp()
            app_g.correr()
        elif opcion == "4":
            print("Saliendo...")
            break
        else:
            print("Opción inválida. Intenta de nuevo.")

if __name__ == "__main__":
    main()