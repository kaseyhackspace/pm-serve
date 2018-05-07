'''
Gateway script that receives sensor data from mesh
and sends it to pm-serve
'''

import serial
import sys
import json
import requests

def main(args):
    print(args)
    ser = serial.Serial('/dev/ttyUSB0', 115200)
    while True:
        bstr = ser.readline()
        str = bstr.decode('utf-8')
        data = json.loads(str)
        print(data['density'])
        r = requests.post("https://dc8c5fe4.ngrok.io/sensors/data/add", data=data)
        print(r.text)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
