
"""--------------------IMPORTS--------------------"""
# python libraries
import random


"""--------------------LECTURA SENSOR--------------------"""

async def read_data() -> list:
    """generates random temp data at the moment to test publishing"""

    data = [random.random()*10, random.random()*10, random.random()*10]
    print(f'leyendo: {data}')

    return data

    
