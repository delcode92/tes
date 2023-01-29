import sys, psycopg2, os, math, threading

from client.client_service import Client
from PyQt5.QtWidgets import (QMdiArea, QMessageBox, QMdiSubWindow, QWidget ,QHeaderView, QLabel, QPushButton, QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import Qt, QRect, QEasingCurve
from PyQt5.QtGui import QColor, QIcon
from configparser import ConfigParser
# from framework import View

class Controller():
    def __init__(self) -> None:
        # self.Util.__init__(self)
        
        # active db cursor 
        self.connect_to_postgresql()
        
        # ========== steps ========
        print("\nController constructor: ")
        print("connect to DB .....")
        print("active DB cursor ..... \n")

    def Action(self):
        pass

    def connect_to_server(self, host, port):
        s = Client(host, port)

    def connect_to_postgresql(self):
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
            print("\nsuccess execute query")

            if type.lower() != "select":    
                return True

        except Exception:
            print("\nexecute query fail")



        if type.lower() =="select":
            data = self.db_cursor.fetchall()
            return data

    # def check_login(self, uname, password):
    #     if uname=="admin" and password=="admin":
    #         self.AdminDashboard()
    #     elif uname=="kasir" and password=="kasir":
    #         self.KasirDashboard()


    def login_ctrl(self, arg):
        uname = arg[1].components["input_uname"].text()
        passwd = arg[1].components["input_pass"].text()

        if uname=="admin" and passwd=="admin":
            self.closeWindow(arg[0])
            self.AdminDashboard()
        elif uname=="kasir" and passwd=="kasir":
            self.closeWindow(arg[0])
            self.KasirDashboard()
        
        # self.check_login(uname, passwd)
        
        
        #  jika berhasil login maka try connect to server
        # Client("localhost", 65430)

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
            
            # clear all input
            self.components["add_rfid"].setText("")
            self.components["add_rfid_owner"].setText("")

            # show success message
            self.components["lbl_success"].setHidden(False)

            timer = threading.Timer(1.0, self.hideSuccess)
            timer.start()


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
                 # clear all input
                self.components["add_uname"].setText("")
                self.components["add_pass"].setText("")
                self.components["retype_pass"].setText("")
                
                # show success message
                self.components["lbl_success"].setHidden(False)

                timer = threading.Timer(1.0, self.hideSuccess)
                timer.start()
    
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
            # clear all input
            self.components["add_nik"].setText("")    
            self.components["add_nama"].setText("")    
            self.components["add_hp"].setText("")    
            self.components["add_alamat"].setText("")    
            self.components["add_jam_masuk"].setText("")    
            self.components["add_jam_keluar"].setText("")    
            self.components["add_nmr_pos"].setText("")
            
            # show success message
            self.components["lbl_success"].setHidden(False)

            timer = threading.Timer(1.0, self.hideSuccess)
            timer.start()

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

    def save_edit_rfid(self):
        # get data from edit form
        id = self.components["hidden_id"].text()
        rfid = self.components["add_rfid"].text()
        owner = self.components["add_rfid_owner"].text()

        # run update query
        self.exec_query(f"update rfid set rfid='{rfid}', nama='{owner}' where id="+id)
        
        # call table table list again
        self.windowBarAction("kelola rfid")
    
    def save_edit_user(self):
        # get data from edit form
        id = self.components["hidden_id"].text()
        uname = self.components["add_uname"].text()
        level = self.components["input_user_level"].currentText()
        passwd = self.components["add_pass"].text()
        retype_passwd = self.components["retype_pass"].text()

        if passwd == retype_passwd:

            # run update query
            self.exec_query(f"update users set username='{uname}', user_level='{level}', password='{passwd}' where id="+id)
            
            # call table table list again
            self.windowBarAction("kelola user")
    
    def save_edit_kasir(self):
        # get data from edit form
        id = self.components["hidden_id"].text()
        nik = self.components["add_nik"].text()
        nama = self.components["add_nama"].text()
        hp = self.components["add_hp"].text()
        alamat = self.components["add_alamat"].text()
        jm_masuk = self.components["add_jam_masuk"].text()
        jm_keluar = self.components["add_jam_keluar"].text()
        no_pos = self.components["add_nmr_pos"].text()

        # run update query
        self.exec_query(f"update kasir set nik='{nik}', nama='{nama}', hp='{hp}', alamat='{alamat}', jm_masuk='{jm_masuk}', jm_keluar='{jm_keluar}', no_pos='{no_pos}'  where id="+id)
        
        # call table table list again
        self.windowBarAction("kelola kasir")
    
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
    
    def save_edit_tarif(self):
        # get data from edit form
        id = self.components["hidden_id"].text()

        pos = self.components["add_tarif_pos"].text()
        tarif_perjam = self.components["add_tarif_per_1jam"].text()
        tarif_per24jam = self.components["add_tarif_per_24jam"].text()
        jns_kendaraan = self.components["add_tarif_jns_kendaraan"].currentText()
        
        # run update query
        self.exec_query(f"update tarif set no_pos='{pos}', tarif_perjam='{tarif_perjam}', tarif_per24jam='{tarif_per24jam}', jns_kendaraan='{jns_kendaraan}' where id="+id)
        
        # call table table list again
        self.windowBarAction("kelola tarif")

    def windowBarAction(self, q):
        
        try:
            bar_action = q.text().lower()
        except Exception:
            bar_action = q

        margin_top = "margin-top:30px;"
        cell_bg_color = QColor(243,243,243)

        self.stacked_animation.setDuration(400)
        self.stacked_animation.setStartValue(self.stacked_widget.geometry())
        self.stacked_animation.setEndValue(QRect(self.stacked_widget.x(), self.stacked_widget.y(), self.stacked_widget.width(), self.stacked_widget.height()))
        self.stacked_animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.stacked_animation.start()

        match bar_action:
            case "dashboard":
                # self.closeWindow(self.window)
                # self.AdminDashboard()
                
                ########### solution replace widget ########
                # x = QLabel("coba test 123")
                # x.setStyleSheet("color: red; font-size: 30px; background: grey;")

                # widget_before = self.right_content_lay.itemAt(0).widget()
                # self.right_content_lay.removeWidget(widget_before)
                # self.right_content_lay.addWidget(x)
                ##################################

                # solution stacked widget
                # self.stacked_widget.setCurrentIndex(0)
                self.stacked_animation.finished.connect(lambda: self.stacked_widget.setCurrentIndex(0))

            case "kelola rfid":
                self.stacked_animation.finished.connect(lambda: self.stacked_widget.setCurrentIndex(1))
                # self.stacked_widget.setCurrentIndex(1)
                # sub_window_setter = { "title": "Kelola RFID", "style":self.bg_white, "size":(800, 600) }
                # cols = 5

                # # create table
                # table = QTableWidget()
                # table.resizeRowsToContents()
                # table.setColumnCount(5)
                # table.setHorizontalHeaderLabels(["id", "RFID", "Nama", "Edit", "Del"])
                # table.setStyleSheet(self.table_style)
                # table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
                # table.setColumnHidden(0, True) #hide id column
                # # table.resizeRowsToContents()

                # header = table.horizontalHeader()

                # # set header stretch
                # for i in range(cols-3):
                #     header.setSectionResizeMode(i+1, QHeaderView.Stretch)
                
                # # run query & set column value
                # query = self.exec_query("SELECT id, rfid, nama FROM rfid order by nama", "SELECT")

                # for l in query:
                #     rows = table.rowCount()
                #     rows_count = rows + 1
                #     table.setRowCount(rows_count)
                    
                #     # set item on table column
                #     for i in range(cols-2):
                        
                #         item = QTableWidgetItem( str(l[i]) )
                #         item.setFlags(Qt.ItemIsEnabled)
                #         table.setItem(rows, i, item)
                    
                #     # create edit button
                #     btn = QPushButton(table)
                #     edit_ico = self.getPath("edit.png")
                #     btn.setIcon(QIcon(edit_ico))
                #     btn.setStyleSheet( self.edit_btn_action )
                #     table.setCellWidget(rows, 3, btn)
                #     btn.clicked.connect(lambda *args, row=rows: self.editData(row, table, "rfid"))
                    
                #     # create delete button
                #     btn_del = QPushButton(table)
                #     del_ico = self.getPath("trash.png")
                #     btn_del.setIcon(QIcon(del_ico))
                #     btn_del.setStyleSheet(self.del_btn_action)
                #     table.setCellWidget(rows, 4, btn_del)
                #     btn_del.clicked.connect(lambda *args, row=rows: self.deleteData(row, table, "rfid"))

                
                # rows_count = math.floor(rows_count/2)
               
                # for r in range(rows_count):
                #     n = 2*r+1
                
                #     table.item(n, 1).setBackground(cell_bg_color)
                #     table.item(n, 2).setBackground(cell_bg_color)
                
                # table.setShowGrid(False)
                # self.SubWinVerticalTable(sub_window_setter, [table])
 
            case "tambah rfid":
                sub_window_setter = { "title": "Tambah RFID", "style":self.bg_white, "size":(600, 400) }

                # components
                components_setter = [
                                    {
                                        "name":"lbl_success",
                                        "category":"label",
                                        "text": "Data Saved",
                                        "style":self.success_lbl
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
                                                "method_name": self.add_rfid
                                        },
                                        "style": self.primary_button
                                    }
                                ]

                self.SubWinVerticalForm(sub_window_setter, components_setter)
                self.components["lbl_success"].setAlignment(Qt.AlignCenter)
                self.components["lbl_success"].setHidden(True)
            
            
            case "kelola user":
                sub_window_setter = { "title": "Kelola User", "style":self.bg_white, "size":(800, 600) }
                cols = 5

                # create table
                table = QTableWidget()
                table.resizeRowsToContents()
                table.setColumnCount(5)
                table.setHorizontalHeaderLabels(["id", "Username", "level", "Action", " "])
                table.setStyleSheet(self.table_style)
                table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
                table.setColumnHidden(0, True) #hide id column
                # table.resizeRowsToContents()

                header = table.horizontalHeader()

                # set header stretch
                for i in range(cols-3):
                    header.setSectionResizeMode(i+1, QHeaderView.Stretch)
                
                # run query & set column value
                query = self.exec_query("SELECT id, username, user_level FROM users", "SELECT")

                for l in query:
                    rows = table.rowCount()
                    rows_count = rows + 1
                    table.setRowCount(rows_count)
                    
                    # set item on table column
                    for i in range(cols-2):
                        
                        item = QTableWidgetItem( str(l[i]) )
                        item.setFlags(Qt.ItemIsEnabled)
                        table.setItem(rows, i, item)
                    
                    # create edit button
                    btn = QPushButton(table)
                    edit_ico = self.getPath("edit.png")
                    btn.setIcon(QIcon(edit_ico))
                    btn.setStyleSheet( self.edit_btn_action )
                    # btn.clicked.connect(lambda: self.editData(table, "users"))
                    table.setCellWidget(rows, 3, btn)
                    btn.clicked.connect(lambda *args, row=rows: self.editData(row, table, "users"))

                    # create delete button
                    btn_del = QPushButton(table)
                    del_ico = self.getPath("trash.png")
                    btn_del.setIcon(QIcon(del_ico))
                    btn_del.setStyleSheet(self.del_btn_action)
                    # btn_del.clicked.connect(lambda: self.deleteData(table, "users"))
                    table.setCellWidget(rows, 4, btn_del)
                    btn.clicked.connect(lambda *args, row=rows: self.deleteData(row, table, "users"))


                rows_count = math.floor(rows_count/2)
               
                for r in range(rows_count):
                    n = 2*r+1

                    table.item(n, 1).setBackground(cell_bg_color)
                    table.item(n, 2).setBackground(cell_bg_color)
                
                table.setShowGrid(False)
                self.SubWinVerticalTable(sub_window_setter, [table])

            case "tambah user":
                sub_window_setter = { "title": "Tambah User", "style":self.bg_white, "size":(600, 600) }

                # components
                components_setter = [
                                    {
                                        "name":"lbl_success",
                                        "category":"label",
                                        "text": "Data Saved",
                                        "style":self.success_lbl
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
                                                "method_name": self.add_user
                                        },
                                        "style": self.primary_button
                                    }
                                ]

                self.SubWinVerticalForm(sub_window_setter, components_setter)
                self.components["lbl_success"].setAlignment(Qt.AlignCenter)
                self.components["lbl_success"].setHidden(True)

            case "kelola kasir":
                sub_window_setter = { "title": "Kelola Kasir", "style":self.bg_white, "size":(1200, 600)}
                cols = 10
                
                # create table
                table = QTableWidget()
                table.resizeRowsToContents()
                table.setColumnCount(10)
                table.setHorizontalHeaderLabels(["id", "NIK", "Nama", "HP", "Alamat", "Jam Masuk", "Jam Keluar", "No Pos", "Action", " "])
                table.setStyleSheet(self.table_style)
                table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
                table.setColumnHidden(0, True) #hide id column
                
                header = table.horizontalHeader()

                # set header stretch
                for i in range(cols-3):
                    header.setSectionResizeMode(i+1, QHeaderView.Stretch)
                
                # run query & set column value
                query = self.exec_query("SELECT id, nik, nama, hp, alamat, jm_masuk, jm_keluar, no_pos FROM kasir", "SELECT")

                for l in query:
                    rows = table.rowCount()
                    rows_count = rows + 1
                    table.setRowCount(rows_count)
                    
                    # set item on table column
                    for i in range(cols-2):
                        
                        item = QTableWidgetItem( str(l[i]) )
                        item.setFlags(Qt.ItemIsEnabled)
                        table.setItem(rows, i, item)
                    
                    # create edit button
                    btn = QPushButton(table)
                    edit_ico = self.getPath("edit.png")
                    btn.setIcon(QIcon(edit_ico))
                    btn.setStyleSheet( self.edit_btn_action )
                    # btn.clicked.connect(lambda: self.editData(table, "kasir"))
                    table.setCellWidget(rows, 8, btn)
                    btn.clicked.connect(lambda *args, row=rows: self.editData(row, table, "kasir"))
                    
                    # create delete button
                    btn_del = QPushButton(table)
                    del_ico = self.getPath("trash.png")
                    btn_del.setIcon(QIcon(del_ico))
                    btn_del.setStyleSheet(self.del_btn_action)
                    # btn_del.clicked.connect(lambda: self.deleteData(table, "kasir"))
                    table.setCellWidget(rows, 9, btn_del)
                    btn.clicked.connect(lambda *args, row=rows: self.deleteData(row, table, "kasir"))


                rows_count = math.floor(rows_count/2)
               
                for r in range(rows_count):
                    n = 2*r+1

                    table.item(n, 1).setBackground(cell_bg_color)
                    table.item(n, 2).setBackground(cell_bg_color)
                    table.item(n, 3).setBackground(cell_bg_color)
                    table.item(n, 4).setBackground(cell_bg_color)
                    table.item(n, 5).setBackground(cell_bg_color)
                    table.item(n, 6).setBackground(cell_bg_color)
                    table.item(n, 7).setBackground(cell_bg_color)
                
                table.setShowGrid(False)
                self.SubWinVerticalTable(sub_window_setter, [table])

            case "tambah kasir":
                sub_window_setter = { "title": "Tambah Kasir", "style":self.bg_white, "size":(800, 600) }

                # components
                components_setter = [
                                    {
                                        "name":"lbl_success",
                                        "category":"label",
                                        "text": "Data Saved",
                                        "style":self.success_lbl
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
                                                "method_name": self.add_kasir
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
                self.components["lbl_success"].setAlignment(Qt.AlignCenter)
                self.components["lbl_success"].setHidden(True)

            case "kelola gate":
                sub_window_setter = { "title": "Kelola Gate", "style":self.bg_white, "size":(1200, 600) }
                cols = 7
                
                # create table
                table = QTableWidget()
                table.resizeRowsToContents()
                table.setColumnCount(cols)
                table.setHorizontalHeaderLabels(["id", "Nomor Pos/Gate", "Tipe Pos", "Jenis Kendaraan", "IP Cam", "Edit", "Del"])
                table.setStyleSheet(self.table_style)
                table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
                table.setColumnHidden(0, True) #hide id column
                
                header = table.horizontalHeader()

                # set header stretch
                for i in range(cols-3):
                    header.setSectionResizeMode(i+1, QHeaderView.Stretch)
                    
                # run query & set column value
                query = self.exec_query("SELECT id, no_pos, tipe_pos, jns_kendaraan, ip_cam FROM gate", "SELECT")

                for l in query:
                    rows = table.rowCount()
                    rows_count = rows + 1
                    table.setRowCount(rows_count)
                    
                    # set item on table column
                    for i in range(cols-2):
                        
                        item = QTableWidgetItem( str(l[i]) )
                        item.setFlags(Qt.ItemIsEnabled)
                        table.setItem(rows, i, item)
                    
                    # create edit button
                    btn = QPushButton(table)
                    edit_ico = self.getPath("edit.png")
                    btn.setIcon(QIcon(edit_ico))
                    btn.setStyleSheet( self.edit_btn_action )
                    # btn.clicked.connect(lambda: self.editData(table, "gate"))
                    table.setCellWidget(rows, 5, btn)
                    btn.clicked.connect(lambda *args, row=rows: self.editData(row, table, "gate"))
                    
                    # create delete button
                    btn_del = QPushButton(table)
                    del_ico = self.getPath("trash.png")
                    btn_del.setIcon(QIcon(del_ico))
                    btn_del.setStyleSheet(self.del_btn_action)
                    # btn_del.clicked.connect(lambda: self.deleteData(table, "gate"))
                    table.setCellWidget(rows, 6, btn_del)
                    btn.clicked.connect(lambda *args, row=rows: self.deleteData(row, table, "gate"))


                rows_count = math.floor(rows_count/2)
               
                for r in range(rows_count):
                    n = 2*r+1

                    table.item(n, 1).setBackground(cell_bg_color)
                    table.item(n, 2).setBackground(cell_bg_color)
                    table.item(n, 3).setBackground(cell_bg_color)
                    table.item(n, 4).setBackground(cell_bg_color)
                
                table.setShowGrid(False)
                self.SubWinVerticalTable(sub_window_setter, [table])

            case "tambah gate":
                sub_window_setter = { "title": "Tambah Pos/Gate", "style":self.bg_white, "size":(600, 600) }

                # components
                components_setter = [{
                                        "name":"lbl_success",
                                        "category":"label",
                                        "text": "Data Saved",
                                        "style":self.success_lbl
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
                                                "method_name": self.add_gate
                                        },
                                        "style": self.primary_button
                                    }
                                ]

                self.SubWinVerticalForm(sub_window_setter, components_setter)
                
                self.components["lbl_success"].setAlignment(Qt.AlignCenter)
                self.components["lbl_success"].setHidden(True)

            case "setting karcis":
                sub_window_setter = { "title": "Setting Karcis", "style":self.bg_white, "size":(600, 600) }

                # components
                components_setter = [{
                                        "name":"lbl_success",
                                        "category":"label",
                                        "text": "Data Saved",
                                        "style":self.success_lbl
                                    },
                                    {
                                        "name":"lbl_nm_tempat",
                                        "category":"label",
                                        "text": "Nama Tempat",
                                        "style":self.primary_lbl + margin_top
                                    },
                                    {
                                        "name":"add_tempat",
                                        "category":"lineEdit",
                                        "style":self.primary_input
                                    },
                                    {
                                        "name":"lbl_nm_perusahaan",
                                        "category":"label",
                                        "text": "Nama Perusahaan",
                                        "style":self.primary_lbl + margin_top
                                    },
                                    {
                                        "name":"add_perusahaan",
                                        "category":"lineEdit",
                                        "style":self.primary_input
                                    },
                                    {
                                        "name":"lbl_pintu_masuk",
                                        "category":"label",
                                        "text": "Pintu Masuk",
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
                                                "method_name": self.add_tarif
                                        },
                                        "style": self.primary_button
                                    }
                                ]

                self.SubWinVerticalForm(sub_window_setter, components_setter)

            case "kelola tarif":
                sub_window_setter = { "title": "Kelola Tarif", "style":self.bg_white, "size":(900, 600) }

                cols = 7
                
                # create table
                table = QTableWidget()
                table.resizeRowsToContents()
                table.setColumnCount(cols)
                table.setHorizontalHeaderLabels(["id", "Nomor Pos/Gate", "Tarif/jam", "Tarif/24jam", "Jenis Kendaraan", "Edit", "Del"])
                table.setStyleSheet(self.table_style)
                table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
                table.setColumnHidden(0, True) #hide id column
                
                header = table.horizontalHeader()

                # set header stretch
                for i in range(cols-3):
                    header.setSectionResizeMode(i+1, QHeaderView.Stretch)
                    
                # run query & set column value
                query = self.exec_query("SELECT id, no_pos, tarif_perjam, tarif_per24jam, jns_kendaraan FROM tarif", "SELECT")

                for l in query:
                    rows = table.rowCount()
                    rows_count = rows + 1
                    table.setRowCount(rows_count)
                    
                    # set item on table column
                    for i in range(cols-2):
                        
                        item = QTableWidgetItem( str(l[i]) )
                        item.setFlags(Qt.ItemIsEnabled)
                        table.setItem(rows, i, item)
                    
                    # create edit button
                    btn = QPushButton(table)
                    edit_ico = self.getPath("edit.png")
                    btn.setIcon(QIcon(edit_ico))
                    btn.setStyleSheet( self.edit_btn_action )
                    # btn.clicked.connect(lambda: self.editData(table, "tarif"))
                    table.setCellWidget(rows, 5, btn)
                    btn.clicked.connect(lambda *args, row=rows: self.editData(row, table, "tarif"))
                    
                    # create delete button
                    btn_del = QPushButton(table)
                    del_ico = self.getPath("trash.png")
                    btn_del.setIcon(QIcon(del_ico))
                    btn_del.setStyleSheet(self.del_btn_action)
                    # btn_del.clicked.connect(lambda: self.deleteData(table, "tarif"))
                    table.setCellWidget(rows, 6, btn_del)
                    btn.clicked.connect(lambda *args, row=rows: self.deleteData(row, table, "tarif"))


                rows_count = math.floor(rows_count/2)
               
                for r in range(rows_count):
                    n = 2*r+1

                    table.item(n, 1).setBackground(cell_bg_color)
                    table.item(n, 2).setBackground(cell_bg_color)
                    table.item(n, 3).setBackground(cell_bg_color)
                    table.item(n, 4).setBackground(cell_bg_color)
                
                table.setShowGrid(False)
                self.SubWinVerticalTable(sub_window_setter, [table])
            
            case "aturan tarif":
                sub_window_setter = { "title": "Aturan Tarif Parkir", "style":self.bg_white, "size":(600, 600) }

                # components
                components_setter = [{
                                        "name":"lbl_success",
                                        "category":"label",
                                        "text": "Data Saved",
                                        "style":self.success_lbl
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
                                                "method_name": self.add_tarif
                                        },
                                        "style": self.primary_button
                                    }
                                ]

                self.SubWinVerticalForm(sub_window_setter, components_setter)

                self.components["lbl_success"].setAlignment(Qt.AlignCenter)
                self.components["lbl_success"].setHidden(True)
            
            case "kelola voucher":
                ...
            
            case "aturan voucher":
                ...
            
            case "kelola laporan":
                sub_window_setter = { "title": "Kelola Laporan" }
            
            case "logout":
                sys.exit()

            case default:
                pass    

        
        # if(bar_action != "dashboard"):

        #     # create subwindows
        #     sub = self.CreateWindow(sub_window_setter, self.window, "mdi")
            
        #     # create layout for sub windows
        #     sub_lay = self.CreateLayout(("VBoxLayout", True), sub)
        #     sub_lay.setContentsMargins(20,0,20,0)
        #     # sub_lay.setSpacing(0)
            
        #     sub_lay.addStretch(1)
        #     self.CreateComponentLayout(components_setter, sub_lay)
        #     sub_lay.addStretch(1)

        #     # show subwindows
        #     sub.show()
    
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

    def deleteData(self, row, table, target):
        # r = table.currentRow()
        id = table.item(row, 0).text()

        # modal
        dlg = QMessageBox(self.window)
        
        dlg.setWindowTitle("Alert")
        dlg.setText("Hapus Data ?")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setIcon(QMessageBox.Question)
        button = dlg.exec()

        if button == QMessageBox.Yes:
            print(f"delete from {target} where id="+id)
            res = self.exec_query(f"delete from {target} where id="+id)

            if res:
                match target:
                    case "rfid":
                        self.windowBarAction("kelola rfid")
                    case "users":
                        self.windowBarAction("kelola user")
                    case "kasir":
                        self.windowBarAction("kelola kasir")
                    case "gate":
                        self.windowBarAction("kelola gate")
                    case "tarif":
                        self.windowBarAction("kelola tarif")
                    case default:
                        pass     
                
    