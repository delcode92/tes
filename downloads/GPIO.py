import RPi.GPIO as GPIO
import sys, socket, select, os
from time import sleep
from datetime import datetime
from _thread import start_new_thread
from escpos.printer import Usb
from configparser import ConfigParser


class GPIOHandler:
    def __init__(self) -> None:
        # global variable
        self.led1, self.led2, self.led3, self.gate = 8,10,11,18
        self.loop1, self.loop2, self.button = 12,13,7

        self.stateLoop1, self.stateLoop2, self.stateButton, self.stateGate = False, False, False, False
        

        # buat koneksi socket utk GPIO
        host = sys.argv[1]
        port = int(sys.argv[2])
        
        while True:

            try:
                self.s.sendall( bytes(f"client({host}) connected", 'utf-8') )
            except:
                print("GPIO handshake fail")

                try:
                    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    self.s.connect((host, port))

                    # sockets_list = [sys.stdin, s]
                    # print("socket list: " , sockets_list)

                    self.s.sendall( bytes(f"GPIO handshake from {host}:{port}", 'utf-8') )
                    print("GPIO handshake success")

                    # stanby data yg dikirim dari server disini
                    start_new_thread( self.recv_server,() )

                    # run input RFID thread
                    start_new_thread( self.rfid_input,() )
                    self.run_GPIO()
                except:
                    print("GPIO handshake fail")
        

    def getPath(self,fileName):
        path = os.path.dirname(os.path.realpath(__file__))
        
        return '/'.join([path, fileName])


    def print_barcode(self,barcode):
        file = self.getPath("config.cfg")
        config = ConfigParser()
        config.read(file)

        vid = int(config['PRINTER']['VID'], 16)
        pid = int(config['PRINTER']['PID'], 16)
        in_ep = int(config['PRINTER']['IN'], 16)
        out_ep = int(config['PRINTER']['OUT'], 16)
        location = config['ID']['LOKASI']
        company = config['ID']['PERUSAHAAN']
        gate_num = config['POSISI']['PINTU']
        gate_name = config['POSISI']['NAMA']
        vehicle_type = config['POSISI']['KENDARAAN']
        footer1 = config['KARCIS']['FOOTER1']
        footer2 = config['KARCIS']['FOOTER2']
        footer3 = config['KARCIS']['FOOTER3']
        footer4 = config['KARCIS']['FOOTER4']

        new_time_text = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        p = Usb(vid, pid , timeout = 0, in_ep = in_ep, out_ep = out_ep)
        # Print text
        p.set('center')
        p.text(location + "\n")
        p.text(company + "\n")
        p.text("------------------------------------\n\n")
        
        p.text(gate_name + " " + gate_num + "\n")
        p.text(vehicle_type + "\n")
        p.text(new_time_text + "\n\n")
        
        p.barcode("{B" + barcode, "CODE128", height=128, width=3, function_type="B")
        # p.qr("test", size=5)
        # p.barcode('1324354657687', 'EAN13', 64, 3, '', '')

        p.text("\n------------------------------------\n")
        p.text(footer1 + "\n")
        p.text(footer2 + "\n")
        p.text(footer3 + "\n")
        p.text(footer4 + "\n")

        # Cut paper
        p.cut()
        p.close()

    def run_GPIO(self):
        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.loop1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.loop2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.led1, GPIO.OUT)
        GPIO.setup(self.led2, GPIO.OUT)
        GPIO.setup(self.led3, GPIO.OUT)
        GPIO.setup(self.gate, GPIO.OUT)
        
        while True:
            if GPIO.input(self.loop1) == GPIO.LOW and not self.stateLoop1:
                print("LOOP 1 ON (Vehicle Incoming)")
                self.stateLoop1 = True
                GPIO.output(self.led1,GPIO.HIGH)
                
            elif GPIO.input(self.loop1) == GPIO.HIGH and self.stateLoop1:  
                print("LOOP 1 OFF (Vehicle Start Moving)")
                self.stateLoop1 = False
                self.stateGate = False
                GPIO.output(self.led1,GPIO.LOW)

            # print("GPIO.input(button)", GPIO.input(button))
            # print("GPIO.LOW", GPIO.LOW)
            # print("GPIO.input(loop1)", GPIO.input(loop1))
            # print("stateButton", stateButton)
            # print("stateGate", stateGate)

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

            if GPIO.input(self.button) == GPIO.LOW and GPIO.input(self.loop1) == GPIO.LOW and not self.stateButton and not self.stateGate:
                
                # send datetime to server
                time_now = datetime.now().strftime("%d%m%Y%H%M%S%f")
                self.s.sendall( bytes(f'datetime#{time_now}', 'utf-8') )
                
                # get return from server

                
                # print("self.button ON (Printing Ticket)")
                
                # self.stateButton = True
                # stateGate = True
                # GPIO.output(led2,GPIO.HIGH)
                # print("RELAY ON (Gate Open)")
                # GPIO.output(gate,GPIO.HIGH)
                # sleep(1)
                # GPIO.output(gate,GPIO.LOW)
                # print("RELAY OFF")
                
            elif GPIO.input(self.button) == GPIO.HIGH and GPIO.input(self.loop1) == GPIO.LOW and self.stateButton:
                print("BUTTON OFF")
                self.stateButton = False
                GPIO.output(self.led2,GPIO.LOW)
                                
            if GPIO.input(self.loop2) == GPIO.LOW and not self.stateLoop2:
                print("LOOP 2 ON (Vehicle Moving In)")
                self.stateLoop2 = True
                
            elif GPIO.input(self.loop2) == GPIO.HIGH and self.stateLoop2:
                print("LOOP 2 OFF (Vehicle In)")
                print(".........(Gate Close)")
                self.stateLoop2 = False 
                self.stateGate = False
                                        
            sleep(0.5)

    def rfid_input(self):
        while True:
            rfid = input("input RFID: ")
            
            if rfid != "":
                # send to server

                try:
                    self.s.sendall( bytes(f"rfid#{rfid}", 'utf-8') )
                except:
                    print("send RFID to server fail")

    def recv_server(self):
        while True:
            while True:
    
                # maintains a list of possible input streams
                sockets_list = [sys.stdin, self.s]
            
                read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
            
                for socks in read_sockets:
                    if socks == self.s:
                        try:
                            message = socks.recv(2048)
                            message = message.decode("utf-8")

                            if message == "rfid-true":
                                print("open Gate Utk Karyawan")
                            elif message == "rfid-false":
                                print("RFID not match !")

                            elif message == "printer-true":
                                print("print struct here ...")

                                print("BUTTON ON (Printing Ticket)")
                    
                                self.stateButton = True
                                self.stateGate = True
                                GPIO.output(self.led2,GPIO.HIGH)
                                print("RELAY ON (Gate Open)")
                                GPIO.output(self.gate,GPIO.HIGH)
                                sleep(1)
                                GPIO.output(self.gate,GPIO.LOW)
                                print("RELAY OFF")
                        except:
                            print("Server not connected ...")



obj = GPIOHandler()
