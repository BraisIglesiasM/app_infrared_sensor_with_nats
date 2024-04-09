
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
                        help='Enter the sensor type (real | mockup) (str)')
    # the frecuency argument is an int, although it could be changed to float if needed
    parser.add_argument('--frec', type=int, required=True, 
                        help='Enter the reading frequency (seconds) (int)')
    parser.add_argument('--min_range', type=int, required=False, 
                        help='Enter minimum for generated values in case of mockup sensor (int)')
    parser.add_argument('--max_range', type=int, required=False, 
                        help='Enter maximum for generated values in case of mockup sensor (int)')

    args = parser.parse_args()

    asyncio.run(app(sensor_type=args.sensor, frec=args.frec, 
                        mockup_min=args.min_range, mockup_max=args.max_range))

    # launch example: $python main.py --sensor mockup --frec 2 --min_range 0 --max_range 65535
    # launch example: $python main.py --sensor real --frec 2 --min_range 10 --max_range 50
