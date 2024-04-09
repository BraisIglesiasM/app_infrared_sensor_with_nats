
"""--------------------IMPORTS--------------------"""
# python libraries
import asyncio
from queue import Queue

# project modules
from reading import read_data
from publishing import publish_data


async def inic_coms(read_queue:Queue, frec:int) -> None:
    """This task runs as long as the service is not paused through 
    the terminal with a stop command. It manages the reading of the
    sensor data and then publish the read data. When an stop command
    is given, this task ends. it can be thrown again with an start
    command"""

    while read_queue.full():
    
        data = asyncio.get_event_loop().create_task(read_data())
        await data
        await asyncio.get_event_loop().create_task(publish_data(data.result()))
        await asyncio.sleep(frec)
    

