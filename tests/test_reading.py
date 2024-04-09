
"""--------------------IMPORTS--------------------"""

# python libraries
import unittest
import assertpy
import asyncio
import sys
import os

# project modules
# adding parent directory to path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from program.reading import read_data


class TestReading(unittest.TestCase):

    async def test_reading_correct_format(self):
        data = asyncio.get_event_loop().create_task(
                read_data(address='nats://localhost:4222'))
        await data
        assertpy.assert_that(data.result()).is_instance_of(bytes)

    async def test_reading_incorrect_format(self):
        data = asyncio.get_event_loop().create_task(
                read_data(address='this is not a nats valid address'))
        await data
        assertpy.assert_that(data.result()).is_instance_of(None)


