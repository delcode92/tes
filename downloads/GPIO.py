import RPi.GPIO as GPIO
import sys, socket, select
from time import sleep
from datetime import datetime
from _thread import start_new_thread

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

        print("GPIO.input(button)", GPIO.input(button))
        print("GPIO.LOW", GPIO.LOW)
        print("GPIO.input(loop1)", GPIO.input(loop1))
        print("stateButton", stateButton)
        print("stateGate", stateGate)

        # GPIO.input(button) 1
        # GPIO.LOW 0
        # GPIO.input(loop1) 0
        # stateButton False
        # stateGate False

        # LOOP 1 OFF (Vehicle Start Moving)
        # GPIO.input(button) 1
        # GPIO.LOW 0
        # GPIO.input(loop1) 1
        # stateButton False
        # stateGate False

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


def rfid_input(s, default):
    while True:
        rfid = input("input RFID: ")
        
        if rfid != "":
            # send to server

            try:
                s.sendall( bytes(f"{rfid}", 'utf-8') )
            except:
                print("send RFID to server fail")

def recv_server(s, default):
    while True:
        while True:
 
            # maintains a list of possible input streams
            sockets_list = [sys.stdin, s]
        
            read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
        
            for socks in read_sockets:
                if socks == s:
                    message = socks.recv(2048)
                    print (message)

# buat koneksi socket utk GPIO 
try:
    host = sys.argv[1]
    port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((host, port))

    # sockets_list = [sys.stdin, s]
    # print("socket list: " , sockets_list)

    s.sendall( bytes(f"GPIO handshake from {host}:{port}", 'utf-8') )
    print("GPIO handshake success")

    # stanby data yg dikirim dari server disini
    start_new_thread( recv_server,(s,None) )

    # run inoput RFID thread
    start_new_thread( rfid_input,(s,None) )
    run_GPIO(s)
except:
    print("GPIO handshake fail")

