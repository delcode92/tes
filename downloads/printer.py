import os
from escpos.printer import Usb
from datetime import datetime
from configparser import ConfigParser


def getPath(fileName):
    path = os.path.dirname(os.path.realpath(__file__))
    
    return '/'.join([path, fileName])

file = getPath("config.cfg")
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

def ticket(barcode):
    
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
    p.text("\n------------------------------------\n")
    p.text(footer1 + "\n")
    p.text(footer2 + "\n")
    p.text(footer3 + "\n")
    p.text(footer4 + "\n")

    # Cut paper
    p.cut()
    p.close()

ticket("1234567890")
    