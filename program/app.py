

"""--------------------IMPORTS--------------------"""
# librerias de python
from queue import Queue
import asyncio
import aioconsole

# modulos propios
from lectura import leer_datos
from gestionInput import inicio_paro



async def enviar_datos(cola):

    pass




"""--------------------APLICACION--------------------"""


async def app(tipo_sensor: str = 'real', frecuencia: int = 2, 
              mockup_min: int = 0, mockup_max:int = 100):
    """Programa principal llamado desde el main. Recibe las consigas
    dadas por consola en la configuracion e inicia las tareas 
    concurrentes (atender ordenes por consola y leer datos)"""

    print(tipo_sensor)
    print(frecuencia)
    print(f'{mockup_min} - {mockup_max}')

    cola = Queue(1)
    cola.put(True)

    try:
        # se espera a que terminen dos tareas concurrentes. una de ellas (inicio_paro) es un bucle infinito, asi que no terminara nunca 
        await asyncio.gather(inicio_paro(cola, frecuencia), leer_datos(cola, frecuencia))
    except KeyboardInterrupt:
        quit()
