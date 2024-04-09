

"""--------------------IMPORTS--------------------"""
# python libraries
import os
import json

# nats
import nats


"""--------------------DATA SENSOR PUBLISHING--------------------"""

async def publish_data(data_sensor) -> None:
    """Publish read data (if any) through nats to a specific subject
    (data_sensor in this case) so that any interested client can 
    get notified """

    servers = os.environ.get("NATS_URL", "nats://localhost:4222").split(",")
    nc = await nats.connect(servers=servers)
    await nc.publish('data_sensor', json.dumps(data_sensor).encode())
    await nc.close()

    # print for debuging purposes
    print(f'publicacion: {data_sensor}')


