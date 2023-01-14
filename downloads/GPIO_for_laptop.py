# import RPi.GPIO as GPIO
import sys, socket, select, random, os
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
        
        # read config file
        file = self.getPath("config.cfg")
        self.config = ConfigParser()
        self.config.read(file)

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
        
            sleep(5)

    def getPath(self,fileName):
        path = os.path.dirname(os.path.realpath(__file__))
        
        return '/'.join([path, fileName])


    def print_barcode(self,barcode):
        
        vid = int( self.config['PRINTER']['VID'], 16 )
        pid = int( self.config['PRINTER']['PID'], 16 )
        in_ep = int( self.config['PRINTER']['IN'], 16 )
        out_ep = int( self.config['PRINTER']['OUT'], 16 )
        location = self.config['ID']['LOKASI']
        company = self.config['ID']['PERUSAHAAN']
        gate_num = self.config['POSISI']['PINTU']
        gate_name = self.config['POSISI']['NAMA']
        vehicle_type = self.config['POSISI']['KENDARAAN']
        footer1 = self.config['KARCIS']['FOOTER1']
        footer2 = self.config['KARCIS']['FOOTER2']
        footer3 = self.config['KARCIS']['FOOTER3']
        footer4 = self.config['KARCIS']['FOOTER4']

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
                            message = socks.recv(1024)
                            message = message.decode("utf-8")

                            if message == "rfid-true":
                                print("open Gate Utk Karyawan")

                            elif message == "rfid-false":
                                print("RFID not match !")

                            elif message == "printer-true":
                                print("print struct here ...")
                                
                                self.print_barcode(self.barcode)
                                
                                print("BUTTON ON (Printing Ticket)")
                    
                                print("RELAY OFF")

                        except Exception as e:
                            print("error:", str(e))



obj = GPIOHandler()
