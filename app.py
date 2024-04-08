
"""--------------------IMPORTS--------------------"""
# librerias de python
from queue import Queue
from threading import Thread

# modulos propios
from lectura import leerdatos


def enviarDatos(cola):

    pass


"""--------------------APLICACION--------------------"""


def app(tipoSensor: str= 'real', frecuencia: int= 2, mockupMin: int= 0, mockupMax:int = 100):

    print(tipoSensor)
    print(frecuencia)
    print(f'{mockupMin} - {mockupMax}')

    # objeto de clase Queue para comunicar entre hilos el inicio y el fin de la lectura. Cuando en la cola hay un objeto (es la capacidad maxima)
    # el metodo .full sera cierto, de forma que añadiendo (.put) y quitando (.get) de la cola, en funcion de las ordenes que se manden desde la 
    # terminal, el hilo secundario donde se realiza la lectura sabe si tiene que leer o no
    cola = Queue(1)
    cola.put(True)

    # ahora se crea y se lanza el hilo secundario, que tiene como funcion leer datos segun la frecuencia especificada en la ejecucion
    # daemon = true para que al terminar la ejecucion del hilo principal, este no siga en ejecucion
    hiloLectura = Thread(target= leerdatos, args=(cola, frecuencia, ), daemon= True)
    hiloLectura.start()

    # bucle infinito de la aplicacion (hilo principal)
    while True:

        # si el objeto de cola esta vacio significa que se detuvo la lectura de datos, por lo que la orden seria de iniciar
        if cola.empty():
            comando = input('Introduzca ''Inicio'' para comenzar la lectura: \n')
            if comando == 'Inicio':
                # se llena la cola
                cola.put(True)      
                # y se reinicia el hilo secundario para que vuelva a leer (cuando se vacia la cola el hilo termina)
                hiloLectura = Thread(target= leerdatos, args=(cola, frecuencia, ), daemon= True)
                hiloLectura.start()
            else:
                print('No se ha reconocido la instrucción')
                
        # si ya hay un item significa que esta leyendo datos del sensor, por lo que la orden seria de parar
        if cola.full():
            comando = input('Introduzca ''Fin'' para finalizar la lectura: \n')
            if comando == 'Fin':
                # se vacia la cola
                cola.get()     
            else:
                print('No se ha reconocido la instrucción')










