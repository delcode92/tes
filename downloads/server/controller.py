import sys, psycopg2, os, math, threading, logging
from logging.handlers import TimedRotatingFileHandler

from client.client_service import Client
from PyQt5.QtWidgets import (QMdiArea, QMessageBox, QMdiSubWindow, QWidget ,QHeaderView, QLabel, QPushButton, QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import Qt, QRect,QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor, QIcon
from configparser import ConfigParser
from escpos.printer import Usb
from datetime import datetime

# from framework import View

class Controller(Client):
    def __init__(self) -> None:
        # self.Util.__init__(self)
        
        self.initDebug()

        # active db cursor 
        self.connect_to_postgresql()
        self.sw_stat = False
        
        # ========== steps ========
        
        self.logger.info("\nController constructor: ")
        self.logger.info("connect to DB .....")
        self.logger.info("active DB cursor ..... \n")

    def initDebug(self):
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

        # clear log file every 1 day
        rotate = TimedRotatingFileHandler('sample.log', when='D', interval=1, backupCount=0, encoding=None, delay=False, utc=False)
        
        self.logger.addHandler(rotate)
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    

    def connect_to_server(self, h, p):
        super().__init__(h,p)
        

    def connect_to_postgresql(self):
        try:
            ini = self.getPath("app.ini")
            
            configur = ConfigParser()
            configur.read(ini)
            
            conn = psycopg2.connect(
                database=configur["db"]["db_name"], user=configur["db"]["username"], password=configur["db"]["password"], host=configur["db"]["host"], port= configur["db"]["port"]
            )
            conn.autocommit = True
            self.db_cursor = conn.cursor()
        except Exception as e:
            self.logger.error( str(e) )    
        
    def exec_query(self, query, type=""):
        
        try:
            self.db_cursor.execute(query)
            self.logger.info("\nsuccess execute query")

            if type.lower() != "select":    
                return True

        except Exception as e:
            self.logger.info("\nexecute query fail")
            self.logger.error( str(e) )


        if type.lower() =="select":
            data = self.db_cursor.fetchall()
            return data



    def login_ctrl(self, arg):
        
        uname = self.components["input_uname"].text()
        passwd = self.components["input_pass"].text()
        q = self.exec_query(f"select * from users where username='{uname}' and password='{passwd}'", "select")
        
        if len(q) == 1:
            
            level = q[0][2].lower()
        
            if level=="admin":
                self.closeWindow(arg[0])
                self.AdminDashboard()
            elif level=="kasir":
                self.closeWindow(arg[0])
                self.KasirDashboard()
    
    def getPrice(self):
        jns_kendaraan = ""
        try:
            # get time based on barcode
            barcode = self.components["barcode_transaksi"].text()
            barcode_time = self.exec_query(f"select datetime, jenis_kendaraan, status_parkir, ip_raspi from karcis where barcode='{barcode}'", "select")
            jns_kendaraan = barcode_time[0][1].capitalize()
            self.ip_raspi = barcode_time[0][3]

            if barcode_time[0][2]:
                status_parkir = "LUNAS"
            elif not barcode_time[0][2]:
                status_parkir = "BELUM LUNAS"
            
            if len(barcode_time[0]) > 0:
                price = 0
                self.time_now = datetime.now()
                self.time_now = self.time_now.replace(tzinfo=None)
                
                barcode_time = barcode_time[0][0].replace(tzinfo=None)

                diff = self.time_now - barcode_time
                total_hours = math.ceil(diff.total_seconds()/3600)
                
                print("====================")
                print("TH", total_hours, type(total_hours))
                print("jns kendaraan:", jns_kendaraan)
                print("====================\n\n")
            
                # get base price from db
                base_price = self.exec_query(f"select tarif_perjam,tarif_per24jam from tarif where jns_kendaraan='{jns_kendaraan}'", "select")
                base_price_perjam = base_price[0][0] 
                base_price_per24jam = base_price[0][1] 
                
                if total_hours==0:
                    jam = 1
                    price = jam * base_price_perjam
                    print("================")
                    print(jam, "jam")
                    print(price, "Rupiah")
                    print("================\n\n")
                
                elif total_hours<24 and total_hours>0:
                    price = total_hours * base_price_perjam
                    
                    print("================")
                    print(total_hours, "jam")
                    print(price, "Rupiah")
                    print("================\n\n")
                
                elif total_hours>24:
                    hari = math.floor(total_hours/24)
                    jam = total_hours-(hari*24)

                    price = (hari*base_price_per24jam) + (jam*base_price_perjam)

                    print("================")
                    print(hari, "hari")
                    print(jam, "jam")
                    print(price, "Rupiah")
                    print("================\n\n")
                
                # set value to textbox
                self.components["jns_kendaraan"].setText( jns_kendaraan )
                self.components["ket_status"].setText( str(status_parkir) )
                
                # just show tarif and enable button if "BELUM LUNAS"
                if status_parkir == "BELUM LUNAS":
                    self.components["tarif_transaksi"].setText( str(price) )
                    
        except Exception as e:
            # clear text box if false input barcode
            self.components["jns_kendaraan"].setText("")
            self.components["ket_status"].setText("")
            self.components["tarif_transaksi"].setText("")

            self.logger.error(str(e))
    
    def hideSuccess(self):
        self.components["lbl_success"].setHidden(True)

    def add_rfid(self):
        # get data
        rfid = self.components["add_rfid"].text()
        name = self.components["add_rfid_owner"].text()
        
        # save data
        query = f"insert into rfid (rfid, nama) values ('{rfid}', '{name}');"
        res = self.exec_query(query)
        
        if res:

            # reset table value
            query = self.exec_query("SELECT id, rfid, nama FROM rfid order by nama", "SELECT")
            cols = 3

            self.fillTable(self.rfid_table, cols, query, len(query))
             
            # clear all input
            self.components["add_rfid"].setText("")
            self.components["add_rfid_owner"].setText("")

            # show success message

            # modal
            dlg = QMessageBox(self.window)
            
            dlg.setWindowTitle("Alert")
            dlg.setText("Data Saved")
            dlg.setIcon(QMessageBox.Information)
            dlg.exec()



    def add_user(self):
        uname = self.components["add_uname"].text()    
        passwd = self.components["add_pass"].text()    
        retype_passwd = self.components["retype_pass"].text()    
        user_level = self.components["input_user_level"].currentText()    
        
        if passwd == retype_passwd:

            # save data
            query = f"insert into users (username, user_level, password) values ('{uname}', '{user_level}', '{passwd}');"
            res = self.exec_query(query)
            
            if res:
                
                # reset table value
                query = self.exec_query("SELECT id, username, user_level FROM users", "SELECT")
                cols = 3

                self.fillTable(self.user_table, cols, query, len(query))

                 # clear all input
                self.components["add_uname"].setText("")
                self.components["add_pass"].setText("")
                self.components["retype_pass"].setText("")

                
                # show success message

                # modal
                dlg = QMessageBox(self.window)
                
                dlg.setWindowTitle("Alert")
                dlg.setText("Data Saved")
                dlg.setIcon(QMessageBox.Information)
                dlg.exec()
    
    def add_kasir(self):
        nik = self.components["add_nik"].text()    
        nama = self.components["add_nama"].text()    
        hp = self.components["add_hp"].text()    
        alamat = self.components["add_alamat"].text()    
        jm_masuk = self.components["add_jam_masuk"].text()    
        jm_keluar = self.components["add_jam_keluar"].text()    
        no_pos = self.components["add_nmr_pos"].text()    
        
        # save data
        query = f"insert into kasir (nik, nama, hp, alamat, jm_masuk, jm_keluar, no_pos) values ('{nik}', '{nama}', '{hp}', '{alamat}', '{jm_masuk}', '{jm_keluar}', '{no_pos}');"
        res = self.exec_query(query)
        
        if res:

            # reset table value
            query = self.exec_query("SELECT id, nik, nama, hp, alamat, jm_masuk, jm_keluar, no_pos FROM kasir", "SELECT")
            cols = 8

            self.fillTable(self.kasir_table, cols, query, len(query))

            # clear all input
            self.components["add_nik"].setText("")    
            self.components["add_nama"].setText("")    
            self.components["add_hp"].setText("")    
            self.components["add_alamat"].setText("")    
            self.components["add_jam_masuk"].setText("")    
            self.components["add_jam_keluar"].setText("")    
            self.components["add_nmr_pos"].setText("")
            
            # show success message
            
            # modal
            dlg = QMessageBox(self.window)
            
            dlg.setWindowTitle("Alert")
            dlg.setText("Data Saved")
            dlg.setIcon(QMessageBox.Information)
            dlg.exec()

    def add_gate(self):
        pos = self.components["add_pos"].text()    
        tipe = self.components["add_tipe_pos"].currentText()    
        jns_kendaraan = self.components["add_jenis_kendaraan"].currentText()    
        ipcam = self.components["add_ipcam"].text()    
        
        # save data
        query = f"insert into gate (no_pos, tipe_pos, jns_kendaraan, ip_cam) values ('{pos}', '{tipe}', '{jns_kendaraan}', '{ipcam}');"
        res = self.exec_query(query)
        
        if res:
                # clear all input
            self.components["add_pos"].setText("")
            self.components["add_ipcam"].setText("")
            
            # show success message
            self.components["lbl_success"].setHidden(False)

            timer = threading.Timer(1.0, self.hideSuccess)
            timer.start()        
    
    def setPay(self):
        # get barcode
        barcode = self.components["barcode_transaksi"].text()
        kendaraan = self.components["jns_kendaraan"].text()
        stat = self.components["ket_status"].text()
        tarif = self.components["tarif_transaksi"].text()

        if barcode != "" and kendaraan != "" and stat != "" and tarif != "":

            # update status to true, tarif and date_keluar
            dt_keluar = self.time_now.strftime('%Y-%m-%d %H:%M:%S')

            self.exec_query(f"update karcis set status_parkir=true, tarif='{tarif}', date_keluar='{dt_keluar}' where barcode='{barcode}'")
            
            # clear all text box and disable button
            self.components["barcode_transaksi"].setText("")
            self.components["jns_kendaraan"].setText("")
            self.components["ket_status"].setText("")
            self.components["tarif_transaksi"].setText("")
            
            # send data to server to open the gate
            self.logger.debug("open gate ... ")

            # modal
            dlg = QMessageBox(self.window)
            
            dlg.setWindowTitle("Alert")
            dlg.setText("Payment success --> OPEN GATE KELUAR")
            dlg.setIcon(QMessageBox.Information)
            dlg.exec()

            # self.s.sendall( bytes('gate#'+self.ip_raspi+'#end', 'utf-8') )

    def setReport(self):
        barcode = self.components["barcode_bermasalah"].text() 
        ket = self.components["ket_bermasalah"].text() 

        if barcode != "" and ket != "":
            self.exec_query(f"insert into laporan_users (barcode, ket) values('{barcode}', '{ket}')")

            # modal
            dlg = QMessageBox(self.window)
            
            dlg.setWindowTitle("Alert")
            dlg.setText("Saved")
            dlg.setIcon(QMessageBox.Information)
            dlg.exec()

    def add_tarif(self):
        pos = self.components["add_tarif_pos"].text()    
        tarif_perjam = self.components["add_tarif_per_1jam"].text()    
        tarif_per24jam = self.components["add_tarif_per_24jam"].text()    
        jns_kendaraan = self.components["add_tarif_jns_kendaraan"].currentText()    
        
        # save data
        query = f"insert into tarif (no_pos, tarif_perjam, tarif_per24jam, jns_kendaraan) values ('{pos}', '{tarif_perjam}', '{tarif_per24jam}', '{jns_kendaraan}');"
        res = self.exec_query(query)
        
        if res:
            # clear all input
            self.components["add_tarif_pos"].setText("")    
            self.components["add_tarif_per_1jam"].setText("")    
            self.components["add_tarif_per_24jam"].setText("")    
        
            # show success message
            self.components["lbl_success"].setHidden(False)

            timer = threading.Timer(1.0, self.hideSuccess)
            timer.start()        

    def add_voucher(self):
        id_pel = self.components["add_voucher_idpel"].text()    
        lokasi = self.components["add_voucher_lokasi"].text()    
        tarif = self.components["add_voucher_tarif"].text()    
        masa_berlaku = self.components["add_voucher_masa_berlaku"].text()    
        jns_kendaraan = self.components["add_voucher_jns_kendaraan"].currentText()

        # save data
        query = f"insert into voucher (id_pel, lokasi, tarif, masa_berlaku, jns_kendaraan) values ('{id_pel}', '{lokasi}', '{tarif}', '{masa_berlaku}', '{jns_kendaraan}');"
        res = self.exec_query(query)
        
        if res:

            # reset table value
            query = self.exec_query("SELECT id, id_pel, lokasi, tarif, masa_berlaku, jns_kendaraan FROM voucher", "SELECT")
            cols = 6

            self.fillTable(self.voucher_table, cols, query, len(query))

            # clear all input
            id_pel = self.components["add_voucher_idpel"].setText("")    
            lokasi = self.components["add_voucher_lokasi"].setText("")    
            tarif = self.components["add_voucher_tarif"].setText("")    
            
            # show success message
            
            # modal
            dlg = QMessageBox(self.window)
            
            dlg.setWindowTitle("Alert")
            dlg.setText("Data Saved")
            dlg.setIcon(QMessageBox.Information)
            dlg.exec()    

    def save_edit_rfid(self):
        # get data from edit form
        # id = self.components["hidden_id"].text()

        id = str(self.hidden_id)
        rfid = self.components["add_rfid"].text()
        owner = self.components["add_rfid_owner"].text()

        # run update query
        self.exec_query(f"update rfid set rfid='{rfid}', nama='{owner}' where id="+id)
        
        # close window edit
        self.win.close()

        # reset table value
        query = self.exec_query("SELECT id, rfid, nama FROM rfid order by nama", "SELECT")
        cols = 3

        self.fillTable(self.rfid_table, cols, query)
        
        # modal
        dlg = QMessageBox(self.window)
        
        dlg.setWindowTitle("Alert")
        dlg.setText("Data Updated")
        dlg.setIcon(QMessageBox.Information)
        dlg.exec()
    
        
    def save_edit_user(self):

        # get data from edit form
        id = str(self.hidden_id)
        uname = self.components["add_uname"].text()
        level = self.components["input_user_level"].currentText()
        passwd = self.components["add_pass"].text()
        retype_passwd = self.components["retype_pass"].text()

        if passwd == retype_passwd:

            # run update query
            self.exec_query(f"update users set username='{uname}', user_level='{level}', password='{passwd}' where id="+id)
            
            # close window edit
            self.win.close()

            # reset table value
            query = self.exec_query("SELECT id, username, user_level FROM users", "SELECT")
            cols = 3

            self.fillTable(self.user_table, cols, query)
            
            # modal
            dlg = QMessageBox(self.window)
            
            dlg.setWindowTitle("Alert")
            dlg.setText("Data Updated")
            dlg.setIcon(QMessageBox.Information)
            dlg.exec()
    
    def save_edit_kasir(self):

        # get data from edit form
        id = str(self.hidden_id)
        nik = self.components["add_nik"].text()
        nama = self.components["add_nama"].text()
        hp = self.components["add_hp"].text()
        alamat = self.components["add_alamat"].text()
        jm_masuk = self.components["add_jam_masuk"].text()
        jm_keluar = self.components["add_jam_keluar"].text()
        no_pos = self.components["add_nmr_pos"].text()

        # run update query
        self.exec_query(f"update kasir set nik='{nik}', nama='{nama}', hp='{hp}', alamat='{alamat}', jm_masuk='{jm_masuk}', jm_keluar='{jm_keluar}', no_pos='{no_pos}'  where id="+id)
        

        # close window edit
        self.win.close()

        # reset table value
        query = self.exec_query("SELECT id, nik, nama, hp, alamat, jm_masuk, jm_keluar, no_pos FROM kasir", "SELECT")
        cols = 8

        self.fillTable(self.kasir_table, cols, query)

        # modal
        dlg = QMessageBox(self.window)
        
        dlg.setWindowTitle("Alert")
        dlg.setText("Data Updated")
        dlg.setIcon(QMessageBox.Information)
        dlg.exec()
    
    def save_edit_gate(self):
        # get data from edit form
        id = self.components["hidden_id"].text()
        pos = self.components["add_pos"].text()
        tipe_pos = self.components["add_tipe_pos"].currentText()
        jns_kendaraan = self.components["add_jenis_kendaraan"].currentText()
        ipcam = self.components["add_ipcam"].text()
        
        # run update query
        self.exec_query(f"update gate set no_pos='{pos}', tipe_pos='{tipe_pos}', jns_kendaraan='{jns_kendaraan}', ip_cam='{ipcam}' where id="+id)
        
        # call table table list again
        self.windowBarAction("kelola gate")
    
    def save_edit_karcis(self):

        try:
            self.logger.info("send JSON config to client ... ")
            
            # get data from form
            nm_tempat = self.components["add_tempat"].text()
            footer1 = self.components["add_footer1"].text()
            footer2 = self.components["add_footer2"].text()
            footer3 = self.components["add_footer3"].text()
            
            # send data JSON to raspi via socket
            config_json = 'config#{"tempat":"'+nm_tempat+'", "footer1":"'+footer1+'", "footer2":"'+footer2+'", "footer3":"'+footer3+'"}#end'
            self.s.sendall( bytes(config_json, 'utf-8') )

            # modal
            dlg = QMessageBox(self.window)
            
            dlg.setWindowTitle("Alert")
            dlg.setText("broadcast success")
            dlg.setIcon(QMessageBox.Information)
            dlg.exec()

        except Exception as e:
            self.logger.error(str(e))

    def filterTarif(self, time="", timeBefore="", tarifMotor="", tarifMobil=""):
        
        if time != "":
            if int(time) < int(timeBefore):
                self.dialogBox(title="Alert", msg="jam tidak boleh lebih kecil dari nilai jam sebelumnya!")
                return False
            elif tarifMotor =="" or tarifMobil == "":
                self.dialogBox(title="Alert", msg="Kenaikan tarif motor/mobil tidak boleh kosong !")
                return False

        elif tarifMotor != "" or tarifMobil != "":
            if time == "":
                self.dialogBox(title="Alert", msg="Jam tarif tidak boleh kosong !")
                return False
            else:
                self.dialogBox(title="Alert", msg="Kenaikan tarif motor/mobil tidak boleh kosong !")
                return False

        
        return True


    def set_tarif(self):
        # get all inputs
        toleransi = self.components["add_toleransi"].text()
        
        # tarif kondisi 1
        # a if a < b else b
        time_kondisi1 = self.components["add_time1"].text()
        tarif_motor_kondisi1 = self.components["add_motor_biaya1"].text()    
        tarif_mobil_kondisi1 = self.components["add_mobil_biaya1"].text()    
        
        # tarif kondisi 2
        time_kondisi2 = self.components["add_time2"].text()    
        tarif_motor_kondisi2 = self.components["add_motor_biaya2"].text()    
        tarif_mobil_kondisi2 = self.components["add_mobil_biaya2"].text()

        # tarif kondisi 3
        time_kondisi3 = self.components["add_time3"].text()    
        tarif_motor_kondisi3 = self.components["add_motor_biaya3"].text()    
        tarif_mobil_kondisi3 = self.components["add_mobil_biaya3"].text()
        
        # tarif max
        time_max = self.components["add_time4"].text()    
        tarif_motor_max = self.components["add_motor_biaya4"].text()    
        tarif_mobil_max = self.components["add_mobil_biaya4"].text()    


        # =========== filter ============
        # 1. toleransi boleh terisi/kosong
        
        # 2. tarif dasar motor dan mobil tidak boleh kosong
        # if tarif_motor_perjam == "" or tarif_mobil_perjam == "":
        #     return self.dialogBox(title="Alert", msg="Tarif dasar motor/mobil tidak boleh kosong !")
        
        # query_motor = f"set tarif_dasar='{tarif_motor_perjam}'"
        # query_mobil = f"set tarif_dasar='{tarif_mobil_perjam}'"

        # 3. kondisi tambahan boleh kosong, atau salah satu/keduanya terisi
        # 4. tarif max boleh kosong / terisi
        
        # 5. jika salah satu sub item dari kondisi terisi, maka sub item yg lain harus terisi
        
        # =================== kondisi 1 =========================
        # if not self.filterTarif(time_kondisi1, "1", tarif_motor_kondisi1, tarif_mobil_kondisi1): 
        #     return False
        # else:
        #     query_motor = query_motor +  """, rules='{"4":"1200"}' """
        #     query_mobil = f"set tarif_dasar='{tarif_mobil_perjam}'"
        # =================== end kondisi 1 =========================
        
        
        # =================== kondisi 2 =========================
        # if not self.filterTarif(time_kondisi2, time_kondisi1, tarif_motor_kondisi2, tarif_mobil_kondisi2): return False
        # =================== end kondisi 2 =========================
        

        # =================== tarif max =========================
        # if not self.filterTarif(time_max, time_kondisi2, tarif_motor_max, tarif_mobil_max): return False
        # =================== end tarif max =========================

        # ============== end filter =================

        # create json for rulse based ond tarif input above
        rules_mobil = '{"'+time_kondisi1+'":"'+tarif_mobil_kondisi1+'", "'+time_kondisi2+'":"'+tarif_mobil_kondisi2+'", "'+time_kondisi3+'":"'+tarif_mobil_kondisi3+'", "'+time_max+'":"'+tarif_mobil_max+'"}' 
        
        # set for update
        # query_motor = f"update tarif {query_motor} where id=1;" 
        query_mobil = f"update tarif set toleransi='{toleransi}', rules='{rules_mobil}' where id=2;" 
        print(query_mobil)
        

        # rules_motor = '{"'+time_kondisi1+'":"'+tarif_motor_kondisi1+'"}' 
        
        # disini
        # res = self.exec_query(query_motor + query_mobil)
        
              

    def save_edit_voucher(self):
        
        # get data from edit form
        id = str(self.hidden_id)
        id_pel = self.components["add_voucher_idpel"].text()    
        lokasi = self.components["add_voucher_lokasi"].text()    
        tarif = self.components["add_voucher_tarif"].text()    
        masa_berlaku = self.components["add_voucher_masa_berlaku"].text()    
        jns_kendaraan = self.components["add_voucher_jns_kendaraan"].currentText()

        # run update query
        self.exec_query(f"update voucher set id_pel='{id_pel}', lokasi='{lokasi}', tarif='{tarif}', masa_berlaku='{masa_berlaku}', jns_kendaraan='{jns_kendaraan}' where id="+id)
        
        # close window edit
        self.win.close()

        # reset table value
        query = self.exec_query("SELECT id, id_pel, lokasi, tarif, masa_berlaku, jns_kendaraan FROM voucher", "SELECT")
        cols = 6

        self.fillTable(self.voucher_table, cols, query)
        
        # modal
        dlg = QMessageBox(self.window)
        
        dlg.setWindowTitle("Alert")
        dlg.setText("Data Updated")
        dlg.setIcon(QMessageBox.Information)
        dlg.exec()

    # def save_edit_tarif(self):
    #     # get data from edit form
    #     id = self.components["hidden_id"].text()

    #     pos = self.components["add_tarif_pos"].text()
    #     tarif_perjam = self.components["add_tarif_per_1jam"].text()
    #     tarif_per24jam = self.components["add_tarif_per_24jam"].text()
    #     jns_kendaraan = self.components["add_tarif_jns_kendaraan"].currentText()
        
    #     # run update query
    #     self.exec_query(f"update tarif set no_pos='{pos}', tarif_perjam='{tarif_perjam}', tarif_per24jam='{tarif_per24jam}', jns_kendaraan='{jns_kendaraan}' where id="+id)
        
    #     # call table table list again
    #     self.windowBarAction("kelola tarif")

    def toggleMenu(self, maxWidth, enable, path=""):
        if enable:

            # GET WIDTH
            width = self.left_widget.width()
            maxExtend = maxWidth
            standard = 30

            # SET MAX WIDTH
            if width == 30:
                # change burger icon
                self.burger_menu.setIcon(QIcon(path+"cross.png"))

                widthExtended = maxExtend
            else:
                self.burger_menu.setIcon(QIcon(path+"menu-burger.png"))
                widthExtended = standard

            # ANIMATION
            self.animation = QPropertyAnimation(self.left_widget, b"minimumWidth")
            self.animation.setDuration(400)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QEasingCurve.InOutQuart)
            self.animation.start()

    def updateStyle(self, target=(None,), non_target=(None,)):
        for nt in non_target:
            nt.setProperty("active", False)
            nt.style().unpolish(nt)
            nt.style().polish(nt)
        
        for t in target:
            t.setProperty("active", True)
            t.style().unpolish(t)
            t.style().polish(t)
        
    def Tabs(self, tabs=(None,), stacked_widget=None, index=0):
        self.updateStyle(target=(tabs[0],), non_target=(tabs[1],))
        stacked_widget.setCurrentIndex(index)    
    
    def finish(self):
        self.animating = False

    def windowBarAction(self, q):
        
        try:
            bar_action = q.text().lower()
        except Exception:
            bar_action = q

        margin_top = "margin-top:30px;"
        cell_bg_color = QColor(243,243,243)
        
        # if self.sw_stat == False:
        #     self.sw = self.stacked_widget.width()
        #     self.sw_stat = True
            
        self.stacked_animation.setDuration(600)
        self.stacked_animation.setStartValue(QRect(0, 0, 0, self.stacked_widget.height()))
        self.stacked_animation.setEndValue(QRect(self.stacked_widget.x(), self.stacked_widget.y(), self.stacked_widget.width(), self.stacked_widget.height()))
        self.stacked_animation.setEasingCurve(QEasingCurve.InOutQuart)
        
        match bar_action:
            case "dashboard":
                
                # set active button and label
                self.updateStyle(
                    target=(self.home_btn, self.home_lbl), 
                    non_target=(self.rfid_btn, 
                                self.users_btn, 
                                self.kasir_btn, 
                                self.karcis_btn, 
                                self.tarif_btn, 
                                self.voucher_btn, 
                                self.laporan_btn, 
                                self.logout_btn, 
                                self.rfid_lbl, 
                                self.users_lbl, 
                                self.kasir_lbl, 
                                self.karcis_lbl, 
                                self.tarif_lbl, 
                                self.voucher_lbl, 
                                self.laporan_lbl, 
                                self.logout_lbl)
                )
                
                # solution stacked widget
                self.stacked_widget.setCurrentIndex(0)
                self.stacked_animation.start()

            case "kelola rfid":
                
                # set active button and label
                self.updateStyle(
                    target=(self.rfid_btn, self.rfid_lbl), 
                    non_target=(self.home_btn, 
                                self.users_btn, 
                                self.kasir_btn, 
                                self.karcis_btn, 
                                self.tarif_btn, 
                                self.voucher_btn, 
                                self.laporan_btn, 
                                self.logout_btn, 
                                self.home_lbl, 
                                self.users_lbl, 
                                self.kasir_lbl, 
                                self.karcis_lbl, 
                                self.tarif_lbl, 
                                self.voucher_lbl, 
                                self.laporan_lbl, 
                                self.logout_lbl)
                )

                self.stacked_widget.setCurrentIndex(1)
                self.stacked_animation.start()
            
            case "kelola user":
                # set active button and label
                self.updateStyle(
                    target=(self.users_btn, self.users_lbl), 
                    non_target=(self.rfid_btn, 
                                self.home_btn, 
                                self.kasir_btn, 
                                self.karcis_btn, 
                                self.tarif_btn, 
                                self.voucher_btn, 
                                self.laporan_btn, 
                                self.logout_btn, 
                                self.rfid_lbl, 
                                self.home_lbl, 
                                self.kasir_lbl, 
                                self.karcis_lbl, 
                                self.tarif_lbl, 
                                self.voucher_lbl, 
                                self.laporan_lbl, 
                                self.logout_lbl)
                )
                
                # solution stacked widget
                self.stacked_widget.setCurrentIndex(2)
                self.stacked_animation.start()

            case "kelola kasir":
                # set active button and label
                self.updateStyle(
                    target=(self.kasir_btn, self.kasir_lbl), 
                    non_target=(self.rfid_btn, 
                                self.home_btn, 
                                self.users_btn, 
                                self.karcis_btn, 
                                self.tarif_btn, 
                                self.voucher_btn, 
                                self.laporan_btn, 
                                self.logout_btn, 
                                self.rfid_lbl, 
                                self.home_lbl, 
                                self.users_lbl, 
                                self.karcis_lbl, 
                                self.tarif_lbl, 
                                self.voucher_lbl, 
                                self.laporan_lbl, 
                                self.logout_lbl)
                )

                # solution stacked widget
                self.stacked_widget.setCurrentIndex(3)
                self.stacked_animation.start()

            case "setting karcis":
                # set active button and label
                self.updateStyle(
                    target=(self.karcis_btn, self.karcis_lbl), 
                    non_target=(self.rfid_btn, 
                                self.home_btn, 
                                self.users_btn,
                                self.kasir_btn, 
                                self.tarif_btn, 
                                self.voucher_btn, 
                                self.laporan_btn, 
                                self.logout_btn, 
                                self.rfid_lbl, 
                                self.home_lbl, 
                                self.users_lbl, 
                                self.kasir_lbl, 
                                self.tarif_lbl, 
                                self.voucher_lbl, 
                                self.laporan_lbl, 
                                self.logout_lbl)
                )

                # solution stacked widget
                self.stacked_widget.setCurrentIndex(4)
                self.stacked_animation.start()

            case "kelola tarif":

                # set active button and label
                self.updateStyle(
                    target=(self.tarif_btn, self.tarif_lbl), 
                    non_target=(self.rfid_btn, 
                                self.home_btn, 
                                self.users_btn,
                                self.kasir_btn, 
                                self.karcis_btn, 
                                self.voucher_btn, 
                                self.laporan_btn, 
                                self.logout_btn, 
                                self.rfid_lbl, 
                                self.home_lbl, 
                                self.users_lbl, 
                                self.kasir_lbl, 
                                self.karcis_lbl, 
                                self.voucher_lbl, 
                                self.laporan_lbl, 
                                self.logout_lbl)
                )

                # solution stacked widget
                self.stacked_widget.setCurrentIndex(5)
                self.stacked_animation.start()

            case "kelola voucher":
                # set active button and label
                self.updateStyle(
                    target=(self.voucher_btn, self.voucher_lbl), 
                    non_target=(self.rfid_btn, 
                                self.home_btn, 
                                self.users_btn,
                                self.kasir_btn, 
                                self.tarif_btn, 
                                self.karcis_btn, 
                                self.laporan_btn, 
                                self.logout_btn, 
                                self.rfid_lbl, 
                                self.home_lbl, 
                                self.users_lbl, 
                                self.kasir_lbl, 
                                self.tarif_lbl, 
                                self.karcis_lbl, 
                                self.laporan_lbl, 
                                self.logout_lbl)
                )

                # solution stacked widget
                self.stacked_widget.setCurrentIndex(6)
                self.stacked_animation.start()
 
            case "kelola laporan":

                # set active button and label
                self.updateStyle(
                    target=(self.laporan_btn, self.laporan_lbl), 
                    non_target=(self.rfid_btn, 
                                self.home_btn, 
                                self.users_btn,
                                self.kasir_btn, 
                                self.tarif_btn, 
                                self.voucher_btn, 
                                self.karcis_btn, 
                                self.logout_btn, 
                                self.rfid_lbl, 
                                self.home_lbl, 
                                self.users_lbl, 
                                self.kasir_lbl, 
                                self.tarif_lbl, 
                                self.voucher_lbl, 
                                self.karcis_lbl, 
                                self.logout_lbl)
                )

                # solution stacked widget
                self.stacked_widget.setCurrentIndex(7)
                self.stacked_animation.start()
            
            case "logout":
                self.closeWindow(self.window)
                self.Login()
            
            case default:
                pass    
    
    def editData(self, row, table, target):
        # r = table.currentRow()
        id = table.item(row, 0).text()
        
        margin_top = "margin-top:30px;"
        
        # show edit form here
        match target:
            case "rfid":
                sub_window_setter = { "title": "Edit RFID", "style":self.bg_white, "size":(600, 400) }

                # components
                components_setter = [
                                    {
                                        "name":"hidden_id",
                                        "category":"lineEdit",
                                    },
                                    {
                                        "name":"lbl_add_rfid",
                                        "category":"label",
                                        "text": "RFID",
                                        "style":self.primary_lbl
                                    },
                                    {
                                        "name":"add_rfid",
                                        "category":"lineEdit",
                                        "style":self.primary_input
                                    },
                                    {
                                        "name":"lbl_add_rfid_owner",
                                        "category":"label",
                                        "text": "Name",
                                        "style":self.primary_lbl + margin_top
                                    },
                                    {
                                        "name":"add_rfid_owner",
                                        "category":"lineEdit",
                                        "style":self.primary_input
                                    },
                                    {
                                        "name":"btn_add_rfid",
                                        "category":"pushButton",
                                        "text": "Save",
                                        "clicked": {
                                                "method_name": self.save_edit_rfid
                                        },
                                        "style": self.primary_button
                                    }
                                ]

                self.SubWinVerticalForm(sub_window_setter, components_setter, "add-mdi")

                # run query based on id
                res = self.exec_query("select * from rfid where id="+id, "select")
                
                
                # put data from DB into edit form
                self.components["hidden_id"].setText(str(res[0][0]))
                self.components["hidden_id"].hide()

                self.components["add_rfid"].setText(res[0][1])
                self.components["add_rfid_owner"].setText(res[0][2])

            case "users":
                sub_window_setter = { "title": "Edit User", "style":self.bg_white, "size":(600, 700) }

                # components
                components_setter = [
                                    {
                                        "name":"hidden_id",
                                        "category":"lineEdit",
                                    },
                                    {
                                        "name":"lbl_add_uname",
                                        "category":"label",
                                        "text": "Username",
                                        "style":self.primary_lbl
                                    },
                                    {
                                        "name":"add_uname",
                                        "category":"lineEdit",
                                        "style":self.primary_input
                                    },
                                    {
                                        "name":"lbl_add_pass",
                                        "category":"label",
                                        "text": "Password",
                                        "style":self.primary_lbl + margin_top
                                    },
                                    {
                                        "name":"add_pass",
                                        "category":"lineEdit",
                                        "style":self.primary_input
                                    },
                                    {
                                        "name":"lbl_retype_pass",
                                        "category":"label",
                                        "text": "Retype Password",
                                        "style":self.primary_lbl + margin_top
                                    },
                                    {
                                        "name":"retype_pass",
                                        "category":"lineEdit",
                                        "style":self.primary_input
                                    },
                                    {
                                        "name":"lbl_user_level",
                                        "category":"label",
                                        "text": "Level",
                                        "style":self.primary_lbl + margin_top
                                    },
                                    {
                                        "name":"input_user_level",
                                        "category":"comboBox",
                                        "items": ["Admin","Pegawai", "Kasir"],
                                        "style":self.primary_combobox
                                    },
                                    {
                                        "name":"btn_add_user",
                                        "category":"pushButton",
                                        "text": "Save",
                                        "clicked": {
                                                "method_name": self.save_edit_user
                                        },
                                        "style": self.primary_button
                                    }
                                ]

                self.SubWinVerticalForm(sub_window_setter, components_setter)
                
                # run query based on id
                res = self.exec_query("select id, username, user_level from users where id="+id, "select")
                
                # put data from DB into edit form
                self.components["hidden_id"].setText(str(res[0][0]))
                self.components["hidden_id"].hide()

                self.components["add_uname"].setText(res[0][1])
                self.components["input_user_level"].setCurrentIndex( self.getComboIndex(self.components["input_user_level"],res[0][2]) )

            case "kasir":
                sub_window_setter = { "title": "Edit Kasir", "style":self.bg_white, "size":(800, 900) }

                # components
                components_setter = [{
                                        "name":"hidden_id",
                                        "category":"lineEdit",
                                    },
                                    {
                                        "name":"lbl_add_nik",
                                        "category":"label",
                                        "text": "NIK",
                                        "style":self.primary_lbl + margin_top
                                    },
                                    {
                                        "name":"add_nik",
                                        "category":"lineEdit",
                                        "style":self.primary_input
                                    },
                                    {
                                        "name":"lbl_add_nama",
                                        "category":"label",
                                        "text": "Nama",
                                        "style":self.primary_lbl + margin_top
                                    },
                                    {
                                        "name":"add_nama",
                                        "category":"lineEdit",
                                        "style":self.primary_input
                                    },
                                    {
                                        "name":"lbl_add_hp",
                                        "category":"label",
                                        "text": "Nomor HP",
                                        "style":self.primary_lbl + margin_top
                                    },
                                    {
                                        "name":"add_hp",
                                        "category":"lineEdit",
                                        "style":self.primary_input
                                    },
                                    {
                                        "name":"lbl_add_alamat",
                                        "category":"label",
                                        "text": "Alamat",
                                        "style":self.primary_lbl + margin_top
                                    },
                                    {
                                        "name":"add_alamat",
                                        "category":"lineEdit",
                                        "style":self.primary_input
                                    },
                                    {
                                        "name":"lbl_add_jam_masuk",
                                        "category":"label",
                                        "text": "Jam Masuk",
                                        "style":self.primary_lbl + margin_top
                                    },
                                    {
                                        "name":"add_jam_masuk",
                                        "category":"lineEdit",
                                        "style":self.primary_input
                                    },
                                    {
                                        "name":"lbl_add_jam_keluar",
                                        "category":"label",
                                        "text": "Jam Keluar",
                                        "style":self.primary_lbl + margin_top
                                    },
                                    {
                                        "name":"add_jam_keluar",
                                        "category":"lineEdit",
                                        "style":self.primary_input
                                    },
                                    {
                                        "name":"lbl_add_nmr_pos",
                                        "category":"label",
                                        "text": "Nomor Pos/Gate",
                                        "style":self.primary_lbl + margin_top
                                    },
                                    {
                                        "name":"add_nmr_pos",
                                        "category":"lineEdit",
                                        "style":self.primary_input
                                    },
                                    {
                                        "name":"btn_add_kasir",
                                        "category":"pushButton",
                                        "text": "Save",
                                        "clicked": {
                                                "method_name": self.save_edit_kasir
                                        },
                                        "style": self.primary_button
                                    },
                                    {
                                        "name":"lbl_space",
                                        "category":"label",
                                        "min_height":20
                                    }
                                ]

                self.SubWinVerticalForm(sub_window_setter, components_setter)

                # run query based on id
                res = self.exec_query("select * from kasir where id="+id, "select")
                
                # put data from DB into edit form
                self.components["hidden_id"].setText(str(res[0][0]))
                self.components["hidden_id"].hide()

                self.components["add_nik"].setText(res[0][1])
                self.components["add_nama"].setText(res[0][2])
                self.components["add_hp"].setText(res[0][3])
                self.components["add_alamat"].setText(res[0][4])
                self.components["add_jam_masuk"].setText(res[0][5])
                self.components["add_jam_keluar"].setText(res[0][6])
                self.components["add_nmr_pos"].setText(res[0][7])

            case "gate":
                sub_window_setter = { "title": "Edit Pos/Gate", "style":self.bg_white, "size":(600, 650) }

                # components
                components_setter = [{
                                        "name":"hidden_id",
                                        "category":"lineEdit",
                                    },
                                    {
                                        "name":"lbl_add_pos",
                                        "category":"label",
                                        "text": "No Pos/Gate",
                                        "style":self.primary_lbl + margin_top
                                    },
                                    {
                                        "name":"add_pos",
                                        "category":"lineEdit",
                                        "style":self.primary_input
                                    },
                                    {
                                        "name":"lbl_add_tipe_pos",
                                        "category":"label",
                                        "text": "Tipe Pos/Gate",
                                        "style":self.primary_lbl + margin_top
                                    },
                                    {
                                        "name":"add_tipe_pos",
                                        "category":"comboBox",
                                        "items": ["Masuk", "Keluar"],
                                        "style":self.primary_combobox
                                    },
                                    {
                                        "name":"lbl_add_jenis_kendaraan",
                                        "category":"label",
                                        "text": "Jenis Kendaraan",
                                        "style":self.primary_lbl + margin_top
                                    },
                                    {
                                        "name":"add_jenis_kendaraan",
                                        "category":"comboBox",
                                        "items": ["Motor", "Mobil"],
                                        "style":self.primary_combobox
                                    },
                                    {
                                        "name":"lbl_add_ipcam",
                                        "category":"label",
                                        "text": "IP Cam",
                                        "style":self.primary_lbl + margin_top
                                    },
                                    {
                                        "name":"add_ipcam",
                                        "category":"lineEdit",
                                        "style":self.primary_input
                                    },
                                    {
                                        "name":"btn_add_pos",
                                        "category":"pushButton",
                                        "text": "Save",
                                        "clicked": {
                                                "method_name": self.save_edit_gate
                                        },
                                        "style": self.primary_button
                                    }
                                ]

                self.SubWinVerticalForm(sub_window_setter, components_setter)
                
                # run query based on id
                res = self.exec_query("select * from gate where id="+id, "select")
                
                # put data from DB into edit form
                self.components["hidden_id"].setText(str(res[0][0]))
                self.components["hidden_id"].hide()

                self.components["add_pos"].setText(res[0][1])

                # get index combobox based on text and set as current index
                
                self.components["add_tipe_pos"].setCurrentIndex(  self.getComboIndex(self.components["add_tipe_pos"],res[0][2]) )
                self.components["add_jenis_kendaraan"].setCurrentIndex( self.getComboIndex(self.components["add_jenis_kendaraan"],res[0][3]) )
                
                self.components["add_ipcam"].setText(res[0][4])
                
            case "tarif":
                sub_window_setter = { "title": "Edit Aturan Tarif Parkir", "style":self.bg_white, "size":(600, 600) }

                # components
                components_setter = [{
                                        "name":"hidden_id",
                                        "category":"lineEdit",
                                    },
                                    {
                                        "name":"lbl_add_tarif_pos",
                                        "category":"label",
                                        "text": "Nomor Pos",
                                        "style":self.primary_lbl + margin_top
                                    },
                                    {
                                        "name":"add_tarif_pos",
                                        "category":"lineEdit",
                                        "style":self.primary_input
                                    },
                                    {
                                        "name":"lbl_add_tarif_per_1jam",
                                        "category":"label",
                                        "text": "Tarif / jam",
                                        "style":self.primary_lbl + margin_top
                                    },
                                    {
                                        "name":"add_tarif_per_1jam",
                                        "category":"lineEdit",
                                        "style":self.primary_input
                                    },
                                    {
                                        "name":"lbl_add_tarif_per_24jam",
                                        "category":"label",
                                        "text": "Tarif / 24 jam",
                                        "style":self.primary_lbl + margin_top
                                    },
                                    {
                                        "name":"add_tarif_per_24jam",
                                        "category":"lineEdit",
                                        "style":self.primary_input
                                    },
                                    {
                                        "name":"lbl_add_tarif_jns_kendaraan",
                                        "category":"label",
                                        "text": "Jenis Kendaraan",
                                        "style":self.primary_lbl + margin_top
                                    },
                                    {
                                        "name":"add_tarif_jns_kendaraan",
                                        "category":"comboBox",
                                        "items":["Motor", "Mobil"],
                                        "style":self.primary_combobox
                                    },
                                    {
                                        "name":"btn_add_tarif",
                                        "category":"pushButton",
                                        "text": "Save",
                                        "clicked": {
                                                "method_name": self.save_edit_tarif
                                        },
                                        "style": self.primary_button
                                    }
                                ]

                self.SubWinVerticalForm(sub_window_setter, components_setter)
                
                # run query based on id
                res = self.exec_query("select * from tarif where id="+id, "select")
                
                # put data from DB into edit form
                self.components["hidden_id"].setText(str(res[0][0]))
                self.components["hidden_id"].hide()

                self.components["add_tarif_pos"].setText(res[0][1])
                self.components["add_tarif_per_1jam"].setText(str(res[0][2]))
                self.components["add_tarif_per_24jam"].setText(str(res[0][3]))
                
                self.components["add_tarif_jns_kendaraan"].setCurrentIndex( self.getComboIndex(self.components["add_tarif_jns_kendaraan"],res[0][4]) )
            case default:
                pass

    def deleteData(self, target):
        # r = table.currentRow()
        # id = table.item(row, 0).text()
        id = str(self.hidden_id)

        # modal
        dlg = QMessageBox(self.window)
        
        dlg.setWindowTitle("Alert")
        dlg.setText("Hapus Data ?")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setIcon(QMessageBox.Question)
        button = dlg.exec()

        if button == QMessageBox.Yes:
            res = self.exec_query(f"delete from {target} where id="+id)

            if res:
                self.hidden_id = -1
                match target.lower():
                    
                    case "rfid":
                        
                        # reset table value
                        query = self.exec_query("SELECT id, rfid, nama FROM rfid order by nama", "SELECT")
                        rows_count = len(query)
                        cols = 3
                        self.fillTable(self.rfid_table, cols, query, rows_count)
                        self.logger.info("RFID delete success")

                    case "users":
                        
                        # reset table value
                        query = self.exec_query("SELECT id, username, user_level FROM users", "SELECT")
                        rows_count = len(query)
                        cols = 3
                        self.fillTable(self.user_table, cols, query, rows_count)
                        self.logger.info("User delete success")
                       
                    case "kasir":

                        # reset table value
                        query = self.exec_query("SELECT id, nik, nama, hp, alamat, jm_masuk, jm_keluar, no_pos FROM kasir", "SELECT")
                        rows_count = len(query)
                        cols = 8
                        self.fillTable(self.kasir_table, cols, query, rows_count)
                        self.logger.info("Kasir delete success")
                    
                    case "voucher":
                        
                        # reset table value
                        query = self.exec_query("SELECT id, id_pel, lokasi, tarif, masa_berlaku, jns_kendaraan FROM voucher", "SELECT")
                        rows_count = len(query)
                        cols = 6
                        self.fillTable(self.voucher_table, cols, query, rows_count)
                        self.logger.info("Voucher delete success")

                    case default:
                        pass     
                
    def printData(self, target):
        match target.lower():
            case "voucher":
                
                try:
                    # init printer
                    p = Usb(0x0FE6, 0x811E , timeout = 0, in_ep = 0x81, out_ep = 0x01)

                    # get data voucher based on id
                    id = self.hidden_id
                    res = self.exec_query("select * from voucher where id="+id, "select")
                
                    # Print text
                    id_pel = res[0][1]
                    lokasi = res[0][2]
                    tarif = res[0][3]
                    date = str(res[0][4]).split("-")
                    masa_berlaku = date[2] +"-"+ date[1] +"-"+ date[0]
                    jns_kendaraan = res[0][5]
                    
                    p.set('center')
                    p.text("VOUCHER PARKIR\n")
                    p.text(lokasi + "\n")
                    p.text("------------------------------------\n\n")
                    
                    p.text("ID PEL: " + id_pel + "\n")
                    p.text("SALDO: " + str(tarif) + "\n")
                    p.text("JENIS KENDARAAN: " + jns_kendaraan + "\n")
                    p.text("MASA BERLAKU: " + masa_berlaku + "\n")
                    
                    p.text("\n------------------------------------\n")
                    
                    p.barcode("{B" + id_pel, "CODE128", height=128, width=3, function_type="B")
                    
                    p.text("\n------------------------------------\n")
        
                    # Cut paper
                    p.cut()
                    p.close()

                except Exception as e:
                    # modal
                    dlg = QMessageBox(self.window)
                    
                    dlg.setWindowTitle("Alert")
                    dlg.setText(str(e))
                    dlg.setIcon(QMessageBox.Warning)
                    dlg.exec()
                        
                
            case default:
                pass

    def dialogBox(self, title="", msg=""):
        
        # init dialog box
        dlg = QMessageBox(self.window)
        dlg.setWindowTitle( title )
        dlg.setText( msg )
        dlg.setIcon(QMessageBox.Information)
        dlg.exec()  