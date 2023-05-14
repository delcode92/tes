import sys, json, psycopg2, os, math, threading, logging, webbrowser
from logging.handlers import TimedRotatingFileHandler

from client.client_service import Client
from PyQt5.QtWidgets import (QMdiArea, QMessageBox, QMdiSubWindow, QWidget, QMainWindow, QVBoxLayout, QHeaderView, QLabel, QPushButton, QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import Qt, QRect,QPropertyAnimation, QEasingCurve, QDateTime
from PyQt5.QtGui import QColor, QIcon
from configparser import ConfigParser
from escpos.printer import Usb
from datetime import datetime, timedelta
from fpdf import FPDF

# from framework import View

class Controller(Client):
    def __init__(self) -> None:
        # self.Util.__init__(self)
        
        self.initDebug()

        # active db cursor 
        self.connect_to_postgresql()
        self.sw_stat = False
        
        # radio button laporan
        self.r_menit = False
        self.r_jam = False

        
        # default value
        self.selected_tarif = "other"

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

            if type.lower() == "":    
                return True

        except Exception as e:
            self.logger.info("\nexecute query fail")
            self.logger.error( str(e) )


        if type.lower() =="select":
            data = self.db_cursor.fetchall()
            return data
        
        elif type.lower() =="cols_res":
            cols = [desc[0] for desc in self.db_cursor.description]
            data = self.db_cursor.fetchall()
            return cols,data
            

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
    
    def calculate_parking_payment(self, rules, parking_seconds):
        
        # get max key:val
        lastKey,lastValue = rules.popitem()
        lastKey = int(lastKey)
        lastValue = int(lastValue)
        
        # loop all keys in dictionary
        for k,v in rules.items():

            key_rules = int(k)
            # val_rules = int(v)
        
            rate_seconds = key_rules * 3600
            # rate_price = rules[k];

            
            if parking_seconds <= rate_seconds and parking_seconds != (lastKey*3600) :
                each_loop_price = 0

                for k2,v2 in rules.items():
                    k2_rules = int(k2)
                    rp = int(v2)
                    
                    # add price until `key`
                    # rp = rules[k2_rules]
                    each_loop_price += rp
                    
                    if key_rules == k2_rules: break
                
                total_payment = each_loop_price
                return total_payment
            
            elif parking_seconds > (lastKey*3600):
                days = math.floor( parking_seconds / (lastKey*3600) )
                total_payment = days * lastValue
            
                remaining_time = parking_seconds - (days*lastKey*60*60)
                
                if remaining_time > 0:
                    
                    total_payment = total_payment + self.calculate_parking_payment(rules, remaining_time)

                return total_payment
            
            elif parking_seconds == (lastKey*3600):
                total_payment = (parking_seconds / (lastKey*3600)) * lastValue

                return total_payment

    def getPrice(self):
        """ this method execute when press enter in barcode lineEdit """

        jns_kendaraan = ""
        status_parkir = ""
        self.diff_formatted = ""
        try:

            # =================== base information ========================
            # get time based on barcode
            barcode = self.components["barcode_transaksi"].text()
            q_karcis_count = self.exec_query(f"select count(*) as jum from karcis where barcode='{barcode}'", "select")
            q_voucher_count = self.exec_query(f"select count(*) as jum from voucher where id_pel='{barcode}'", "select")

            # print("==>val: ", query_karcis[0], type(query_karcis[0]))
            
            # jika ada data
            if int(q_karcis_count[0][0]) > 0:
                query_karcis = self.exec_query(f"select datetime, date_keluar, jenis_kendaraan, status_parkir from karcis where barcode='{barcode}'", "select")
               
                jns_kendaraan = query_karcis[0][2].capitalize()
                self.components["jns_kendaraan"].setText( jns_kendaraan )
               
                if query_karcis[0][3]:
                    status_parkir = "LUNAS"
                elif not query_karcis[0][3]:
                    status_parkir = "BELUM LUNAS"
                
                self.components["ket_status"].setText( status_parkir )


                # get toleransi
                query = self.exec_query(f"select toleransi, tipe_tarif, rules from tarif where jns_kendaraan='{jns_kendaraan}' or jns_kendaraan='{jns_kendaraan.lower()}'", "select")
                tolerance = int(query[0][0]) * 60

                # parse rules
                rules = json.loads( query[0][2] )

                # lama parkir ==> (datetime masuk - current time)
                self.time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.time_now = datetime.strptime(self.time_now, '%Y-%m-%d %H:%M:%S')
                barcode_time = query_karcis[0][0].replace(tzinfo=None)

                diff = self.time_now - barcode_time
                parking_seconds = int( diff.total_seconds() )

                self.diff_formatted = str(timedelta(seconds = parking_seconds))

                print("==> lama parkir: ", self.diff_formatted)

                # check apakah lama parkir melewati batas toleransi ?
                if parking_seconds > tolerance:
                    
                    # cek kategori tarif
                    if query[0][1] == "other":
                        tot_pay = self.calculate_parking_payment(rules, parking_seconds)
                        
                        self.components["tarif_transaksi"].setText( str(tot_pay) )

                    elif query[0][1] == "flat":
                        # tarif flat artinya tarif konstan
                        # get first key:value from json rules
                        key,value = next( iter(rules.items()) )

                        # set lineEdit
                        self.components["tarif_transaksi"].setText( str(value) )

                    
                    elif query[0][1] == "progresif":
                        # tarif artinya kelipatan dari jam yg di set
                        h1,value = next( iter(rules.items()) )
                        h1 = int(h1)
                        value = int(value)

                        ph = math.floor(parking_seconds/3600)
                        h1_seconds = h1 * 60 * 60
                        final_price = 0

                        if parking_seconds>h1_seconds:
                            mod = parking_seconds % 3600

                            # exact multiple
                            if mod==0:
                                final_price = ph * value 
                            elif mod>0:
                                ph =math.floor( ph/h1 )
                                final_price = ( ph  * value) + value
                                
                        elif parking_seconds <= h1_seconds:
                            final_price = value
                        
                        # set lineEdit
                        self.components["tarif_transaksi"].setText( str(final_price) )

                elif parking_seconds < tolerance:
                    self.components["ket_status"].setText("FREE")
                    self.components["tarif_transaksi"].setText("0")
                    
                # total_hours = math.ceil(diff.total_seconds()/3600)
                
                # print("====================")
                # print("TH", total_hours, type(total_hours))
                # print("jns kendaraan:", jns_kendaraan)
                # print("====================\n\n")
            
                # # get base price from db
                # base_price = self.exec_query(f"select tarif_perjam,tarif_per24jam from tarif where jns_kendaraan='{jns_kendaraan}'", "select")
                # base_price_perjam = base_price[0][0] 
                # base_price_per24jam = base_price[0][1] 
                
                # if total_hours==0:
                #     jam = 1
                #     price = jam * base_price_perjam
                #     print("================")
                #     print(jam, "jam")
                #     print(price, "Rupiah")
                #     print("================\n\n")
                
                # elif total_hours<24 and total_hours>0:
                #     price = total_hours * base_price_perjam
                    
                #     print("================")
                #     print(total_hours, "jam")
                #     print(price, "Rupiah")
                #     print("================\n\n")
                
                # elif total_hours>24:
                #     hari = math.floor(total_hours/24)
                #     jam = total_hours-(hari*24)

                #     price = (hari*base_price_per24jam) + (jam*base_price_perjam)

                #     print("================")
                #     print(hari, "hari")
                #     print(jam, "jam")
                #     print(price, "Rupiah")
                #     print("================\n\n")
                
                # # set value to textbox
                # self.components["jns_kendaraan"].setText( jns_kendaraan )
                # self.components["ket_status"].setText( str(status_parkir) )
                
                # # just show tarif and enable button if "BELUM LUNAS"
                # if status_parkir == "BELUM LUNAS":
                #     self.components["tarif_transaksi"].setText( str(price) )

            if int(q_voucher_count[0][0]) > 0:
                self.components["jns_kendaraan"].setText("")
                self.components["ket_status"].setText( "VOUCHER" )
                self.components["tarif_transaksi"].setText("0")
                print("==> cari di voucher")

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
            if self.diff_formatted == "" : self.diff_formatted = "00:00:00"

            self.exec_query(f"update karcis set status_parkir=true, tarif='{tarif}', date_keluar='{dt_keluar}', lama_parkir='{self.diff_formatted}', jns_transaksi='casual' where barcode='{barcode}'")
            
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

    def check_tarif_type(self, tt):
        try:
            self.selected_tarif = tt.text()
        except:
            self.selected_tarif = tt

        if self.selected_tarif == "progresif" or self.selected_tarif == "flat":
            # disabled others input
            self.components["widget_container_biaya2"].setStyleSheet("background-color:#636e72;")
            self.components["widget_container_biaya3"].setStyleSheet("background-color:#636e72;")
            self.components["widget_container_biaya4"].setStyleSheet("background-color:#636e72;")

            self.components["widget_container_biaya2"].setEnabled(False)
            self.components["widget_container_biaya3"].setEnabled(False)
            self.components["widget_container_biaya4"].setEnabled(False)
            
        elif self.selected_tarif == "other":
            self.components["widget_container_biaya2"].setStyleSheet("border: 1px solid #b2bec3; background-color:none;")
            self.components["widget_container_biaya3"].setStyleSheet("border: 1px solid #b2bec3; background-color:none;")
            self.components["widget_container_biaya4"].setStyleSheet("border: 1px solid #b2bec3; background-color:none;")

            self.components["widget_container_biaya2"].setEnabled(True)
            self.components["widget_container_biaya3"].setEnabled(True)
            self.components["widget_container_biaya4"].setEnabled(True)
        
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

    def getBetween(self, hours_before, hours_after, max_hours, price):
        hours_before = int(hours_before)
        hours_after = int(hours_after)
        max_hours = int(max_hours)

        json_txt = ""
        h = 0
        
        for i in range(24):
            
            h = h + hours_after + hours_before if h==0 else h + hours_before
            
            if h < max_hours:
                json_txt = json_txt + f'"{h}":"{price}",'
            
            elif h >= max_hours:
                json_txt = json_txt[:-1]  
                return json.loads("{"+json_txt+"}")
                # return json_txt

    def add_kendaraan(self):
        
        kendaraan = self.components["inp_jns_kend"].text().lower()
        denda = self.components["inp_denda_kend"].text()
        c = self.exec_query(f"select count(jns_kendaraan) as jum from tarif where jns_kendaraan='{kendaraan}'","select")

        if c[0][0] == 0:
            # save to tbl tarif
            res = self.exec_query(f"select * from tarif where id=1","select")
            rules = res[0][1]
            toleransi = res[0][3]
            tipe_tarif = res[0][4]
            base_rule = res[0][5]

            query = self.exec_query(f"insert into tarif (rules, jns_kendaraan, toleransi, tipe_tarif, base_rules, denda) values ('{rules}', '{kendaraan}', {toleransi}, '{tipe_tarif}', '{base_rule}', {denda})")
            
            if query:
                self.tarif_stack.removeWidget(self.tarif_content2)
                self.tarif_content2 = QWidget()
                self.tarif_content2_lay = QVBoxLayout()
                self.tarif_content2.setLayout( self.tarif_content2_lay )
                self.tarif_content2_lay.setContentsMargins(25,25,25,25)

                self.tarif_stack.addWidget( self.tarif_content2 )

                self.tarif_components_setter = [{
                                        "name":"main_kendaraan",
                                        "category":"widget",
                                        "layout": "VBoxLayout",
                                        "max_width":700,
                                        "style":self.block_children,
                                        "children":[]
                                    }]
                self.tarif_components_setter[0]["children"] = self.getKendaraanList()


                self.CreateComponentLayout(self.tarif_components_setter, self.tarif_content2_lay)
                self.tarif_content2_lay.addStretch(1)

                self.tarif_stack.setCurrentIndex( 1 )
                
                self.dialogBox(title="Alert", msg=f"Berhasil ditambah")

        elif c[0][0] > 0:
            self.dialogBox(title="Alert", msg=f"Jenis Kendaraan ==> {kendaraan} sudah ada !")

    def getKendaraanForm(self, component_setter=""):
        res = self.exec_query(f"select jns_kendaraan, base_rules from tarif order by id", "select")
        
        # parse base rules ==> get hours
        base_rules = json.loads( str(res[0][1]) )
        json_keys = [] 

        # extract ket-value from json
        for key in base_rules.keys():
            json_keys.append( str(key) )

        for j in range(4):
            l = []
            l_jam = []
            txt_jam = ""
            key = str(json_keys[j])
            n = j+1
            
            # sub_container2_biaya1
            # sub_container2_biaya2
            # sub_container2_biaya3
            # sub_container2_biaya4
            
            # create label & time children list
            if j==0:
                txt_jam = "jam pertama"
            elif j==1 or j==2 :
                txt_jam = "jam berikutnya"
            elif j==3:
                txt_jam = "jam"
            
            l_jam =  [{
                                "name":"lbl",
                                "category":"label",
                                "min_width":140 if j==3 else 0,
                                "text": "Tarif maksimal per " if j==3 else "Tarif: ",
                                "style":self.primary_lbl + "max-width:50px; border: none;"
                            },
                            {
                                "name":f"add_time{n}",
                                "category":"spinbox",
                                "range":(0,24),
                                "value":f"{key}",
                                "style":self.primary_spinbox 
                            },
                            {
                                "name":"lbl",
                                "category":"label",
                                "text":txt_jam ,
                                "style":self.primary_lbl + "border: none;"
                            }]
            
            for i in range( len(res) ):
                jns_kendaraan = res[i][0]
                jns_kendaraan = jns_kendaraan.lower()

                # parse base rules based on key
                br = json.loads( str(res[i][1]) )
                biaya = br[ key ] 

                # create children list
                l = l + [{
                        "name":"lbl",
                        "category":"label",
                        "text":f"{jns_kendaraan}(Rp):",
                        "style":self.primary_lbl + "border: none; margin-left:6px;"
                    },
                    {
                        "name":f"add_{jns_kendaraan}_biaya{n}",
                        "category":"lineEditInt",
                        "text": f"{biaya}", # ==> "text": tarif_motor_kondisi1,
                        "style":self.primary_input 
                    }]
                

            # jam 
            self.tarif_form_setter[1+n]["children"][0]["children"] = l_jam 
            
            self.tarif_form_setter[1+n]["children"][1]["children"] = l
            

    def getKendaraanList(self):
        res = self.exec_query(f"select jns_kendaraan, denda, id from tarif order by id", "select")
        l = []

        for i in range( len(res) ):
            l = l + [{
                        "name":f"kendaraan{i}_wgt",
                        "category":"widget",
                        "layout": "HBoxLayout",
                        "style":"border:none;",
                        "children":[
                            {
                                "name":f"nm_kend{i}",
                                "category":"lineedit",
                                "text":str( res[i][0] ).capitalize(),
                                "max_width":200,
                                "style":self.primary_input
                            },
                            {
                                "name":f"denda{i}",
                                "category":"lineedit",
                                "text":str( res[i][1] ),
                                "max_width":200,
                                "style":self.primary_input
                            },
                            {
                                "name":f"update{i}",
                                "category":"pushButton",
                                "text":"update",
                                "max_width":100,
                                "style":self.primary_update_button,
                                "clicked": {
                                    "method_name": self.update_denda, 
                                    "arguments": ( i, str( res[i][2] ) )                                 }
                            }
                        ]
                    }]


        l_header = [{
                        "name":"header_wgt",
                        "category":"widget",
                        "layout": "HBoxLayout",
                        "style":"border:none;",
                        "children":[
                            {
                                "name":"header1",
                                "category":"label",
                                "text":"JENIS KENDARAAN",
                                "style":self.primary_lbl + "margin-left: 40px;"
                            },
                            {
                                "name":"header1",
                                "category":"label",
                                "text":"DENDA",
                                "style":self.primary_lbl + "margin-left: 60px;"
                            },
                            {
                                "name":"header1",
                                "category":"label",
                                "text":"ACTION",
                                "style":self.primary_lbl + "margin-left: 80px;"
                            }
                        ]
                    }]
        
        l_bottom = [{
                        "name":"add_kendaraan_wgt",
                        "category":"widget",
                        "layout": "HBoxLayout",
                        "style":"border:none;",
                        "children":[
                            {
                                "name":"inp_jns_kend",
                                "category":"lineEdit",
                                "max_width":200,
                                "style":self.primary_input
                            },
                            {
                                "name":"inp_denda_kend",
                                "category":"lineEditint",
                                "max_width":200,
                                "style":self.primary_input
                            },
                            {
                                "name":"add_kendaraan",
                                "category":"pushButton",
                                "text":"ADD",
                                "max_width":100,
                                "style":self.primary_add_button,
                                "clicked": {
                                    "method_name": self.add_kendaraan
                                }
                            }
                        ]
                    }]

        return l_header + l + l_bottom

        

    def update_denda( self, args ):
        elem_id, row_id= args

        jns_kendaraan = self.components[f"nm_kend{elem_id}"].text()
        denda = self.components[f"denda{elem_id}"].text()

        query = self.exec_query(f"update tarif set jns_kendaraan='{jns_kendaraan}', denda={denda} where id={row_id}")
       
        if query: self.dialogBox(title="Alert", msg=f"Berhasil diupdate")

        # set tarif form
        self.tarif_stack.removeWidget(self.tarif_content1)
        # self.tarif_content1.deleteLater()

        self.tarif_content1 = QWidget()
        # self.tarif_content1.setStyleSheet("border: 2px solid red;")
        # self.tarif_content1_lay = None
        self.tarif_content1_lay = QVBoxLayout()
        self.tarif_content1.setLayout( self.tarif_content1_lay )
        self.tarif_content1_lay.setContentsMargins(25,0,25,0)
        # self.tarif_content1_lay.addWidget(self.form_container)

        self.tarif_content1.setMaximumWidth(800)
        self.tarif_content1.setStyleSheet("margin-left: 25px; background:#222b45; border: 1px solid #b2bec3;")
        self.tarif_content1_lay.setContentsMargins(25,25,25,25)

        self.tarif_stack.insertWidget( 0, self.tarif_content1 )

        # components
        
        # self.tarif_form_setter 

        self.getKendaraanForm()
        
        # self.tarif_stack.update()
        self.CreateComponentLayout( self.tarif_form_setter, self.tarif_content1_lay )
        # self.components["widget_tipe_tarif"].setStyleSheet("background:#222b45;")

    def set_tarif(self):
        
        # get tolerance
        tolerance = self.components["add_toleransi"].text()
        
        ### create query for update

        # loop based on jenis kendaraan
        q_jkendaraan = self.exec_query(f"select id,jns_kendaraan from tarif order by id", "select")
        base_rules = ""
        final_query = ""

        for i in range( len(q_jkendaraan) ):
            id_kendaraan = q_jkendaraan[i][0]
            j_kendaraan = q_jkendaraan[i][1]
            j_kendaraan = j_kendaraan.lower()

            # loop based on row form
            for i in range(4):
                n = i+1
                jam = self.components[f'add_time{n}'].text()
                tarif = self.components[f'add_{j_kendaraan}_biaya{n}'].text()

                base_rules = base_rules + f'"{jam}":"{tarif}",'

            # remove last comma from base rules string
            base_rules = base_rules[:-1]
            
            # convert base rules to json
            base_rules = "{"+base_rules+"}"
            br = json.loads(base_rules)
            br_key = list(br.keys()) 

            # =============== set rules ================
            k1 = br_key[0]
            v1 = br[ str(k1) ]
            
            k2 = int(k1) + int(br_key[1])
            v2 = br[ br_key[1] ]
            
            k3 = int(k2) + int(br_key[2])
            v3 = br[ br_key[2] ]

            rules = { str(k1):str(v1), str(k2):str(v2), str(k3):str(v3) }
            
            h_before = int(br_key[2])
            h_after = k2 + int(br_key[2])
            max_hour = int(br_key[-1])
            price = int( br[ str(br_key[1]) ] )

            # print("h_before", h_before)
            # print("h_after", h_after)
            # print("max_hour", max_hour)
            # print("price", price)

            value_between = self.getBetween(h_before, h_after, max_hour, price)
            rules.update(value_between)
            
            max_key = str(max_hour)
            max_key_val = {max_key:br[max_key]}
            
            rules.update(max_key_val)
            rules = json.dumps(rules)
            
            # print("==> rules: ", rules)

            # print("==> between:", value_between)
            final_query = final_query + f"update tarif set rules='{rules}', toleransi={tolerance}, tipe_tarif='{self.selected_tarif}', base_rules='{base_rules}' where id={id_kendaraan};"

            # clear
            base_rules = ""

        
        res = self.exec_query(final_query)

        if res:
            self.dialogBox(title="Alert", msg="Tarif berhasil diupdate")

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


    def detailPopUp(self, form_type="", form_size=(400,400)):
        
        if self.hidden_id != -1:
            yellow_font = "color: #ffeaa7;"
            id = str(self.hidden_id)

            match form_type.lower():
                case "karcis":
                    cols,res = self.exec_query("select * from karcis where id="+id, "cols_res")
                    img_masuk = str( res[0][cols.index('images_path')] )
                    # img_keluar = str( res[0][cols.index('images_path_keluar')] )

                    img_masuk = "" if img_masuk=="" or img_masuk==None else "./cap/"+img_masuk+".jpg"
                    # img_keluar = "" if img_keluar=="" or img_keluar==None else "./cap/"+img_keluar+".jpg"

                    
                    components = [
                                    {
                                        "name":"lbl_barcode",
                                        "category":"label",
                                        "text": "Barcode:",
                                        "style":self.primary_lbl + yellow_font
                                    },
                                    {
                                        "name":"detail_barcode",
                                        "category":"label",
                                        "text":str( res[0][cols.index('barcode')] ),
                                        "style":self.detail_lbl
                                    },
                                    {
                                        "name":"lbl_datetime",
                                        "category":"label",
                                        "text": "Waktu Masuk:",
                                        "style":self.primary_lbl + yellow_font
                                    },
                                    {
                                        "name":"detail_datetime",
                                        "category":"label",
                                        "text":str( res[0][cols.index('datetime')] ),
                                        "style":self.detail_lbl
                                    },
                                    {
                                        "name":"lbl_gate",
                                        "category":"label",
                                        "text": "Gate:",
                                        "style":self.primary_lbl + yellow_font
                                    },
                                    {
                                        "name":"detail_gate",
                                        "category":"label",
                                        "text":str( res[0][cols.index('gate')] ),
                                        "style":self.detail_lbl
                                    },
                                    {
                                        "name":"lbl_stat",
                                        "category":"label",
                                        "text": "Status Parkir:",
                                        "style":self.primary_lbl + yellow_font
                                    },
                                    {
                                        "name":"detail_stat",
                                        "category":"label",
                                        "text": str( res[0][cols.index('status_parkir')] ),
                                        "style":self.detail_lbl
                                    },
                                    {
                                        "name":"lbl_jns_kendaaraan",
                                        "category":"label",
                                        "text": "Jenis Kendaraan:",
                                        "style":self.primary_lbl + yellow_font
                                    },
                                    {
                                        "name":"detail_jns_kendaraan",
                                        "category":"label",
                                        "text":str( res[0][cols.index('jenis_kendaraan')] ),
                                        "style":self.detail_lbl
                                    },
                                    {
                                        "name":"lbl_photo",
                                        "category":"label",
                                        "text": "Photo:",
                                        "style":self.primary_lbl + yellow_font
                                    },
                                    {
                                        "name":"detail_photo",
                                        "category":"image",
                                        "img_path":img_masuk,
                                        "style":self.detail_lbl
                                    },
                                ]

                case default:
                    pass    

            self.win = QMainWindow()
            central_widget = QWidget()
            central_lay = QVBoxLayout()
            
            central_lay.setContentsMargins(25,25,25,25)
            central_widget.setStyleSheet("background:#222b45;")

            self.CreateComponentLayout(components, central_lay)
            central_lay.addStretch(1)
            
            central_widget.setLayout(central_lay)
            self.win.setCentralWidget(central_widget)

            self.win.setWindowTitle(f"{form_type} details")
            self.win.resize(form_size[0], form_size[1])
            
            self.win.show()


    def fillTable(self, table, cols, query, rows=0):
        
        if rows != 0:
            table.setRowCount(rows)
            
        # rows loop 
        r = 0
        for l in query:
            
            # set item on table column
            for i in range(cols):
                try:
                    val = str(l[i])
                except:
                    val = ""
                
                
                if val == 'None': val = ""
                elif val == 'True': val = "keluar"
                elif val == 'False': val = "masuk"

                # print(type(val))
                
                item = QTableWidgetItem( val )
                table.setItem(r, i, item)
            
            r = r + 1
    
    def fillTableKarcis(self, table, cols, res, index_tgl_masuk=None, index_tgl_keluar=None):
            
        # rows loop 
        r = 0
        for l in res:
            
            # set item on table column
            for i in range(cols):
                try:
                    val = str(l[i])
                except:
                    val = ""
                
                
                if val == 'None': val = ""
                elif val == 'True': val = "keluar"
                elif val == 'False': val = "masuk"

                if index_tgl_masuk!=None and i==index_tgl_masuk or index_tgl_keluar!=None and i==index_tgl_keluar:
                    x = val.split("-")
                    if len(x) == 3:
                        year, month, day = x
                        val = f"{day}/{month}/{year}" 
                
                item = QTableWidgetItem( val )
                table.setItem(r, i, item)
            
            r = r + 1


    def radioFilterMenit(self,tt):
        
        if tt:
            self.r_menit = True
            self.radio_btn_jam.setChecked(False)
   
    def radioFilterJam(self,tt):
        
        if tt:
            self.r_jam = True
            self.radio_btn_menit.setChecked(False)
    

    def refreshKarcis(self):

        # reset filter form to default settings
        self.input_cari.setText("")
        self.pilih_jns_kendaraan.setCurrentIndex( 2 )
        self.pilih_stat_kendaraan.setCurrentIndex( 2 )
        self.pilih_jns_transaksi.setCurrentIndex( 2 )
        self.pilih_shift.setCurrentIndex( 5 )
        self.pilih_tgl1.setDateTime( QDateTime.currentDateTime() )
        self.pilih_tgl2.setDateTime( QDateTime.currentDateTime() )
        self.input_menit1.setValue(0)
        self.input_menit2.setValue(0)
        self.input_jam1.setValue(0)
        self.input_jam2.setValue(0)
        
        # refill karcis table
        self.karcis_rows = self.exec_query("select count(*) as count from karcis", "select")
        self.row_limit = 18 if self.karcis_rows[0][0] >= 18 else self.karcis_rows[0][0]
        self.row_offset = 0
        self.query_search = f"SELECT id, barcode,  nopol, jenis_kendaraan, gate, cast(datetime as date), cast(date_keluar as date), lama_parkir, status_parkir, tarif, jns_transaksi, kd_shift FROM karcis order by id"
        query = self.exec_query(f"SELECT id, barcode,  nopol, jenis_kendaraan, gate, cast(datetime as date), cast(date_keluar as date), lama_parkir, status_parkir, tarif, jns_transaksi, kd_shift FROM karcis order by id limit {self.row_limit} OFFSET {self.row_offset}", "SELECT")
        rows_count = len(query)
        cols = 11

        self.laporan_table.setRowCount(rows_count)
        self.fillTableKarcis(self.laporan_table, cols, query, index_tgl_masuk=5, index_tgl_keluar=6)

        self.lbl_count.setText(f"1-{self.row_limit} from {self.karcis_rows[0][0]} results")

    def searchKarcis(self):

        tgl1 = self.pilih_tgl1.text()
        tgl2 = self.pilih_tgl2.text()
        tgl1 = tgl1.replace("/", "-" ) #for file name
        tgl2 = tgl2.replace("/", "-" )

        day, month, year = tgl1.split("-")
        parse_tgl1 = f"{year}-{month}-{day}"
        
        day, month, year = tgl2.split("-")
        parse_tgl2 = f"{year}-{month}-{day}"

        # create query based on filter
        query = ""

        cari_data = self.input_cari.text()
        jns_kendaraan = self.pilih_jns_kendaraan.currentText()
        stat_kendaraan = self.pilih_stat_kendaraan.currentText()
        jns_transaksi = self.pilih_jns_transaksi.currentText()
        kd_shift = self.pilih_shift.currentText()

        # cari data, tanggal, menit, jam, jenis pembayaran, shift,  
        # SELECT id, barcode,  nopol, jenis_kendaraan, gate, datetime, date_keluar, lama_parkir, status_parkir, tarif, jns_transaksi, kd_shift
         
        # select datetime from karcis where cast(datetime as date) between '2023-02-05' and '2023-02-06';
        # select id,lama_parkir from karcis where lama_parkir between CAST('3600 seconds' AS interval) and CAST('10800 seconds' AS interval);
        # select id,lama_parkir from karcis where lama_parkir=CAST('3600 seconds' AS interval);
        query = f"{query} "
        
        ######### stat kendaraan ===> menentukan column tgl mana yg akan di filter
        if stat_kendaraan == "Masuk":
            query = f"{query} cast( datetime as date ) between '{parse_tgl1}' and '{parse_tgl2}'"
        elif stat_kendaraan == "Keluar":
            query = f"{query} cast( date_keluar as date ) between '{parse_tgl1}' and '{parse_tgl2}'"
        elif stat_kendaraan == "Semua":
            query = f"{query} ( cast( datetime as date ) between '{parse_tgl1}' and '{parse_tgl2}' or cast( date_keluar as date ) between '{parse_tgl1}' and '{parse_tgl2}' )"
            
           
        ######## check menit/jam filter is active ?
        if self.r_menit:
            sv1 = self.input_menit1.text()
            sv2 = self.input_menit2.text()
            query = f"{query} and lama_parkir between CAST('{sv1}' AS interval) and CAST('{sv2}' AS interval)"
        elif self.r_jam:
            sv1 = self.input_jam1.text()
            sv2 = self.input_jam2.text()
            query = f"{query} and lama_parkir between CAST('{sv1}' AS interval) and CAST('{sv2}' AS interval)"
        
        

        ######### jns kendaraan
        if jns_kendaraan != "Semua":
            query = f"{query} and jenis_kendaraan='{ jns_kendaraan.lower() }'"

        
        ######### jenis transaksi
        if jns_transaksi != "Semua":
            query = f"{query} and jns_transaksi='{ jns_transaksi.lower() }'"

        
        ######### shift
        if kd_shift != "Semua":
            query = f"{query} and kd_shift='{kd_shift}'"
        

        ######### cari data
        if cari_data != "" and cari_data != None:
            query = f"{query} and barcode like '%{cari_data}%' or CAST( tarif as TEXT ) like '%{cari_data}%' or nopol like '%{cari_data}%'"


        # exec query
        self.query_search = f"select id, barcode, nopol, jenis_kendaraan, gate, cast(datetime as date), cast(date_keluar as date), lama_parkir, status_parkir, tarif, jns_transaksi, kd_shift from karcis where {query} order by id"
        # print("cek==>: ", query)

        # print("==> query: ",query)

        # extract result & fill laporan table
        self.karcis_rows = self.exec_query(f"select count(*) as count from karcis where {query}", "select") # query utk hitung jumlah semua data, berdasarkan filter2ny, tidak pakai limit karena mau tau jumlah semua data
        self.row_limit = 18 if self.karcis_rows[0][0] >= 18 else self.karcis_rows[0][0] # menentukan jumlah limit, berdasarakan total data yg ada
        self.row_offset = 0
        
        
        query_limit = f"{self.query_search} limit {self.row_limit} OFFSET {self.row_offset}" # baru masukkan limit kedalam querynya
        
        res = self.exec_query( query_limit, "SELECT") # result yg ada limitnya
        res2 = self.exec_query( self.query_search, "SELECT") # result yg tidak ada limitnya, utk diolah pada proses yg lain, seperti cetak laporan
        rows_count = len(res)
        cols = 11

        self.laporan_table.setRowCount( rows_count )
        self.laporan_table.setColumnCount( cols )
        self.fillTableKarcis(self.laporan_table, cols, res, index_tgl_masuk=5, index_tgl_keluar=6)

        self.lbl_count.setText(f"1-{self.row_limit} from {self.karcis_rows[0][0]} results")
        
        # enable print button
        print_btn_action = """QPushButton {
                                background:#ff3d71; 
                                padding:5px;
                                color:#fff;
                                font-size:13px; 
                                font-weight: 500;
                            }
                            QPushButton:hover {
                                background-color: #951C3C;
                            }"""
        
        self.row_print.setEnabled(True)
        self.row_print.setStyleSheet( print_btn_action )

        # update total income
        # print(f"select SUM(tarif) as tot_income from karcis where {query}")
        q_income = self.exec_query(f"select SUM(tarif) as tot_income from karcis where {query}", "SELECT")
        income_res = 0 if q_income[0][0] is None else q_income[0][0]
        # print(q_income[0][0], type(q_income[0][0]))

        if income_res > 0:
            self.total_income_lbl.setText("TOTAL INCOME: Rp " +  "{:,}".format( q_income[0][0] ).replace(",", ".") )
        else:
            self.total_income_lbl.setText("TOTAL INCOME: Rp 0" )


        return tgl1,tgl2,res2 

    def printLaporan(self):

        # Margin
        self.m= 10
        
        # Cell height
        self.ch = 6
        self.pdf = FPDF()
        
        self.pdf.set_font('Arial', '', 8)

        tgl1,tgl2,res = self.searchKarcis()

        # print("===>")
        # print(type(res))
        # print(res)
        
        ### jenis laporan
        if self.row_opsi_print.currentText() == "rekap/jam":
            
            # Page landscape: Width of A4 is 210mm x 297mm 
            self.ph = 210
            self.pw = 297 - 2*self.m
            self.pdf.add_page(orientation='L')

            self.agregatJam( tgl1,tgl2 )
        
        elif self.row_opsi_print.currentText() == "rekap/tgl":
            # Page landscape: Width of A4 is 210mm x 297mm 
            self.ph = 210
            self.pw = 297 - 2*self.m
            self.pdf.add_page(orientation='L')

            self.agregatTgl( tgl1,tgl2 )
        
        elif self.row_opsi_print.currentText() == "semua":

            # Page potrait: Width of A4 is 210mm x 297mm 
            self.ph = 297
            self.pw = 210 - 2*self.m
            self.pdf.add_page(orientation='P')

            self.semuaData( tgl1,tgl2,res )

        

    def agregatJam(self,tgl1,tgl2):
        self.ch = 5
        day, month, year = tgl1.split("-")
        d1 = datetime( int(year), int(month), int(day) )
        parse_tgl1 = f"{day}/{month}/{year}"
        
        day, month, year = tgl2.split("-")
        d2 = datetime( int(year), int(month), int(day) )
        parse_tgl2 = f"{day}/{month}/{year}"

        self.pdf.set_font('Arial', 'B', 10)
        self.pdf.cell(w=(self.pw/5)*5, h=self.ch, txt="REKAP PENDAPATAN PARKIR", border=0, ln=1, align='C')
        self.pdf.cell(w=(self.pw/5)*5, h=self.ch, txt=f"periode: {parse_tgl1} sampai dengan {parse_tgl2}", border=0, ln=1)
        
        ############################### header ###############################
        self.pdf.cell(w=(self.pw/5), h=self.ch*2, txt="Lama Parkir", border=1, align='C')
        self.pdf.cell(w=(self.pw/5), h=self.ch, txt="Motor", border=1)
        self.pdf.cell(w=(self.pw/5), h=self.ch, txt="Mobil", border=1)
        self.pdf.cell(w=(self.pw/5), h=self.ch, txt="Lainnya", border=1)
        self.pdf.cell(w=(self.pw/5), h=self.ch, txt="Grand Total", border=1)

        self.pdf.ln()

        self.pdf.cell((self.pw/5), self.ch,  border=0)
        
        # motor
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="jml", border=1)
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="total", border=1)

        # mobil
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="jml", border=1)
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="total", border=1)

        # lainnya
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="jml", border=1)
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="total", border=1)

        # grand total
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="jml", border=1)
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="total", border=1, ln=1)

        ############################ end header ###########################

        ############################ table content ###########################
        
        bottom_j_motor = 0
        bottom_j_mobil = 0
        bottom_j_gt = 0
        bottom_t_motor = 0
        bottom_t_mobil = 0
        bottom_t_gt = 0
        
        # toleransi dalam menit, jadi harus di konversi kedalam detik
        toleransi = self.exec_query(f"select toleransi from tarif where id=1","select")
        toleransi = int(toleransi[0][0]) * 60

        self.pdf.set_font('Arial', '', 10)
        for i in range(25):
            
            self.pdf.cell(w=(self.pw/5), h=self.ch, txt=f"{i} Jam", border=1)
            
            # konversi jam ke detik
            i_before = i * 3600
            i_after = (i+1) * 3600
            
            # motor
            if i==0:
                res = self.exec_query(f"""
                        select count(*) as jml, SUM(tarif) as total from karcis 
                        where CAST(date_keluar as date) 
                        between '{d1}' and '{d2}' 
                        and cast(EXTRACT(epoch FROM lama_parkir) as integer) >= {toleransi}
                        and cast(EXTRACT(epoch FROM lama_parkir) as integer) < {i_after}
                        and status_parkir=true
                        and lost_ticket=false
                        and (jenis_kendaraan='motor' or jenis_kendaraan='Motor') """, "select")

            else:
                res = self.exec_query(f"""
                        select count(*) as jml, SUM(tarif) as total from karcis 
                        where CAST(date_keluar as date) 
                        between '{d1}' and '{d2}' 
                        and cast(EXTRACT(epoch FROM lama_parkir) as integer) >= {i_before}
                        and cast(EXTRACT(epoch FROM lama_parkir) as integer) < {i_after}
                        and status_parkir=true
                        and lost_ticket=false
                        and (jenis_kendaraan='motor' or jenis_kendaraan='Motor') """, "select")
    
            j_motor = 0 if res[0][0]==0 or res[0][0] is None else res[0][0]
            t_motor = 0 if res[0][1]==0 or res[0][1] is None else res[0][1]
            self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( j_motor ).replace(",", "."), border=1)
            self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( t_motor ).replace(",", "."), border=1)
            bottom_j_motor += j_motor
            bottom_t_motor += t_motor

            # mobil
            if i==0:
                res = self.exec_query(f"""
                        select count(*) as jml, SUM(tarif) as total from karcis 
                        where CAST(date_keluar as date) 
                        between '{d1}' and '{d2}' 
                        and cast(EXTRACT(epoch FROM lama_parkir) as integer) >= {toleransi}
                        and cast(EXTRACT(epoch FROM lama_parkir) as integer) < {i_after}
                        and status_parkir=true
                        and lost_ticket=false
                        and (jenis_kendaraan='mobil' or jenis_kendaraan='Mobil') """, "select")

            else:
                res = self.exec_query(f"""
                        select count(*) as jml, SUM(tarif) as total from karcis 
                        where CAST(date_keluar as date) 
                        between '{d1}' and '{d2}' 
                        and cast(EXTRACT(epoch FROM lama_parkir) as integer) >= {i_before}
                        and cast(EXTRACT(epoch FROM lama_parkir) as integer) < {i_after}
                        and status_parkir=true
                        and lost_ticket=false
                        and (jenis_kendaraan='mobil' or jenis_kendaraan='Mobil') """, "select")
    
            j_mobil = 0 if res[0][0]==0 or res[0][0] is None else res[0][0]
            t_mobil = 0 if res[0][1]==0 or res[0][1] is None else res[0][1]
            self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( j_mobil ).replace(",", "."), border=1)
            self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( t_mobil ).replace(",", "."), border=1)
            bottom_j_mobil += j_mobil
            bottom_t_mobil += t_mobil

            # lainnya
            self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="...", border=1)
            self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="...", border=1)

            # grand total 
            gth_jum = int(j_motor) + int(j_mobil) 
            gth_tot = int(t_motor) + int(t_mobil) 
            bottom_j_gt += gth_jum
            bottom_t_gt += gth_tot
            self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( gth_jum ).replace(",", "."), border=1)
            self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( gth_tot ).replace(",", "."), border=1)

            self.pdf.ln()



        #### > 24 jam
        day1_in_seconds = 24 * 3600  
        self.pdf.cell(w=(self.pw/5), h=self.ch, txt="> 24 Jam", border=1,)
        
        # motor
        res = self.exec_query(f"""
                        select count(*) as jml, SUM(tarif) as total from karcis 
                        where CAST(date_keluar as date) 
                        between '{d1}' and '{d2}' 
                        and cast(EXTRACT(epoch FROM lama_parkir) as integer) > {day1_in_seconds}
                        and status_parkir=true
                        and lost_ticket=false
                        and (jenis_kendaraan='motor' or jenis_kendaraan='Motor') """, "select")
        
        j_motor = 0 if res[0][0]==0 or res[0][0] is None else res[0][0]
        t_motor = 0 if res[0][1]==0 or res[0][1] is None else res[0][1]
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( j_motor ).replace(",", "."), border=1)
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( t_motor ).replace(",", "."), border=1)
        bottom_j_motor += j_motor
        bottom_t_motor += t_motor
        
        
        # mobil
        res = self.exec_query(f"""
                        select count(*) as jml, SUM(tarif) as total from karcis 
                        where CAST(date_keluar as date) 
                        between '{d1}' and '{d2}' 
                        and cast(EXTRACT(epoch FROM lama_parkir) as integer) > {day1_in_seconds}
                        and status_parkir=true
                        and lost_ticket=false
                        and (jenis_kendaraan='mobil' or jenis_kendaraan='Mobil') """, "select")
        
        j_mobil = 0 if res[0][0]==0 or res[0][0] is None else res[0][0]
        t_mobil = 0 if res[0][1]==0 or res[0][1] is None else res[0][1]
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( j_mobil ).replace(",", "."), border=1)
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( t_mobil ).replace(",", "."), border=1)
        bottom_j_mobil += j_mobil
        bottom_t_mobil += t_mobil
        
        # lainnya
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="...", border=1)
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="...", border=1)
        
        # grand total
        gth_jum = int(j_motor) + int(j_mobil) 
        gth_tot = int(t_motor) + int(t_mobil) 
        bottom_j_gt += gth_jum
        bottom_t_gt += gth_tot
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( gth_jum ).replace(",", "."), border=1)
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( gth_tot ).replace(",", "."), border=1)
        
        self.pdf.ln()
        
        #### pass
        self.pdf.cell(w=(self.pw/5), h=self.ch, txt="Pass", border=1,)
        
        # motor
        res = self.exec_query(f"""
                        select count(*) as jml, SUM(tarif) as total from karcis 
                        where CAST(date_keluar as date) 
                        between '{d1}' and '{d2}' 
                        and cast(EXTRACT(epoch FROM lama_parkir) as integer) <= {toleransi}
                        and status_parkir=true
                        and lost_ticket=false
                        and (jenis_kendaraan='motor' or jenis_kendaraan='Motor') """, "select")
        
        j_motor = 0 if res[0][0]==0 or res[0][0] is None else res[0][0]
        t_motor = 0 if res[0][1]==0 or res[0][1] is None else res[0][1]
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( j_motor ).replace(",", "."), border=1)
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( t_motor ).replace(",", "."), border=1)
        bottom_j_motor += j_motor
        bottom_t_motor += t_motor
        
        
        # mobil
        res = self.exec_query(f"""
                        select count(*) as jml, SUM(tarif) as total from karcis 
                        where CAST(date_keluar as date) 
                        between '{d1}' and '{d2}' 
                        and cast(EXTRACT(epoch FROM lama_parkir) as integer) <= {toleransi}
                        and status_parkir=true
                        and lost_ticket=false
                        and (jenis_kendaraan='mobil' or jenis_kendaraan='Mobil') """, "select")
        
        j_mobil = 0 if res[0][0]==0 or res[0][0] is None else res[0][0]
        t_mobil = 0 if res[0][1]==0 or res[0][1] is None else res[0][1]
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( j_mobil ).replace(",", "."), border=1)
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( t_mobil ).replace(",", "."), border=1)
        bottom_j_mobil += j_mobil
        bottom_t_mobil += t_mobil
        
        # lainnya
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="...", border=1)
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="...", border=1)
        
        # grand total
        gth_jum = int(j_motor) + int(j_mobil) 
        gth_tot = int(t_motor) + int(t_mobil) 
        bottom_j_gt += gth_jum
        bottom_t_gt += gth_tot
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( gth_jum ).replace(",", "."), border=1)
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( gth_tot ).replace(",", "."), border=1)
        
        self.pdf.ln()

        ### lost ticket
        

        #### bottom row-cell
        self.pdf.set_font('Arial', 'B', 10)
        self.pdf.cell(w=(self.pw/5), h=self.ch, txt="TOTAL", border=1, align='C')
        
        # motor
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( bottom_j_motor ).replace(",", "."), border=1)
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( bottom_t_motor ).replace(",", "."), border=1)
        
        # mobil
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( bottom_j_mobil ).replace(",", "."), border=1)
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( bottom_t_mobil ).replace(",", "."), border=1)
        
        # lainnya
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="", border=1)
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="", border=1)
        
        # grand total
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( bottom_j_gt ).replace(",", "."), border=1)
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( bottom_t_gt ).replace(",", "."), border=1)
        
        self.pdf.ln()
        
        ################# end table content ######################

        lap_name = f"laporan_{tgl1}_{tgl2}.pdf"
        self.pdf.output(f'./{lap_name}', 'F')

        path = os.path.abspath(lap_name)

        webbrowser.open_new("file://"+path)

    def agregatTgl(self,tgl1,tgl2):
        
        day, month, year = tgl1.split("-")
        d1 = datetime( int(year), int(month), int(day) )
        parse_tgl1 = f"{day}/{month}/{year}"
        
        day, month, year = tgl2.split("-")
        d2 = datetime( int(year), int(month), int(day) )
        parse_tgl2 = f"{day}/{month}/{year}"

        self.pdf.set_font('Arial', 'B', 8)
        self.pdf.cell(w=(self.pw/5)*5, h=self.ch, txt="REKAP PENDAPATAN PARKIR", border=0, ln=1, align='C')
        self.pdf.cell(w=(self.pw/5)*5, h=self.ch, txt=f"periode: {parse_tgl1} sampai dengan {parse_tgl2}", border=0, ln=1)
        
        ############################### header ###############################
        self.pdf.cell(w=(self.pw/5), h=self.ch*2, txt="Tanggal", border=1, align='C')
        self.pdf.cell(w=(self.pw/5), h=self.ch, txt="Motor", border=1)
        self.pdf.cell(w=(self.pw/5), h=self.ch, txt="Mobil", border=1)
        self.pdf.cell(w=(self.pw/5), h=self.ch, txt="Lainnya", border=1)
        self.pdf.cell(w=(self.pw/5), h=self.ch, txt="Grand Total", border=1)

        self.pdf.ln()

        self.pdf.cell((self.pw/5), self.ch,  border=0)
        
        # motor
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="jml", border=1)
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="total", border=1)

        # mobil
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="jml", border=1)
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="total", border=1)

        # lainnya
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="jml", border=1)
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="total", border=1)

        # grand total
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="jml", border=1)
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="total", border=1, ln=1)

        ############################ end header ###########################

        ############################ table content ###########################
        

        ###### check apakah jumlah data pada list sama dengan selisih tgl1 dan tgl 2
        ###### jika sama, artinya range tgl tersebut ada datanya semua
        delta = d2-d1
        # start_date = datetime.strptime(start_date_str, "%Y-%m-%d")

        bottom_j_motor = 0
        bottom_j_mobil = 0
        bottom_j_gt = 0
        bottom_t_motor = 0
        bottom_t_mobil = 0
        bottom_t_gt = 0
        
        self.pdf.set_font('Arial', '', 8)
        for i in range(delta.days+1):
            current_date = d1 + timedelta(days=i) 
            tgl = current_date.strftime("%d/%m/%y")
            tgl2 = current_date.strftime("%Y-%m-%d")



            self.pdf.cell(w=(self.pw/5), h=self.ch, txt=tgl, border=1)

            # motor
            res = self.exec_query(f"select count(*) as jml, SUM(tarif) as total from karcis where cast(date_keluar as date)='{tgl2}' and (jenis_kendaraan='motor' or jenis_kendaraan='Motor') and lost_ticket=false", "SELECT")
            j_motor = 0 if res[0][0]==0 or res[0][0] is None else res[0][0]
            t_motor = 0 if res[0][1]==0 or res[0][1] is None else res[0][1]
            self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( j_motor ).replace(",", "."), border=1)
            self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( t_motor ).replace(",", "."), border=1)
            bottom_j_motor += j_motor
            bottom_t_motor += t_motor
            
            # mobil
            res = self.exec_query(f"select count(*) as jml, SUM(tarif) as total from karcis where cast(date_keluar as date)='{tgl2}' and (jenis_kendaraan='mobil' or jenis_kendaraan='Mobil') and lost_ticket=false", "SELECT")
            j_mobil = 0 if res[0][0]==0 or res[0][0] is None else res[0][0]
            t_mobil = 0 if res[0][1]==0 or res[0][1] is None else res[0][1]
            bottom_j_mobil += j_mobil
            bottom_t_mobil += t_mobil
            self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( j_mobil ).replace(",", "."), border=1)
            self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( t_mobil ).replace(",", "."), border=1)
            
            # lainnya
            self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="...", border=1)
            self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="...", border=1)

            # grand total
            gth_jum = int(j_motor) + int(j_mobil) 
            gth_tot = int(t_motor) + int(t_mobil) 
            bottom_j_gt += gth_jum
            bottom_t_gt += gth_tot
            self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( gth_jum ).replace(",", "."), border=1)
            self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( gth_tot ).replace(",", "."), border=1)

            self.pdf.ln()
        

        # bottom row-cell
        self.pdf.set_font('Arial', 'B', 8)
        self.pdf.cell(w=(self.pw/5), h=self.ch, txt="TOTAL", border=1, align='C')
        
        # motor
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( bottom_j_motor ).replace(",", "."), border=1)
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( bottom_t_motor ).replace(",", "."), border=1)
        
        # mobil
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( bottom_j_mobil ).replace(",", "."), border=1)
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( bottom_t_mobil ).replace(",", "."), border=1)
        
        # lainnya
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="", border=1)
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="", border=1)
        
        # grand total
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( bottom_j_gt ).replace(",", "."), border=1)
        self.pdf.cell(w=(self.pw/5)/2, h=self.ch, txt="{:,}".format( bottom_t_gt ).replace(",", "."), border=1)
        
        self.pdf.ln()

        ################# end table content ######################

        lap_name = f"laporan_perjam_{tgl1}_{tgl2}.pdf"
        self.pdf.output(f'./{lap_name}', 'F')

        path = os.path.abspath(lap_name)

        webbrowser.open_new("file://"+path)

    def semuaData(self,tgl1,tgl2,res):
        
        day, month, year = tgl1.split("-")
        parse_tgl1 = f"{day}/{month}/{year}"
        
        day, month, year = tgl2.split("-")
        parse_tgl2 = f"{day}/{month}/{year}"

        self.pdf.set_font('Arial', 'B', 8)
        self.pdf.cell(w=(self.pw/7)*7, h=self.ch, txt="REKAP PARKIR HARIAN", border=0, ln=1, align='C')
        self.pdf.cell(w=(self.pw/7)*7, h=self.ch, txt=f"periode: {parse_tgl1} sampai dengan {parse_tgl2}", border=0, align='C', ln=1)
        
        ############################### header ###############################
        self.pdf.cell(w=(self.pw/7), h=self.ch, txt="Nopol", border=1, align='C')
        self.pdf.cell(w=(self.pw/7), h=self.ch, txt="J.Kend", border=1, align='C')
        self.pdf.cell(w=(self.pw/7), h=self.ch, txt="W.Masuk", border=1, align='C')
        self.pdf.cell(w=(self.pw/7), h=self.ch, txt="W.Keluar", border=1, align='C')
        self.pdf.cell(w=(self.pw/7), h=self.ch, txt="Lama", border=1, align='C')
        self.pdf.cell(w=(self.pw/7), h=self.ch, txt="St.Trans", border=1, align='C')
        self.pdf.cell(w=(self.pw/7), h=self.ch, txt="Tarif", border=1, align='C')
        self.pdf.ln()
        
        tot_ch = 0

        for i in range(len(res)):
            date_masuk = "" if res[i][5] is None else str(res[i][5].strftime("%d/%m/%y %H:%M:%S"))
            date_keluar = "" if res[i][6] is None else str(res[i][5].strftime("%d/%m/%y %H:%M:%S"))
            tarif = "0" if res[i][9] is None else str(res[i][9])
            nopol = "" if res[i][2] is None else str(res[i][2])
            tot_ch = tot_ch + self.ch

            self.pdf.set_font('Arial', '', 8)
            self.pdf.cell(w=(self.pw/7), h=self.ch, txt=nopol, border=1)
            self.pdf.cell(w=(self.pw/7), h=self.ch, txt=str(res[i][3]), border=1)
            self.pdf.cell(w=(self.pw/7), h=self.ch, txt=date_masuk, border=1)
            self.pdf.cell(w=(self.pw/7), h=self.ch, txt=date_keluar, border=1)
            self.pdf.cell(w=(self.pw/7), h=self.ch, txt=str(res[i][7]), border=1)
            self.pdf.cell(w=(self.pw/7), h=self.ch, txt=str(res[i][10]), border=1)
            self.pdf.cell(w=(self.pw/7), h=self.ch, txt=tarif, border=1, ln=1)

            if tot_ch == 39*self.ch:
                tot_ch = 0
                self.pdf.cell(0, 10, 'Page %s' % self.pdf.page_no(), 0, 0, 'C')
                self.pdf.ln()

                self.pdf.set_font('Arial', 'B', 8)
                self.pdf.cell(w=(self.pw/7)*7, h=self.ch, txt="REKAP PARKIR HARIAN", border=0, ln=1, align='C')
                self.pdf.cell(w=(self.pw/7)*7, h=self.ch, txt=f"periode: {parse_tgl1} sampai dengan {parse_tgl2}", border=0, align='C', ln=1)
                
                ############################### header ###############################
                self.pdf.cell(w=(self.pw/7), h=self.ch, txt="Nopol", border=1, align='C')
                self.pdf.cell(w=(self.pw/7), h=self.ch, txt="J.Kend", border=1, align='C')
                self.pdf.cell(w=(self.pw/7), h=self.ch, txt="W.Masuk", border=1, align='C')
                self.pdf.cell(w=(self.pw/7), h=self.ch, txt="W.Keluar", border=1, align='C')
                self.pdf.cell(w=(self.pw/7), h=self.ch, txt="Lama", border=1, align='C')
                self.pdf.cell(w=(self.pw/7), h=self.ch, txt="St.Trans", border=1, align='C')
                self.pdf.cell(w=(self.pw/7), h=self.ch, txt="Tarif", border=1, align='C')
                self.pdf.ln()

        lap_name = f"laporan_harian_{tgl1}_{tgl2}.pdf"
        self.pdf.output(f'./{lap_name}', 'F')

        path = os.path.abspath(lap_name)

        webbrowser.open_new("file://"+path)

    def dialogBox(self, title="", msg=""):
        
        # init dialog box
        dlg = QMessageBox(self.window)
        dlg.setWindowTitle( title )
        dlg.setText( msg )
        dlg.setIcon(QMessageBox.Information)
        dlg.exec()  
