# app_infrared_sensor_with_nats

## Hello there 👋


## PROBLEM AND OBJECTIVES

this repository contains a project made in python for the reading of an infrared sensor, which is not available at the moment. 
It is assumed that this sensor can be read using NATS request-reply protocols. So, to obtain a reading, a request is 
launched under a specific subject, to which the sensor responds with a list in byte format (python b strings) of 64 words (16bits).

The objective is to create a backend application that reads data from the sensor every two seconds and publishes it.

The following restrictions have been considered for the realization of the project:  

-at the moment of launching the application, it will be possible to configure by console the data reading period of the sensor, specify if it is a real sensor or a mockup and, in this case, a range of minimum and maximum values for data generation.
-communication will be via NATS messenger service. (https://nats.io/)
-data capture can be stopped and resumed at any time


## DEVELOPMENT

Considerations: the 'data capture can be stopped and resumed' was proposed to be solved using CLI (terminal) inputs. This project was made using Python3 with
VSCode on a windows 10 OS. Libraries aside the python standard library used are nats.py, assertpy and aioconsole.     

This project uses git as version control to keep track of the project versions. Each commit works properly according to its description. Only manual tests have been made 
for each version but the last one, where unit tests were also conducted. Until V0.0.3 (not included) code comments are in spanish. this was
changed on V0.0.3 to comply with PEP 8 Style Guide (https://peps.python.org/pep-0008/)

Project progress history (ordered by commits):

- V0.0.0: only contains a readme and a .gitignore
- V0.0.1: first aproach to a application that attends terminal inputs while running another task(s). Succesfully made using python threads and Queues
- V0.0.2: the use of threads is replaced by the asyncio library, on which nats.py is based. 
- V0.0.3: Initial tests with nats. Used only to publish data (publish.py). A nats server has been launched to make sure a client can receive the posted messages. a logging is created. Function inic_comms from module comms is made to group reading and posting tasks. Function hints are now more detailed
- V0.1.0: first version to meet the objective. reading.py is now available (for a supposed real or mockup sensor). publishing.py is modified to post read data. use of logging extended. A config file (main.cfg) is created to easily edit nats addresses and use them globally. Unit tests are also made. a class (Sensor) has been written so that, in the future, it will be easier to read several sensors simultaneously without repeating code, although some changes would need to be made to the code in that case


Feel free to clone the repository and navigate through the commits to see code and changes with more detail (or even run it with a nats-server!)


## RESULTS  


A nats server has been locally deployed to ensure that data is published correctly. Also, a script was made to simulate a sensor, which listens requests and 
replys as (allegedly) the real sensor would. This sort of manual end-to-end test was made the application works as expected 


## POSSIBLE FUTURE IMPLEMENTATIONS 


* Read data can be stored in a database so that they are not lost in case there are no customers receiving the publications.
* Optimize the Sensor class to use generators instead of lists (for memory optimizing)
* Include more unit tests and some end-to-end tests for more code coverage
* Improve the variable names used to make code as clear as possible. 



## Hola 👋


## PROBLEMA Y OBJETIVOS 

este repositorio contiene un proyecto realizado en python para la lectura de un sensor de infrarrojos del que, por el momento, no se dispone. 
Para el proyecto se presupone que este sensor puede ser leído utilizando protocolos NATS de request-reply. Así, para obtener una lectura, se lanza 
una petición bajo un tema concreto, a la que el sensor responde con una lista en formato bytes (b strings de python) de 64 palabras (16bits).

El objetivo es crear una aplicación backend que lea los datos del sensor cada dos segundos y los publique.

Para la realización del proyecto se han considerado las siguientes restricciones:  

-en el momento de lanzar la aplicación, se podrá configurar por consola el periodo de lectura de datos del sensor, especificar si se trata de un sensor real o de uno mockup y, en este caso, un rango de valores mínimos y máximos para la generación de datos.
-La comunicación se realizará a través del servicio de mensajería NATS. (https://nats.io/)
-la captura de datos puede detenerse y reanudarse en cualquier momento


## DESARROLLO 

Consideraciones: para "la captura de datos se puede detener y reanudar" se propuso resolverlo usando entradas por CLI (línea de comandos en consola). Este 
proyecto se realizó utilizando Python3 con VSCode en un sistema operativo windows 10. Las librerías, aparte de la librería estándar de python, utilizadas son nats.py, assertpy y aioconsole.     

Este proyecto utiliza git como sistema de control de versiones para mantener un registro de las versiones del proyecto. Cada commit funciona correctamente según lo descrito en su descripción. 
Sólo se han hecho tests manuales para cada versión excepto para la última, en la que también se realizaron test unitarios. Hasta la V0.0.3 (no incluida) los comentarios del código están en castellano. 
esto se cambió en la V0.0.3 para cumplir con la Guía de Estilos PEP 8 (https://peps.python.org/pep-0008/)

Historial de progreso del proyecto (ordenado por commits):

* V0.0.0: sólo contiene un readme y un .gitignore
* V0.0.1: primera aproximación a una aplicación que atiende inputs de consola mientras ejecuta otra(s) tarea(s). Realizado con éxito usando python threads y Queues
* V0.0.2: se sustituye el uso de hilos por la librería asyncio, en la que se basa nats.py. 
* V0.0.3: Pruebas iniciales con nats. Se utiliza sólo para publicar datos (publish.py). Se ha probado en conjunto con un servidor nats para asegurarse de que un cliente puede recibir correctamente los mensajes publicados. Se ha creado un logging. La función inic_comms() del módulo comms se hace para agrupar tareas de lectura y publicación de datos. Las hints de las funciones son ahora más detalladas
* V0.1.0: primera versión que cumple el objetivo. reading.py ya está disponible (para un supuesto sensor real o mockup). publishing.py se modifica para publicar los datos leídos del sensor. uso del logging ampliado. Se crea un fichero de configuración (main.cfg) para editar fácilmente las direcciones NATS y usarlas globalmente. También se realizan pruebas unitarias. se escribe una clase (Sensor) para que, en el futuro, sea más fácil leer varios sensores simultáneamente sin repetir código, aunque en ese caso habría que hacer algunas adaptaciones en el código

Siéntete libre de clonar el repositorio y navegar por los commits para ver el código y los cambios con más detalle (e incluso ejecutarlo junto a nats-server!)


## RESULTADOS

Se ha desplegado localmente un servidor nats para garantizar que los datos se publican correctamente. Además, se ha realizado un script para simular un sensor, que escucha las peticiones y responde como (supuestamente) lo haría el sensor real. Esta especie de test de extremo a extremo manual se hizo para comprobar que la aplicación funciona como se esperaba 


## POSIBLES IMPLEMENTACIONES FUTURAS


* Los datos leídos se pueden guardar en una base de datos para que no se pierdan en caso de que no haya clientes que reciban las publicaciones.
* Optimizar la clase Sensor para usar generadores en lugar de listas (para optimizar el uso de memoria).
* Incluir más tests unitarios y algunos tests de extremo a extremo para una mayor cobertura del código
* Mejorar los nombres de las variables utilizadas para que el código sea lo más claro posible. 

____________________________________________________________________________________



