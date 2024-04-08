
"""--------------------IMPORTS--------------------"""
# librerias de python
import argparse

# modulos propios
from app import app



"""--------------------MAIN--------------------"""

if __name__ == '__main__':

    # se utiliza la libreria argparse para poder usar argumentos de control en el momento de ejecucion
    # estos argumentos seran: tipo de sensor (real o mocked), frecuencia de lectura y rango (en caso de sensor mocked)

    # se inicializa el objeto de la clase ArgumentParser que recogerá los argumentos en la ejecución
    parser = argparse.ArgumentParser(description='App')

    # primer argumento: tipo de sensor a utilizar, obligatorio
    parser.add_argument('--sensor', type= str, required=True, help='Introduce el tipo de sensor a emplear (real | mockup)')

    # segundo argumento: tiempo de lectura (periodo) en segundos, obligatorio
    parser.add_argument('--frec', type=int, required=True, help='Introduce la frecuencia de lectura del sensor (en segundos)')

    # tercer argumento: rango de valores simulados
    parser.add_argument('--rangoMin', type=int, required=False, help='Introduce el minimo para valores generados en caso de sensor mockup')
    # cuarto argumento: maximo para el rango de valores simulados
    parser.add_argument('--rangoMax', type=int, required=False, help='Introduce el maximo para valores generados en caso de sensor mockup')

    args = parser.parse_args()

    # app es la funcion que encapsula la aplicacion de ejecucion ciclica
    app(args.sensor, args.frec, args.rangoMin, args.rangoMax)