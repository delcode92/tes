import RPi.GPIO as GPIO
import sys, socket
from time import sleep
from datetime import datetime


def run_GPIO(socket):
    
    led1, led2, led3, gate = 8,10,11,18
    loop1, loop2, button = 12,13,7

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(loop1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(loop2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(led1, GPIO.OUT)
    GPIO.setup(led2, GPIO.OUT)
    GPIO.setup(led3, GPIO.OUT)
    GPIO.setup(gate, GPIO.OUT)
    stateLoop1, stateLoop2, stateButton, stateGate = False, False, False, False

    while True:
        if GPIO.input(loop1) == GPIO.LOW and not stateLoop1:
            print("LOOP 1 ON (Vehicle Incoming)")
            stateLoop1 = True
            GPIO.output(led1,GPIO.HIGH)
            
        elif GPIO.input(loop1) == GPIO.HIGH and stateLoop1:  
            print("LOOP 1 OFF (Vehicle Start Moving)")
            stateLoop1 = False
            stateGate = False
            GPIO.output(led1,GPIO.LOW)
            
        if GPIO.input(button) == GPIO.LOW and GPIO.input(loop1) == GPIO.LOW and not stateButton and not stateGate:
            
            # send datetime to server
            time_now = datetime.now().strftime("%d%m%Y%H%M%S%f")
            socket.sendall( bytes(time_now, 'utf-8') )
            print("BUTTON ON (Printing Ticket)")
            
            stateButton = True
            stateGate = True
            GPIO.output(led2,GPIO.HIGH)
            print("RELAY ON (Gate Open)")
            GPIO.output(gate,GPIO.HIGH)
            sleep(1)
            GPIO.output(gate,GPIO.LOW)
            print("RELAY OFF")
            
        elif GPIO.input(button) == GPIO.HIGH and GPIO.input(loop1) == GPIO.LOW and stateButton:
            print("BUTTON OFF")
            stateButton = False
            GPIO.output(led2,GPIO.LOW)
                            
        if GPIO.input(loop2) == GPIO.LOW and not stateLoop2:
            print("LOOP 2 ON (Vehicle Moving In)")
            stateLoop2 = True
            
        elif GPIO.input(loop2) == GPIO.HIGH and stateLoop2:
            print("LOOP 2 OFF (Vehicle In)")
            print(".........(Gate Close)")
            stateLoop2 = False 
            stateGate = False
                                    
        sleep(0.5)

# buat koneksi socket utk GPIO 
try:
    host = sys.argv[1]
    port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((host, port))

    s.sendall( bytes(f"GPIO handshake from {host}:{port}", 'utf-8') )
    print("GPIO handshake success")

    run_GPIO(s)
except:
    print("GPIO handshake fail")

