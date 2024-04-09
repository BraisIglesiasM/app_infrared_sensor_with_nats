
"""--------------------IMPORTS--------------------"""
# python libraries
import argparse
import asyncio

# project modules
from app import app



"""--------------------MAIN--------------------"""

if __name__ == '__main__':

    # the argparse library is used in order to be able to use control arguments at launch
    # these arguments will be: type of sensor (real or mocked), reading frequency and mockup range

    parser = argparse.ArgumentParser(description='App')
    parser.add_argument('--sensor', type= str, required=True, 
                        help='Enter the sensor type (real | mockup)')
    parser.add_argument('--frec', type=int, required=True, 
                        help='Enter the reading frequency (seconds)')
    parser.add_argument('--min_range', type=int, required=False, 
                        help='Enter minimum for generated values in case of mockup sensor')
    parser.add_argument('--max_range', type=int, required=False, 
                        help='Enter maximum for generated values in case of mockup sensor')

    args = parser.parse_args()

    asyncio.run(app(args.sensor, args.frec, args.min_range, args.max_range))