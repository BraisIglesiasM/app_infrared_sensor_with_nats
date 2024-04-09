
"""--------------------IMPORTS--------------------"""
# python libraries
import random
import asyncio
import logging

# nats
from nats.aio.client import Client as NATS


"""--------------------LECTURA SENSOR--------------------"""

async def read_data(address:str) -> bytes | None:
    """function that reads the actual sensor. for the development, it was 
    assumed that the sensor can communicate via nats messaging, replying 
    via the request-reply protocol, under the subject sensor_reading with a list of 64 words in b string format."""

    nc = NATS()

    await nc.connect(servers=[address])

    # Send the request
    try:
        msg = await nc.request("sensor_reading", b'', timeout=1)
        # Use the response
        read_data = msg.data
        # [end request_reply]
        await nc.close()
        return read_data
    
    except asyncio.TimeoutError:
        logging.exception('Communication with sensor failed')
        await nc.close()
        return None


    
