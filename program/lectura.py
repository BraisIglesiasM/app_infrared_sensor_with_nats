
"""--------------------IMPORTS--------------------"""
# librerias de python
import asyncio


"""--------------------LECTURA SENSOR--------------------"""

async def leer_datos(cola, frecuencia):
    """esta tarea solo funciona cuando la cola esta llena. en cuanto se vacia 
    (se para la lectura por input), finaliza """

    while cola.full():

            print('leyendo')
            await asyncio.sleep(frecuencia)
