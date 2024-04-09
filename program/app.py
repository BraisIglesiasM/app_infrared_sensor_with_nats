

"""--------------------IMPORTS--------------------"""
# python libraries
from queue import Queue
import asyncio
import aioconsole
import logging

# project modules
from comms import inic_coms



"""--------------------TERMINAL MANAGEMENT--------------------"""

"""it was decided to use an independent task for terminal management, concurrent 
to the messaging ones, in order to be able to listen to text entries at any time, 
regardless of the status of reading or publishing."""
async def terminal(read_queue:Queue, frec:int) -> None:
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
                    logging.info('service resumed')
                    # now that the queue is full, other tasks know reading is resumed
                    read_queue.put(True)  
                    asyncio.get_event_loop().create_task(
                        inic_coms(read_queue, frec)
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
                    print('Entered text not recognized')




"""--------------------APLICATION--------------------"""


async def app(sensor_type:str = 'real', frec:int = 2, mockup_min:int = 0, 
            mockup_max:int = 100) -> None:
    """The function is the core of the application. It processes the startup, 
    creates the logging and Queue objects and starts the main async concurrent 
    tasks: the terminal management and the communication ones"""

    # prints for debuging purposes. May be removed after
    print(sensor_type)
    print(frec)
    print(f'{mockup_min} - {mockup_max}')

    # it was decided to register info messages in logging, 
    # to keep track of start and stop orders
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='logging.log', encoding='utf-8', level=logging.INFO, 
                        format='%(levelname)s:%(asctime)s -> %(message)s')
    logging.info('service launched')


    """object of class Queue to communicate between threads the Resume and the 
    end of the reading. when in the read_queue there is an object (it is the 
    maximum capacity) the .full method will be true, so that adding (.put) and 
    removing (.get) from the read_queue, depending on the commands that are sent 
    from the terminal, the thread where the reading takes place knows whether 
    it has to read or not"""
    read_queue = Queue(1)
    read_queue.put(True)

    try:
        await asyncio.gather(terminal(read_queue, frec), inic_coms(read_queue, frec))
    except KeyboardInterrupt:
        quit()

