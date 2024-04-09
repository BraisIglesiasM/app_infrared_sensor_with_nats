
"""--------------------IMPORTS--------------------"""
# python libraries
import asyncio
from queue import Queue
import random

# project modules
from reading import read_data
from publishing import publish_data


"""--------------------COMMUNICATIONS TASK--------------------"""

async def inic_comms(read_queue:Queue, frec:int, addresses:dict, is_mockup:bool, 
                    mockup_min:int = 0, mockup_max:int = 65535) -> None:
    """This task runs as long as the service is not paused through 
    the terminal with a stop command. It manages the reading of the
    sensor data and then publish the read data. if the sensor type is 
    mockup, them the data is randomly generated. When an stop command
    is given, this task ends. it can be thrown again with an start
    command"""

    while read_queue.full():

        if is_mockup:
            """the mockup data is created with a generator that changes 
            a random number in the rangeof the min-max arguments to binary 
            and then encoded to a bytes class object (b string)"""
            to_publish_data = str(["{0:b}".format(random.randrange(mockup_min,mockup_max,1)) 
                                for i in range(64)]).encode()
        else:
            data = asyncio.get_event_loop().create_task(
                read_data(address=addresses['Sensor1'][0]))
            await data
            if data.result() is None:
                to_publish_data = None
            else:
                to_publish_data = data.result()

        
        await asyncio.get_event_loop().create_task(
            publish_data(data_sensor=to_publish_data, address=addresses['Sensor1'][1]))
        await asyncio.sleep(frec)
    

