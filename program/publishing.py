

"""--------------------IMPORTS--------------------"""
# python libraries
import asyncio
import logging

# nats
import nats


"""--------------------PUBLICACION data SENSOR--------------------"""

async def publish_data(data_sensor:bytes|None, address:str) -> None:
    """Publish read data (if not none) through nats to a specific subject
    (data_sensor in this case) so that any interested client can 
    get notified """

    if data_sensor is not None:

        nc = await nats.connect(servers=[address])

        try:
            await nc.publish("data_sensor", data_sensor)
        except asyncio.TimeoutError as e:
            logging.exception(f'data publishing failed: {e}')

        await nc.close()



