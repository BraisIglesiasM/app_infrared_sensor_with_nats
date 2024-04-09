

"""--------------------IMPORTS--------------------"""
# python libraries
from queue import Queue
import asyncio
import logging
import os
import configparser

# nats
import nats

# other 
import aioconsole

# project modules
from comms import inic_comms



"""--------------------CFG FILE--------------------"""

async def cfg_file_reading() -> dict:
    """This function reads the config file where the messaging (nats) addresses
    are stored, for an easy fast edit. This file also makes the project more easily 
    expandable If theres no .cfg file (critical message in logging), just create one
    plain text file on the program root with the main.cfg name. example:
    ________________________________________
    [Sensor1]
    Read_address = nats://localhost:4222
    Publish_address = nats://localhost:4222
    ________________________________________
    the return type us a dictionary of sensors where the values are a list of two
    strings, the read address and the publishing address. example:
    {'Sensor1':['nats://localhost:4222', 'nats://localhost:4222']}

    this function can be expanded to read data from more than one sensor if needed
    as a for loop would be easily implemented
    """

    file = '../main.cfg'

    if not os.path.isfile(file):
            logging.critical('Cant open cfg file. Please make sure it is not deleted')
            quit()

    CP = configparser.ConfigParser(allow_no_value=True)
    CP.optionxform = str #Para que sea sensible a Mays/Mins 
    
    CP.read(file)

    try:
        read_address = CP.get('Sensor1', 'Read_address')
        publish_address = CP.get('Sensor1', 'Publish_address')
    except configparser.NoSectionError:
        logging.critical(
            'Problem with cfg file sections. Please make sure the section names are SensorX')
        quit()
    except configparser.NoOptionError:
        logging.critical(
            'Problem with cfg file options. Please make sure the section have Read_address and Publish_address')
        quit()
    except configparser.Error:
        logging.critical(
            'Cfg file reading failed, please make sure the format is correct')
    
    return {'Sensor1':[str(read_address), str(publish_address)]}


"""--------------------TERMINAL MANAGEMENT--------------------"""

"""it was decided to use an independent task for terminal management, concurrent 
to the messaging ones, in order to be able to listen to text entries at any time, 
regardless of the status of reading or publishing."""
async def terminal(read_queue:Queue, frec:int, addresses:dict, is_mockup:bool, 
                mockup_min:int = 0, mockup_max:int = 65535) -> None:
        """This function runs on an infinite loop, waiting for terminal commands 
        to pause-resume the reading (and publishing). The Queue object will be 
        full when reading is started and empty otherwise"""
        
        while True:

            if read_queue.empty():
                # aioconsole input is used in this case instead of python input 
                # to avoid an input wait in the whole python thread, killing concurrency
                terminal_input = await aioconsole.ainput(
                    'Please enter ''Resume'' to start reading: \n')
                if terminal_input == 'Resume':
                    # now that the queue is full, other tasks know reading is resumed
                    logging.info('service resumed')
                    read_queue.put(True)  
                    asyncio.get_event_loop().create_task(
                        inic_comms(read_queue=read_queue, frec=frec, addresses=addresses, 
                                is_mockup=is_mockup,mockup_min=mockup_min, mockup_max=mockup_max
                        )
                    )
                else:
                    print('Entered text not recognized')
                    
            # if queue is already full, reading is active, so the only 
            # admissible input would be stop
            if read_queue.full():
                terminal_input = await aioconsole.ainput(
                    'Please enter ''Stop'' to pause reading: \n')
                if terminal_input == 'Stop':
                    logging.info('service stopped')
                    # with the queue empty, the comm services will stop
                    read_queue.get()     
                else:
                    print('No se ha reconocido la instrucción')





"""--------------------APLICACION--------------------"""

async def app(sensor_type: str= 'real', frec: int= 2, mockup_min: int= 0, 
            mockup_max:int = 65535) -> None:
    """The function is the core of the application. It processes the startup, 
    creates the logging and Queue objects and starts the main async concurrent 
    tasks: the terminal management and the communication ones"""

    # prints for debuging purposes. May be removed after
    print(sensor_type)
    print(frec)
    print(f'{mockup_min} - {mockup_max}')

    # checking values for sensor type
    if sensor_type.upper() != 'MOCKUP':
        sensor_type = 'real'
    
    # checking values for sensor frecuency: as it was thought as an integer,
    # its minimum value will be 1
    if type(frec) is not int:
        frec = 2
    elif frec < 1:
        frec = 1

    # checking values for mockup_min
    if type(mockup_min) is not int:
        mockup_min = 0
    elif mockup_min < 0:
        mockup_min = 0

    # checking values for mockup_max
    if type(mockup_max) is not int:
        mockup_max = 0
    elif mockup_max < 0:
        mockup_max = 65535

    # if they are not coherent, they will be set to default
    if mockup_min > mockup_max:
        mockup_min = 0
        mockup_max = 65535
    

    # it was decided to register info messages in logging, 
    # to keep track of start and stop orders
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='logging.log', encoding='utf-8', level=logging.INFO, 
                        format='%(levelname)s:%(asctime)s -> %(message)s')
    logging.info('service launched')

    # config fil reading for getting the reading and publishing addresses 
    addresses_async = asyncio.get_event_loop().create_task(cfg_file_reading())
    await addresses_async
    # addresses = cfg_file_reading()
    # await addresses.

    addresses = addresses_async.result()

    """sensor type check. This ckeck was made to change the string argument to a bool,
    to improve readbility in the functions where its used. not case sensitive.
    if any other text aside from mockup is entered, sensor type will be real.
    another option would be to check if real and raise an exception if something else
    is entered"""
    sensor_mockup = False
    if sensor_type.upper() == 'MOCKUP':
        sensor_mockup = True

    """object of class Queue to communicate between threads the Resume and the 
    end of the reading. when in the read_queue there is an object (it is the 
    maximum capacity) the .full method will be true, so that adding (.put) and 
    removing (.get) from the read_queue, depending on the commands that are sent 
    from the terminal, the thread where the reading takes place knows whether 
    it has to read or not"""
    read_queue = Queue(1)
    # its set full from the very beginning so the app starts reading automatically
    read_queue.put(True)

    try:
        await asyncio.gather(
            terminal(read_queue=read_queue, frec= frec, addresses=addresses, 
                    is_mockup=sensor_mockup, mockup_min=mockup_min, mockup_max=mockup_max), 
            inic_comms(read_queue=read_queue, frec=frec, addresses=addresses, 
                    is_mockup=sensor_mockup, mockup_min=mockup_min, mockup_max=mockup_max)
            )
    except KeyboardInterrupt:
        quit()

