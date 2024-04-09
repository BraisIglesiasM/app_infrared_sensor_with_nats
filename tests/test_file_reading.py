
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

from program.app import cfg_file_reading


class TestFileReading(unittest.TestCase):

    async def test_reading_file_correct_format(self):

        addresses_async = asyncio.get_event_loop().create_task(cfg_file_reading())
        await addresses_async
        assertpy.assert_that(addresses_async.result()).is_instance_of(dict)

    async def test_reading_file_correct_reading_address(self):
        addresses_async = asyncio.get_event_loop().create_task(cfg_file_reading())
        await addresses_async
        assertpy.assert_that(addresses_async.result()['Sensor1'][0]).is_instance_of(str)

    async def test_reading_file_correct_publishing_address(self):
        addresses_async = asyncio.get_event_loop().create_task(cfg_file_reading())
        await addresses_async
        assertpy.assert_that(addresses_async.result()['Sensor1'][1]).is_instance_of(str)


