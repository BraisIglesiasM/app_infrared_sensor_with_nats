
"""--------------------IMPORTS--------------------"""
# librerias de python
import asyncio
import aioconsole

# modulos propios
from lectura import leer_datos


async def inicio_paro(cola, frecuencia):
        """funcion llamada desde app, encargada de iniciar o parar la lectura de datos del sensor 
        mediante imputs por consola enviar una q para el servicio y, si esta parado, enviar 'Inicio' 
        lo reanuda. Por defecto empieza iniciado. Se utiliza una queue para compartir informacion sobre 
        el estado requerido entre las funciones concurrentes (como leer_datos.lectura)"""
        
        while True:

            # si no hay items en la cola quiere decir que se ha detenido la lectura, por lo que se espera un Inicio para reanudarla
            if cola.empty():
                # para que el input no bloquee las demas funciones asincronas trabajando en concurrencia, se usa la libreria aioconsole
                # aioconsole es compatible con los awaits de asyncio y no bloquea el hilo principal
                comando = await aioconsole.ainput('Introduzca ''Inicio'' para comenzar la lectura: \n')
                #comando = input('Introduzca ''Inicio'' para comenzar la lectura: \n')
                if comando == 'Inicio':
                    # se llena la cola
                    cola.put(True)  
                    # y se vuelve a lanzar la tarea de lectura, que habia terminado
                    asyncio.get_event_loop().create_task(leer_datos(cola, frecuencia))

                else:
                    print('No se ha reconocido la instrucción')
                    
            # si ya hay un item significa que esta leyendo datos del sensor, por lo que la orden seria de parar
            if cola.full():
                comando = await aioconsole.ainput('Introduzca ''q'' para detener la lectura: \n')
                #comando = input('Introduzca ''Fin'' para finalizar la lectura: \n')
                if comando == 'q':
                    # se vacia la cola
                    cola.get()     
                else:
                    print('No se ha reconocido la instrucción')

