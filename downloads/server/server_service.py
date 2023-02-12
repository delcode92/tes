import os,sys, re, socket, psycopg2, logging, datetime, json, multiprocessing
from time import sleep
from cv2 import add
from _thread import start_new_thread
from framework import *
from configparser import ConfigParser

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

    changePixmap = pyqtSignal(QImage)

    def run(self):
        debug = Debug()
        
        debug.logger.info("Run Cam Thread ...")

        self.is_running = True
        self.capture = None
        
        while self.is_running:
            try:

                if not self.capture:
                    rtsp = 'rtsp://admin:admin@192.168.100.121'        
                    debug.logger.info("Run video capture from --> "+ rtsp)
                    self.capture = cv2.VideoCapture(rtsp)
                    # self.capture = cv2.VideoCapture(0)

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
                    self.changePixmap.emit(p)
            
            except Exception as e:
                self.is_running = False
                self.capture = None
                self.msleep(5000)
                self.is_running = True

                debug.logger.info("something wrong with ipcam .... ")
                debug.logger.error(str(e))
                debug.logger.info("retrying to connect.... ")
        else:
            debug.logger.info("IP CAM not connected ... ")

class IPCam(Util, View):
    img_name = ""
    def __init__(self, multiproc_conn) -> None:
        
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
        main_layout = self.CreateLayout(("VBoxLayout", False), self.window)
            
        main_layout.setContentsMargins(200, 50, 200, 50)
        cam_layout = self.CreateLayout(("FormLayout", False), main_layout)
        
        right_list = self.CreateLayout(("VBoxLayout", False))
        right_list.setContentsMargins(0,0,0,0)
        right_list.setSpacing(0)

        status_layout =  self.CreateLayout(("FormLayout", False))
        
        # set right layout background
        right_widget = QWidget()
        right_widget.setLayout(right_list)
        right_widget.setStyleSheet(View.bg_grey)
        right_widget.setMinimumHeight(20)
        right_widget.setMinimumWidth(250)

        # inside right_widget --> there is widget that contain status layout(form lay)

        # set status widget
        stat_widget = QWidget()
        stat_widget.setLayout(status_layout)
        stat_widget.setMaximumHeight(150)
        stat_widget.setMaximumWidth(250)
        
        # put component into right form
        gate_lbl = QLabel("GATE 1")
        gate_lbl.setFont( View.fontStyle(None, "Helvetica", 20, 80) )

        ip_lbl = QLabel("IP Address: ")
        ip_lbl.setMinimumWidth(100)
        ip_lbl.setFont( View.fontStyle(None, "Helvetica", 12, 40) )

        ip_val = QLabel("192.168.100.1")
        ip_val.setFont( View.fontStyle(None, "Helvetica", 12, 40) )

        stat_lbl = QLabel("Status: ")
        stat_lbl.setMinimumWidth(100)
        stat_lbl.setFont( View.fontStyle(None, "Helvetica", 12, 40) )
        
        stat_val = QLabel("CONNECTED")
        stat_val.setFont( View.fontStyle(None, "Helvetica", 12, 80) )
        stat_val.setStyleSheet(View.bg_light_green + View.color_white + "padding :8px")

        status_layout.addRow(gate_lbl)
        status_layout.addRow(ip_lbl, ip_val)
        status_layout.addRow(stat_lbl, stat_val)

        # snap_button = QPushButton("snap")
        # status_layout.addRow(stat_lbl, snap_button)

        # snap_button.clicked.connect(self.snap_func)

        # web cam image here with label helper
        self.lbl1 = QLabel()
        self.lbl1.setMinimumWidth(640)
        self.lbl1.setMinimumHeight(400)
        self.lbl1.setStyleSheet(View.bg_black)

        # connect pixmap with label, using thread
        th = Thread()
        th.changePixmap.connect(self.setImage) # using pyqt5 slot and signal 
        th.start()

        right_list.addWidget(stat_widget)

        # add cam & others data to from layout
        cam_layout.addRow(self.lbl1, right_widget)

        # add cam layout(from layout) to main layout
        main_layout.addLayout(cam_layout)
        
        widget = QWidget()
        widget.setLayout(main_layout)
        
        scroll = QScrollArea() 
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        scroll.setMinimumWidth(100)
        # scroll.setMaximumWidth(1200)
        
        self.window.setCentralWidget(scroll)

        self.window.showMinimized()
        sys.exit(self.app.exec_())

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

    # @pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        try:
            self.lbl1.setPixmap(QPixmap.fromImage(image))
            
        except Exception as e:
            self.debug.logger.info("Something wrong with set image frame to QLabel ...")
            self.debug.logger.error(str(e))
        
        if self.snap_thread_stat == False:
            start_new_thread(self.snap_thread, (image,))
            self.snap_thread_stat = True

        if self.snap_stat:
            image.save(f"./cap/{self.snap_barcode}.jpg","JPG")
            self.snap_stat = False
            image = QImage()
            self.debug.logger.info("save snapshot image & re-init QImage ...")

# HOST = "127.0.0.1" --> sys.argv[1]
# PORT = 65430 --> sys.argv[2]
# class Server(Util, View):
class Server:

    db_cursor = None
    list_of_clients = {}
    
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
                        # print(msg)

                        if "rfid#" in msg:
                            try:
                                msg = re.search('rfid#(.+?)#end', msg).group(1)
                            except AttributeError:
                                self.debug.logger.error("rfid between substring not found ... ")

                            print("==================================")
                            self.debug.logger.debug("checking RFID ...")

                            # self.db_cursor.execute("select count(*) as count from rfid where rfid='123'")
                            res = self.exec_query(f"select count(*) as count from rfid where rfid='{msg}'", "select")
                            self.debug.logger.debug("RFID result: "+ res[0][0])

                            if res[0][0] == 1:
                                self.debug.logger.debug("success rfid")
                                conn.sendall( bytes("rfid-true", 'utf-8') )
                            else:
                                self.debug.logger.error("fail rfid")
                                conn.sendall( bytes("rfid-false", 'utf-8') )
                            print("==================================")

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
    process_1 = multiprocessing.Process(target=IPCam, args=(conn1,))
    process_2 = multiprocessing.Process(target=Server, args=(sys.argv[1], sys.argv[2], conn2))
    process_1.start()
    process_2.start()
    process_1.join()
    process_2.join()

if __name__ == "__main__":
    run()