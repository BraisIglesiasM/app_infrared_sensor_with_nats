
"""--------------------IMPORTS--------------------"""
# librerias de python
import time


"""--------------------LECTURA SENSOR--------------------"""

def leerdatos(cola, frecuencia):

    # este hilo solo funciona cuando la cola esta llena. en cuanto se vacia (se para la lectura), el hilo termina
    while cola.full():

            print('leyendo')
            #comando = await aioconsole.ainput('Introduzca ''q'' para detener la lectura: \n')
            #print(comando)
            time.sleep(frecuencia)
            #time.sleep(frecuencia)
