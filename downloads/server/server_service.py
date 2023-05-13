import os,sys, re, socket, psycopg2, logging, datetime, json, multiprocessing
import typing
from PyQt5.QtCore import QObject
from time import sleep
from cv2 import add
from _thread import start_new_thread
from framework import *
from configparser import ConfigParser
import copy

class Debug():
    
    def __init__(self) -> None:
        
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.NOTSET)
        self.logfile_path = "./logging/log_file.log"

        # our first handler is a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler_format = '%(levelname)s: %(message)s'
        console_handler.setFormatter(logging.Formatter(console_handler_format))

        # start logging and show messages

        # the second handler is a file handler
        file_handler = logging.FileHandler(self.logfile_path)
        file_handler.setLevel(logging.INFO)
        file_handler_format = '%(asctime)s | %(levelname)s | %(lineno)d: %(message)s'
        file_handler.setFormatter(logging.Formatter(file_handler_format))

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

# class worker
class Thread(QThread):

    changePixmaps = pyqtSignal(QImage)
    
    def run(self):
        
        debug = Debug()
        
        debug.logger.info("Run IP Cam 1 Thread ...")

        self.is_running = True
        self.capture = None
        
        while self.is_running:
            
            try:

                if not self.capture:
                    rtsp = IPCam.list_ip[0]        
                    # rtsp = f'rtsp://admin:admin@{IPCam.list_ip[0]}'        
                    debug.logger.info("Run video capture from --> "+ rtsp)
                    self.capture = cv2.VideoCapture(rtsp)
                    
                elif not ret:
                    debug.logger.error("Failed to read from video stream!")
                    raise Exception("Failed to read from video stream!")   
                
                ret, frame = self.capture.read()
                if ret:
                    rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
                    h, w, ch = rgbImage.shape
                    bytesPerLine = ch * w
                    convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                    p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                    self.changePixmaps.emit(p)
            
            except Exception as e:
                self.is_running = False
                self.capture = None
                self.msleep(5000)
                self.is_running = True

                debug.logger.info("something wrong with ipcam 1 .... ")
                debug.logger.error(str(e))
                debug.logger.info("retrying to connect.... ")
        else:
            debug.logger.info("IP CAM 1 not connected ... ")

class Thread2(QThread):

    changePixmaps2 = pyqtSignal(QImage)
    
    def run(self):
        
        debug = Debug()
        
        debug.logger.info("Run IP Cam 2 Thread ...")

        self.is_running = True
        self.capture = None
        
        while self.is_running:
            try:

                if not self.capture:
                    rtsp = IPCam.list_ip[1]            
                    debug.logger.info("Run video capture from --> "+ rtsp)
                    self.capture = cv2.VideoCapture(rtsp)
                    
                elif not ret:
                    debug.logger.error("Failed to read from video stream!")
                    raise Exception("Failed to read from video stream!")   
                
                ret, frame = self.capture.read()
                if ret:
                    rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
                    h, w, ch = rgbImage.shape
                    bytesPerLine = ch * w
                    convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                    p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                    self.changePixmaps2.emit(p)
            
            except Exception as e:
                self.is_running = False
                self.capture = None
                self.msleep(5000)
                self.is_running = True

                debug.logger.info("something wrong with ipcam 2 .... ")
                debug.logger.error(str(e))
                debug.logger.info("retrying to connect.... ")
        else:
            debug.logger.info("IP CAM 2 not connected ... ")

class Thread3(QThread):

    changePixmaps3 = pyqtSignal(QImage)
    
    def run(self):
        
        debug = Debug()
        
        debug.logger.info("Run IP Cam 3 Thread ...")

        self.is_running = True
        self.capture = None
        
        while self.is_running:
            try:

                if not self.capture:
                    rtsp = IPCam.list_ip[2]        
                    debug.logger.info("Run video capture from --> "+ rtsp)
                    self.capture = cv2.VideoCapture(rtsp)
                    
                elif not ret:
                    debug.logger.error("Failed to read from video stream!")
                    raise Exception("Failed to read from video stream!")   
                
                ret, frame = self.capture.read()
                if ret:
                    rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
                    h, w, ch = rgbImage.shape
                    bytesPerLine = ch * w
                    convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                    p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                    self.changePixmaps3.emit(p)
            
            except Exception as e:
                self.is_running = False
                self.capture = None
                self.msleep(5000)
                self.is_running = True

                debug.logger.info("something wrong with ipcam 3 .... ")
                debug.logger.error(str(e))
                debug.logger.info("retrying to connect.... ")
        else:
            debug.logger.info("IP CAM 3 not connected ... ")

class Thread4(QThread):

    changePixmaps4 = pyqtSignal(QImage)
    
    def run(self):
        
        debug = Debug()
        
        debug.logger.info("Run IP Cam 4 Thread ...")

        self.is_running = True
        self.capture = None
        
        while self.is_running:
            try:

                if not self.capture:
                    rtsp = IPCam.list_ip[3]            
                    debug.logger.info("Run video capture from --> "+ rtsp)
                    self.capture = cv2.VideoCapture(rtsp)
                    
                elif not ret:
                    debug.logger.error("Failed to read from video stream!")
                    raise Exception("Failed to read from video stream!")   
                
                ret, frame = self.capture.read()
                if ret:
                    rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
                    h, w, ch = rgbImage.shape
                    bytesPerLine = ch * w
                    convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                    p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                    self.changePixmaps4.emit(p)
            
            except Exception as e:
                self.is_running = False
                self.capture = None
                self.msleep(5000)
                self.is_running = True

                debug.logger.info("something wrong with ipcam 4 .... ")
                debug.logger.error(str(e))
                debug.logger.info("retrying to connect.... ")
        else:
            debug.logger.info("IP CAM 4 not connected ... ")

class Thread5(QThread):

    changePixmaps5 = pyqtSignal(QImage)
    
    def run(self):
        
        debug = Debug()
        
        debug.logger.info("Run IP Cam 5 Thread ...")

        self.is_running = True
        self.capture = None
        
        while self.is_running:
            try:

                if not self.capture:
                    rtsp = IPCam.list_ip[4]        
                    debug.logger.info("Run video capture from --> "+ rtsp)
                    self.capture = cv2.VideoCapture(rtsp)
                    
                elif not ret:
                    debug.logger.error("Failed to read from video stream!")
                    raise Exception("Failed to read from video stream!")   
                
                ret, frame = self.capture.read()
                if ret:
                    rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
                    h, w, ch = rgbImage.shape
                    bytesPerLine = ch * w
                    convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                    p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                    self.changePixmaps5.emit(p)
            
            except Exception as e:
                self.is_running = False
                self.capture = None
                self.msleep(5000)
                self.is_running = True

                debug.logger.info("something wrong with ipcam 5 .... ")
                debug.logger.error(str(e))
                debug.logger.info("retrying to connect.... ")
        else:
            debug.logger.info("IP CAM 5 not connected ... ")

class Thread6(QThread):

    changePixmaps6 = pyqtSignal(QImage)
    
    def run(self):
        
        debug = Debug()
        
        debug.logger.info("Run IP Cam 6 Thread ...")

        self.is_running = True
        self.capture = None
        
        while self.is_running:
            try:

                if not self.capture:
                    rtsp = IPCam.list_ip[5]            
                    debug.logger.info("Run video capture from --> "+ rtsp)
                    self.capture = cv2.VideoCapture(rtsp)
                    
                elif not ret:
                    debug.logger.error("Failed to read from video stream!")
                    raise Exception("Failed to read from video stream!")   
                
                ret, frame = self.capture.read()
                if ret:
                    rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
                    h, w, ch = rgbImage.shape
                    bytesPerLine = ch * w
                    convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                    p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                    self.changePixmaps6.emit(p)
            
            except Exception as e:
                self.is_running = False
                self.capture = None
                self.msleep(5000)
                self.is_running = True

                debug.logger.info("something wrong with ipcam 6 .... ")
                debug.logger.error(str(e))
                debug.logger.info("retrying to connect.... ")
        else:
            debug.logger.info("IP CAM 6 not connected ... ")

class Thread7(QThread):

    changePixmaps7 = pyqtSignal(QImage)
    
    def run(self):
        
        debug = Debug()
        
        debug.logger.info("Run IP Cam 7 Thread ...")

        self.is_running = True
        self.capture = None
        
        while self.is_running:
            try:

                if not self.capture:
                    rtsp = IPCam.list_ip[6]
                    debug.logger.info("Run video capture from --> "+ rtsp)
                    self.capture = cv2.VideoCapture(rtsp)
                    
                elif not ret:
                    debug.logger.error("Failed to read from video stream!")
                    raise Exception("Failed to read from video stream!")   
                
                ret, frame = self.capture.read()
                if ret:
                    rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
                    h, w, ch = rgbImage.shape
                    bytesPerLine = ch * w
                    convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                    p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                    self.changePixmaps7.emit(p)
            
            except Exception as e:
                self.is_running = False
                self.capture = None
                self.msleep(5000)
                self.is_running = True

                debug.logger.info("something wrong with ipcam 7 .... ")
                debug.logger.error(str(e))
                debug.logger.info("retrying to connect.... ")
        else:
            debug.logger.info("IP CAM 7 not connected ... ")

class Thread8(QThread):

    changePixmaps8 = pyqtSignal(QImage)
    
    def run(self):
        
        debug = Debug()
        
        debug.logger.info("Run IP Cam 8 Thread ...")

        self.is_running = True
        self.capture = None
        
        while self.is_running:
            try:

                if not self.capture:
                    rtsp = IPCam.list_ip[7]            
                    debug.logger.info("Run video capture from --> "+ rtsp)
                    self.capture = cv2.VideoCapture(rtsp)
                    
                elif not ret:
                    debug.logger.error("Failed to read from video stream!")
                    raise Exception("Failed to read from video stream!")   
                
                ret, frame = self.capture.read()
                if ret:
                    rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
                    h, w, ch = rgbImage.shape
                    bytesPerLine = ch * w
                    convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                    p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                    self.changePixmaps8.emit(p)
            
            except Exception as e:
                self.is_running = False
                self.capture = None
                self.msleep(5000)
                self.is_running = True

                debug.logger.info("something wrong with ipcam 8 .... ")
                debug.logger.error(str(e))
                debug.logger.info("retrying to connect.... ")
        else:
            debug.logger.info("IP CAM 8 not connected ... ")



class IPCam(Util, View):
    img_name = ""

    ####### get ipcam ip ########
    ini = Util.getPath(None,fileName="app.ini")
        
    configur = ConfigParser()
    configur.read(ini)

    jum_gate = 0
    list_ip = []

    for i in range(8):
        try:
            n = i+1
            ip = [configur[f"gate{n}"]["ipcam1"], configur[f"gate{n}"]["ipcam2"]]
            list_ip = list_ip + ip
            
            jum_gate+=1
        except:
            break;
    
    ##############################

    def __init__(self, multiproc_conn) -> None:
        
        
        self.cam_comp = {}
        self.lbl_comp = {}
        self.debug = Debug()

        self.process_conn = multiproc_conn
        self.snap_stat = False
        self.snap_thread_stat = False

        # 1. initialize important property & method from all parents
        # exampel : in Components Class --> self.components = {}
        super().__init__()

        # create one main window object for all
        self.window = QMainWindow()

        self.camGUI()

    def camGUI(self):
        window_setter = {
            "title":"Cam Dashboard", 
            "size": "fullScreen",
            "style": "background-color: #fff; color:#000;"
        }

        # create window
        self.CreateWindow(window_setter, self.window)
        
        # create layouts
        self.main_layout = self.CreateLayout(("VBoxLayout", False), self.window)            
        self.main_layout.setContentsMargins(200, 50, 200, 50)

        # loop cam gui based on app.ini
        # ===================== start cam loop =========================
        
        self.cam_layout = self.CreateLayout(("FormLayout", False), self.main_layout)
        self.main_layout.addLayout(self.cam_layout)
        
        self.methods = []

        for i in range(IPCam.jum_gate):
            method_name = f"initGate{i+1}"
            print(f"==> method: {method_name}")
            method = getattr(self, method_name, None)
            
            method()
            sleep(1)

        # ============= end cam loop =================


        widget = QWidget()
        widget.setLayout(self.main_layout)
        
        scroll = QScrollArea() 
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        scroll.setMinimumWidth(100)
        scroll.setMaximumHeight(1200)
        
        self.window.setCentralWidget(scroll)

        self.main_layout.addStretch(1)

        self.window.showMinimized()
        self.window.setWindowFlag(Qt.WindowCloseButtonHint, True) # set false to hide running proccess
        
        self.app.aboutToQuit.connect(self.stopThreads)
        sys.exit(self.app.exec_())

    def stopThreads(self):
        print("kill all threads")
        # self.ss_th.quit()
        # self.ss_th.terminate()
        # # self.ss_th.wait()

        # self.ss_th2.quit()
        # self.ss_th2.terminate()
        # self.ss_th2.wait()

    def snap_func(self):
        self.snap_stat = True

    def snap_thread(self, image):
        self.debug.logger.info("Run snapshot thread( standby waiting snapshot# command ) ...")

        while True:
            snap = self.process_conn.recv()
            
            if  "snapshot#" in snap:
                
                self.debug.logger.info("Get & Split snapshot command")

                # split barcode from snapshot# string
                snap = snap.replace("snapshot#", "")

                self.snap_stat = True
                self.snap_barcode = snap

    # ========= init gate ==========
    def initGate1(self):
        gate_lbl = QLabel("GATE 1")
        gate_lbl.setFont( View.fontStyle(None, "Helvetica", 20, 80) )
       
        # web cam image here with label helper
        self.lbl1 = QLabel()
        self.lbl1.setMaximumWidth(640)
        self.lbl1.setMaximumHeight(400)
        self.lbl1.setStyleSheet(View.bg_black)
        
        self.lbl2 = QLabel()
        self.lbl2.setMaximumWidth(640)
        self.lbl2.setMaximumHeight(400)
        self.lbl2.setStyleSheet(View.bg_black)

        # connect pixmap with label, using thread
        self.th = Thread()
        self.th.changePixmaps.connect(self.setImage) # using pyqt5 slot and signal 
        self.th.start()
        
        self.th2 = Thread2()
        self.th2.changePixmaps2.connect(self.setImage2) # using pyqt5 slot and signal 
        self.th2.start()

        # add cam & others data to from layout
        self.cam_layout.addRow(gate_lbl)
        self.cam_layout.addRow(self.lbl1, self.lbl2)

    
    def initGate2(self):
        gate_lbl = QLabel("GATE 2")
        gate_lbl.setStyleSheet("margin-top: 20px;")
        gate_lbl.setFont( View.fontStyle(None, "Helvetica", 20, 80) )
        
        # web cam image here with label helper
        self.lbl3 = QLabel()
        self.lbl3.setMaximumWidth(640)
        self.lbl3.setMaximumHeight(400)
        self.lbl3.setStyleSheet(View.bg_black)
        
        self.lbl4 = QLabel()
        self.lbl4.setMaximumWidth(640)
        self.lbl4.setMaximumHeight(400)
        self.lbl4.setStyleSheet(View.bg_black)
        
        # connect pixmap with label, using thread
        self.th3 = Thread3()
        self.th3.changePixmaps3.connect(self.setImage3) # using pyqt5 slot and signal 
        self.th3.start()
        
        self.th4 = Thread4()
        self.th4.changePixmaps4.connect(self.setImage4) # using pyqt5 slot and signal 
        self.th4.start()

        # add cam & others data to from layout
        self.cam_layout.addRow(gate_lbl)
        self.cam_layout.addRow(self.lbl3, self.lbl4)
    
    def initGate3(self):
        gate_lbl = QLabel("GATE 3")
        gate_lbl.setStyleSheet("margin-top: 20px;")
        gate_lbl.setFont( View.fontStyle(None, "Helvetica", 20, 80) )
        
        # web cam image here with label helper
        self.lbl5 = QLabel()
        self.lbl5.setMaximumWidth(640)
        self.lbl5.setMaximumHeight(400)
        self.lbl5.setStyleSheet(View.bg_black)
        
        self.lbl6 = QLabel()
        self.lbl6.setMaximumWidth(640)
        self.lbl6.setMaximumHeight(400)
        self.lbl6.setStyleSheet(View.bg_black)
        
        # connect pixmap with label, using thread
        self.th5 = Thread5()
        self.th5.changePixmaps5.connect(self.setImage5) # using pyqt5 slot and signal 
        self.th5.start()
        
        self.th6 = Thread6()
        self.th6.changePixmaps6.connect(self.setImage6) # using pyqt5 slot and signal 
        self.th6.start()

        # add cam & others data to from layout
        self.cam_layout.addRow(gate_lbl)
        self.cam_layout.addRow(self.lbl5, self.lbl6)
    
    def initGate4(self):
        gate_lbl = QLabel("GATE 4")
        gate_lbl.setStyleSheet("margin-top: 20px;")
        gate_lbl.setFont( View.fontStyle(None, "Helvetica", 20, 80) )
        
        # web cam image here with label helper
        self.lbl7 = QLabel()
        self.lbl7.setMaximumWidth(640)
        self.lbl7.setMaximumHeight(400)
        self.lbl7.setStyleSheet(View.bg_black)
        
        self.lbl8 = QLabel()
        self.lbl8.setMaximumWidth(640)
        self.lbl8.setMaximumHeight(400)
        self.lbl8.setStyleSheet(View.bg_black)
        
        # connect pixmap with label, using thread
        self.th7 = Thread7()
        self.th7.changePixmaps7.connect(self.setImage7) # using pyqt5 slot and signal 
        self.th7.start()
        
        self.th8 = Thread8()
        self.th8.changePixmaps8.connect(self.setImage8) # using pyqt5 slot and signal 
        self.th8.start()

        # add cam & others data to from layout
        self.cam_layout.addRow(gate_lbl)
        self.cam_layout.addRow(self.lbl7, self.lbl8)
    # ==============================
    
    # @pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        try:
            self.lbl1.setPixmap(QPixmap.fromImage(image))
            
        except Exception as e:
            self.debug.logger.info("Something wrong with set image frame to QLabel 1 ...")
            self.debug.logger.error(str(e))
        
        if self.snap_thread_stat == False:
            start_new_thread(self.snap_thread, (image,))
            self.snap_thread_stat = True

        if self.snap_stat:
            image.save(f"./cap/{self.snap_barcode}.jpg","JPG")
            self.snap_stat = False
            image = QImage()
            self.debug.logger.info("save snapshot image & re-init QImage 1 ...")

    def setImage2(self, image):
        try:
            self.lbl2.setPixmap(QPixmap.fromImage(image))
            
        except Exception as e:
            self.debug.logger.info("Something wrong with set image frame to QLabel 2 ...")
            self.debug.logger.error(str(e))

    def setImage3(self, image):
        try:
            self.lbl3.setPixmap(QPixmap.fromImage(image))
            
        except Exception as e:
            self.debug.logger.info("Something wrong with set image frame to QLabel 3 ...")
            self.debug.logger.error(str(e))

    def setImage4(self, image):
        try:
            self.lbl4.setPixmap(QPixmap.fromImage(image))
            
        except Exception as e:
            self.debug.logger.info("Something wrong with set image frame to QLabel 4 ...")
            self.debug.logger.error(str(e))
    
    def setImage5(self, image):
        try:
            self.lbl5.setPixmap(QPixmap.fromImage(image))
            
        except Exception as e:
            self.debug.logger.info("Something wrong with set image frame to QLabel 5 ...")
            self.debug.logger.error(str(e))

    def setImage6(self, image):
        try:
            self.lbl6.setPixmap(QPixmap.fromImage(image))
            
        except Exception as e:
            self.debug.logger.info("Something wrong with set image frame to QLabel 6 ...")
            self.debug.logger.error(str(e))

    def setImage7(self, image):
        try:
            self.lbl7.setPixmap(QPixmap.fromImage(image))
            
        except Exception as e:
            self.debug.logger.info("Something wrong with set image frame to QLabel 7 ...")
            self.debug.logger.error(str(e))

    def setImage8(self, image):
        try:
            self.lbl8.setPixmap(QPixmap.fromImage(image))
            
        except Exception as e:
            self.debug.logger.info("Something wrong with set image frame to QLabel 8 ...")
            self.debug.logger.error(str(e))

# HOST = "127.0.0.1" --> sys.argv[1]
# PORT = 65430 --> sys.argv[2]
# class Server(Util, View):
class Server:

    db_cursor = None
    list_of_clients = {}
    ipcam1 = ""
    ipcam2 = ""

    def __init__(self, host, port, multiproc_conn ) -> None:
        
        # init debug
        self.debug = Debug()

        self.process_conn = multiproc_conn
        self.SERVER_IP = host

        self.connect_to_postgresql()
        self.connect_server(host, int(port))

    def client_thread(self, conn,addr):
        self.debug.logger.info("Start client thread")
        
        with conn:
            # tidak masalah pembuatan komponen label koneksi disini
            # karena kalaupun koneksi gagal maka statusnya bisa dicek ama looping cek koneksi pada program client_service
            # lagipula disini sudah ada append list utk ip client

            # yg memebdakan satu client dengan client yg lain adalah ip ny
            # sementara pada penamaan komponen label harus ada hubungan/integrasi antara client yg konek dengan name 
            # komponent tersebut

            self.debug.logger.info(f"Connected by {addr}")
            
            # create label component

            try:
                self.debug.logger.info("Server standby waiting message from client ... ")

                while True:
                    data = conn.recv(1024)
                    msg = data.decode("utf-8")
                    
                    if(msg==''):
                        self.debug.logger.info(f"client{addr} disconnected at {datetime.datetime.now()}")
                    elif(msg!=''):
                        
                        # disini harus bisa membedakan data string yg diterima
                        # apakah itu string RFID 
                        # atau string datetime utk karcis parkir
                        # disini akan terjadi proses pengecekan agar return value sesuai dengan bagiannya
                        # disini juga terjadi proses capture imag dari ipcam

                        # txt = data.decode("utf-8")
                        # print(data.decode("utf-8"))
                        # print("===========> masuk bro")
                        # print(msg)

                        if "rfid#" in msg:
                            try:
                                msg = re.search('rfid#(.+?)#end', msg).group(1)
                            except Exception as e:
                                self.debug.logger.debug("rfid between substring not found ... ")
                                self.debug.logger.error(str(e))

                            print("==================================")
                            print("checking RFID ...")

                            # self.db_cursor.execute("select count(*) as count from rfid where rfid='123'")
                            res = self.exec_query(f"select count(*) as count from rfid where rfid='{msg}'", "select")
                            # print(f"select count(*) as count from rfid where rfid='{msg}'")
                            self.debug.logger.debug("RFID result: "+ str(res[0][0]))
                            
                                  

                            if res[0][0] == 1:
                                self.debug.logger.debug("success rfid")
                                conn.sendall( bytes("rfid-true", 'utf-8') )
                            else:
                                self.debug.logger.debug("fail rfid")
                                conn.sendall( bytes("rfid-false", 'utf-8') )
                            print("==================================")

                        elif "date#" in msg:
                            try:
                                self.debug.logger.debug("Set datetime for client ... ")

                                # get current date
                                today = datetime.datetime.now()
                                dt = today.strftime("%Y-%m-%d %H:%M:%S")

                                conn.sendall( bytes(f"date#{dt}#end", 'utf-8') )
                            except Exception as e:
                                self.debug.logger.debug("getdate between substring not found ... ")
                                self.debug.logger.error(str(e))

                        elif "pushButton#" in msg:
                            
                            try:
                                msg = re.search('pushButton#(.+?)#end', msg).group(1)
                            except AttributeError:
                                self.debug.logger.error("JSON between substring not found ... ")

                            try:
                                
                                self.debug.logger.debug("get json string : " + msg)
                                self.debug.logger.info("converting to dictionary ...")
                                res = json.loads(msg)    
                                self.debug.logger.debug(res)

                                # get data from json
                                barcode = res["barcode"]
                                time = res["time"]
                                jns_kendaraan = res["jns_kendaraan"]
                                gate = res["gate"]
                                ip_raspi = res["ip_raspi"]
                                # save to db
                                Y = time[0:4]
                                M = time[4:6]
                                D = time[6:8]

                                h = time[8:10]
                                m = time[10:12]
                                s = time[12:14]
                                
                                time = int(time)
                                # insert into karcis (datetime) values('2023-01-05 10:43:50.866085');
                                dt = f'{Y}-{M}-{D} {h}:{m}:{s}'
                                q = f"insert into karcis (barcode, datetime, gate, jenis_kendaraan, ip_raspi) values ('{barcode}', '{dt}', '{gate}', '{jns_kendaraan}', '{ip_raspi}')";
                                self.exec_query(q)

                                # set filename from ip cam class
                                IPCam.img_name = barcode

                                # capture cam image
                                self.debug.logger.info("server ask to snapshot ....")
                                self.process_conn.send(f"snapshot#{barcode}")
                                
                                self.debug.logger.info("Save Date Time & capture cam image success ....")
                                self.debug.logger.info(f"send return value to raspi( {addr} )....")
                                
                                conn.sendall( bytes("printer-true", 'utf-8') )
                            
                            except Exception as e:
                                self.debug.logger.error(str(e))
                            
                        elif "config#" in msg:
                            try:
                                print("===================================")
                                msg = re.search('config#(.+?)#end', msg).group(1)
                                self.debug.logger.info("receive message from GUI: "+ msg)

                                self.debug.logger.info("broadcast to clients ...")

                                for ip in self.list_of_clients.keys():
                                    if ip != self.SERVER_IP:
                                        self.debug.logger.info(f"send config JSON to {ip} ... ")
                                        self.list_of_clients[ip].sendall( bytes(f'config#{msg}#end', 'utf-8') )
                                        sleep(1)

                            except Exception as e:
                                self.debug.logger.error(str(e))
                            
                        elif "gate#" in msg:
                            print("===================================")
                            ip = re.search('gate#(.+?)#end', msg).group(1)
                            self.debug.logger.info("Open gate with ip : "+ ip)

                            self.list_of_clients[ip].sendall( bytes(f'open-true', 'utf-8') )
                    if not data:
                        break
            except:
                self.debug.logger.error(f"client{addr} disconnected at {datetime.datetime.now()}")
                

    def connect_server(self, h, p):
        print("============> masuk bro")
        self.debug.logger.info("conn to server ... ")
        
        # while true -> fro server socket always stanby, event after client connection break/fail
        while True:
            # start_new_thread(self.gui,())    
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((h, p))
                s.listen()
                conn, addr = s.accept()
                
                # save conn obj based on ip
                self.list_of_clients[f"{addr[0]}"] = conn

                t = start_new_thread(self.client_thread, (conn, addr))
                
    def getPath(self,fileName):
        path = os.path.dirname(os.path.realpath(__file__))
        return '/'.join([path, fileName])

    def connect_to_postgresql(self):
        # //disini wak
        self.debug.logger.info("conn to potsgre")
        ini = self.getPath("app.ini")
        
        configur = ConfigParser()
        configur.read(ini)
        
        conn = psycopg2.connect(
            database=configur["db"]["db_name"], user=configur["db"]["username"], password=configur["db"]["password"], host=configur["db"]["host"], port= configur["db"]["port"]
        )

        conn.autocommit = True
        self.db_cursor = conn.cursor()

    
    def exec_query(self, query, type=""):
        try:
            self.db_cursor.execute(query)
            self.debug.logger.debug("\nsuccess execute query")

            if type == "":    
                return True

            elif type.lower() == "select":
                data = self.db_cursor.fetchall()
                return data

        except Exception as e:
            self.debug.logger.error(str(e))


def run():
    conn1, conn2 = multiprocessing.Pipe()
    process_1 = multiprocessing.Process(target=IPCam, args=(conn1,), name="IPCAM")
    process_2 = multiprocessing.Process(target=Server, args=(sys.argv[1], sys.argv[2], conn2), name="SERVER")
    process_1.start()
    process_2.start()
    process_1.join()
    process_2.join()

if __name__ == "__main__":
    run()