# from gpio_config import *
import sys
from time import sleep
from client_service import Client

# run/connect client socket here first
client = Client(sys.argv[1], int(sys.argv[2]))

# while True:
#     inp = input()

#     # call client service --> check rfid --> return true/false
#     res = client.get_data( inp+"#rfid" )

#     # print(res)
#     print(res.decode("utf-8"))

#     if(res.decode("utf-8") == "true"):
#         GPIO.output(gate,GPIO.HIGH)
#         sleep(1)
#         GPIO.output(gate,GPIO.LOW)

