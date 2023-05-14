import sys,cv2,os, json, logging
from framework import *
# from kasir_ipcam import *
from _thread import start_new_thread
from configparser import ConfigParser
from PyQt5.QtWidgets import QDialog

class ClickableLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
    clicked = pyqtSignal()

class Main(Util, View):
    def __init__(self) -> None:
        # 1. initialize important property & method from all parents
        # exampel : in Components Class --> self.components = {}
        super().__init__()

        # initialize font
        self.helvetica_12 = ("Helvetica", 12, 40)
        self.helvetica_13 = ("Helvetica", 13, 40)

        # create one main window object for all
        self.window = QMainWindow()
        self.mdi = None
        self.app_stat = False
        self.hidden_id = -1 # hidden id

        # steps
        
        # create thread for connect to server
        start_new_thread(self.connect_to_server, ( sys.argv[1], sys.argv[2] ))
        

    def setMenuClicked(self, button=None, label=None, page=""):
        button.clicked.connect(lambda: self.windowBarAction(page))
        label.clicked.connect(lambda: self.windowBarAction(page))
    
    def setTabButton(self, tab1=None, tab2=None , tabsContainer=None, stackedWidget=None):
        
        if tab1 != None:
            tab1.setMaximumWidth(180)
            tab1.setIcon(QIcon(self.icon_path+"table-columns.png"))
            tab1.setStyleSheet(View.tab_button)
            
            if tab2==None:
                tab1.setProperty("active", True)

            tabsContainer.addWidget(tab1)
        
        if tab2 != None:
            tab2.setMaximumWidth(180)
            tab2.setIcon(QIcon(self.icon_path+"apps-add.png"))
            tab2.setStyleSheet(View.tab_button)
            tabsContainer.addWidget(tab2)

        # enable exchange between tabs
        if tab1 != None and tab2 != None:
            tab1.clicked.connect(lambda: self.Tabs(tabs=(tab1,tab2), stacked_widget=stackedWidget, index=0))
            tab2.clicked.connect(lambda: self.Tabs(tabs=(tab2,tab1), stacked_widget=stackedWidget, index=1))

        
        tabsContainer.setAlignment(Qt.AlignLeft)

    def getCellVal(self, table, page=""):
        row = table.currentRow()
        self.hidden_id = table.item(row, 0).text()
        
        match page:
            case "rfid":
                self.row_info_rfid.setText(str(row+1))
            case "users":
                self.row_info_users.setText(str(row+1))
            case "kasir":
                self.row_info_kasir.setText(str(row+1))
            case "karcis":
                ...
                # self.search_data_karcis.setText(str(row+1))
            case "tarif":
                self.row_info_tarif.setText(str(row+1))
            case "voucher":
                self.row_info_voucher.setText(str(row+1))
            case "laporan":
                self.row_info_laporan.setText(str(row+1))
            case default:
                pass

    def fillTableTarif(self, table, cols, query, rows=0):
        
        if rows != 0:
            table.setRowCount(rows)
        
        # loop each row based on query row result
        r = 0
        for l in query:
            
            # set item on table column
            col_index = 0
            for i in range(cols):
                
                # if has reach 3 column in table tarif --> JSON string
                val = str(l[i]) # {"4":"1000", "6":"1000"}
                
                if i == 2:
                    rules = json.loads(val)

                    for k,v in rules.items():
                        # add v->value into
                        item = QTableWidgetItem( v )
                        table.setItem(r, col_index, item)
                        col_index+=1

                else:
                    if val == 'None': val = ""

                    item = QTableWidgetItem( val )
                    table.setItem(r, col_index, item)

                    col_index+=1
            
            r = r + 1

    def createFormContainer(self, scrollable=False):
        
        form_container = QWidget()
        form_container_lay = QVBoxLayout()
        form_container_lay.setContentsMargins(25,25,25,25)
        form_container.setLayout(form_container_lay)
        form_container.setMaximumWidth(800)

        form_container.setStyleSheet("background:#222b45;")
        
        if scrollable:
            screen = self.app.primaryScreen()
            size = screen.size()

            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setMaximumHeight( size.height() - 200 )
            scroll.setWidget(form_container)
            
            return scroll,form_container_lay
        else:
            return form_container,form_container_lay

    def editPopUp(self, form_type="", form_size=(400,400) ):
        
        if self.hidden_id != -1:
            margin_top = "margin-top:30px;"
            id = str(self.hidden_id)

            match form_type.lower():
                case "rfid":
                    res = self.exec_query("select * from rfid where id="+id, "select")
                    
                    components = [
                                        {
                                            "name":"lbl_add_rfid",
                                            "category":"label",
                                            "text": "RFID",
                                            "style":self.primary_lbl
                                        },
                                        {
                                            "name":"add_rfid",
                                            "category":"lineEditInt",
                                            "text":res[0][1],
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
                                            "text":res[0][2],
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

                case "user":
                    
                    res = self.exec_query("select * from users where id="+id, "select")

                    components = [
                                        {
                                            "name":"lbl_add_uname",
                                            "category":"label",
                                            "text": "Username",
                                            "style":self.primary_lbl
                                        },
                                        {
                                            "name":"add_uname",
                                            "category":"lineEdit",
                                            "text":res[0][1],
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
                                            "category":"lineeditpassword",
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
                                            "category":"lineeditpassword",
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
                                            "selected_item": res[0][2],
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
                
                case "kasir":
                    
                    res = self.exec_query("select * from kasir where id="+id, "select")

                    components = [      {
                                            "name":"lbl_add_nik",
                                            "category":"label",
                                            "text": "NIK",
                                            "style":self.primary_lbl
                                        },
                                        {
                                            "name":"add_nik",
                                            "category":"lineEditInt",
                                            "text":res[0][1],
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
                                            "text":res[0][2],
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
                                            "category":"lineEditInt",
                                            "text":res[0][3],
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
                                            "text":res[0][4],
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
                                            "text":res[0][5],
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
                                            "text":res[0][6],
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
                                            "text":res[0][7],
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
                                        }
                                    ]
                
                case "tarif":
                    
                    cols,res = self.exec_query("select * from tarif order by id", "cols_res")
                    
                    tipe_tarif = str(res[1][cols.index('tipe_tarif')])
                    toleransi = str(res[1][cols.index('toleransi')])
                    tarif_dasar_motor = "0"
                    tarif_max_motor = "0"
                    tarif_dasar_mobil = "0"
                    tarif_max_mobil = "0"
                    waktu_max = "0"
                    
                    # components
                    components = [
                                        {
                                            "name":"widget_tipe_tarif",
                                            "category":"widget",
                                            "layout": "VBoxLayout",
                                            "style":self.block_children,
                                            "children":[
                                                {
                                                    "name":"r_progressive",
                                                    "category":"RadioButton",
                                                    "text":"progresif",
                                                    "checked": True if tipe_tarif == "progresif" else False, 
                                                    "style":"border:none;",
                                                    "toggled": {
                                                        "method_name": self.check_tarif_type
                                                    }
                                                },
                                                {
                                                    "name":"r_flat",
                                                    "category":"RadioButton",
                                                    "text":"flat",
                                                    "checked": True if tipe_tarif == "flat" else False, 
                                                    "style":"border:none;",
                                                    "toggled": {
                                                        "method_name": self.check_tarif_type
                                                    } 
                                                },
                                                {
                                                    "name":"r_other",
                                                    "category":"RadioButton",
                                                    "text":"other",
                                                    "checked": True if tipe_tarif == "other" else False, 
                                                    "style":"border:none;",
                                                    "toggled": {
                                                        "method_name": self.check_tarif_type
                                                    }
                                                }
                                            ]
                                        },
                                        {
                                            "name":"widget_toleransi",
                                            "category":"widget",
                                            "layout": "HBoxLayout",
                                            "style":self.block_children,
                                            "children":[
                                                {
                                                    "name":"t_lbl1",
                                                    "category":"label",
                                                    "text":"Toleransi mobil/motor ",
                                                    "style":self.primary_lbl + "border: none;"
                                                },
                                                {
                                                    "name":"add_toleransi",
                                                    "category":"lineEditInt",
                                                    "text":toleransi,
                                                    "style":self.primary_input 
                                                },
                                                {
                                                    "name":"t_lbl2",
                                                    "category":"label",
                                                    "text":" menit",
                                                    "style":self.primary_lbl + "border: none;"
                                                },
                                            ]
                                        },
                                        {
                                            "name":"widget_container_biaya1",
                                            "category":"widget",
                                            "layout": "VBoxLayout",
                                            "style":self.block_children,
                                            "children":[
                                                {
                                                "name":"sub_container1_biaya1",
                                                "category":"widget",
                                                "layout": "HBoxLayout",
                                                "style": "border:none;",
                                                "children":[
                                                    {
                                                        "name":"lbl",
                                                        "category":"label",
                                                        "text":"Tarif: ",
                                                        "style":self.primary_lbl + "border: none;"
                                                    },
                                                    {
                                                        "name":"add_time1",
                                                        "category":"spinbox",
                                                        "range":(0,24),
                                                        "value":"0",
                                                        "style":self.primary_spinbox
                                                    },
                                                    {
                                                        "name":"lbl",
                                                        "category":"label",
                                                        "text":" jam pertama",
                                                        "style":self.primary_lbl + "border: none;"
                                                    }
                                                ]
                                                },
                                                {
                                                "name":"sub_container2_biaya1",
                                                "category":"widget",
                                                "layout": "HBoxLayout",
                                                "style": "border:none;",
                                                "children":[
                                                    {
                                                        "name":"lbl",
                                                        "category":"label",
                                                        "text":"Motor(Rp) ",
                                                        "style":self.primary_lbl + "border: none;"
                                                    },
                                                    {
                                                        "name":"add_motor_biaya1",
                                                        "category":"lineEditInt",
                                                        "text": tarif_dasar_motor,
                                                        "style":self.primary_input 
                                                    },
                                                    {
                                                        "name":"lbl",
                                                        "category":"label",
                                                        "text":"Mobil(Rp) ",
                                                        "style":self.primary_lbl + "border: none;"
                                                    },
                                                    {
                                                        "name":"add_mobil_biaya1",
                                                        "category":"lineEditInt",
                                                        "text": tarif_dasar_mobil,
                                                        "style":self.primary_input 
                                                    }
                                                ]
                                                }
                                            ]
                                        },
                                        {
                                            "name":"widget_container_biaya2",
                                            "category":"widget",
                                            "layout": "VBoxLayout",
                                            "style":self.block_children,
                                            "children":[
                                                {
                                                "name":"sub_container1_biaya2",
                                                "category":"widget",
                                                "layout": "HBoxLayout",
                                                "style": "border:none;",
                                                "children":[
                                                    {
                                                        "name":"lbl",
                                                        "category":"label",
                                                        "text":"Tarif: ",
                                                        "style":self.primary_lbl + "border: none;"
                                                    },
                                                    {
                                                        "name":"add_time2",
                                                        "category":"lineEditInt",
                                                        "text": "0",
                                                        "style":self.primary_input 
                                                    },
                                                    {
                                                        "name":"lbl",
                                                        "category":"label",
                                                        "text":" jam berikutnya",
                                                        "style":self.primary_lbl + "border: none;"
                                                    }
                                                ]
                                                },
                                                {
                                                "name":"sub_container2_biaya2",
                                                "category":"widget",
                                                "layout": "HBoxLayout",
                                                "style": "border:none;",
                                                "children":[
                                                    {
                                                        "name":"lbl",
                                                        "category":"label",
                                                        "text":"Motor(Rp) ",
                                                        "style":self.primary_lbl + "border: none;"
                                                    },
                                                    {
                                                        "name":"add_motor_biaya2",
                                                        "category":"lineEditInt",
                                                        "text": "0",
                                                        "style":self.primary_input 
                                                    },
                                                    {
                                                        "name":"lbl",
                                                        "category":"label",
                                                        "text":"Mobil(Rp) ",
                                                        "style":self.primary_lbl + "border: none;"
                                                    },
                                                    {
                                                        "name":"add_mobil_biaya2",
                                                        "category":"lineEditInt",
                                                        "text": "0",
                                                        "style":self.primary_input 
                                                    }
                                                ]
                                                }
                                            ]
                                        },
                                        {
                                            "name":"widget_container_biaya3",
                                            "category":"widget",
                                            "layout": "VBoxLayout",
                                            "style":self.block_children,
                                            "children":[
                                                {
                                                "name":"sub_container1_biaya3",
                                                "category":"widget",
                                                "layout": "HBoxLayout",
                                                "style": "border:none;",
                                                "children":[
                                                    {
                                                        "name":"lbl",
                                                        "category":"label",
                                                        "text":"Tarif: ",
                                                        "style":self.primary_lbl + "border: none;"
                                                    },
                                                    {
                                                        "name":"add_time3",
                                                        "category":"lineEditInt",
                                                        "text": "0",
                                                        "style":self.primary_input 
                                                    },
                                                    {
                                                        "name":"lbl",
                                                        "category":"label",
                                                        "text":" jam berikutnya",
                                                        "style":self.primary_lbl + "border: none;"
                                                    }
                                                ]
                                                },
                                                {
                                                "name":"sub_container2_biaya3",
                                                "category":"widget",
                                                "layout": "HBoxLayout",
                                                "style": "border:none;",
                                                "children":[
                                                    {
                                                        "name":"lbl",
                                                        "category":"label",
                                                        "text":"Motor(Rp) ",
                                                        "style":self.primary_lbl + "border: none;"
                                                    },
                                                    {
                                                        "name":"add_motor_biaya3",
                                                        "category":"lineEditInt",
                                                        "text": "0",
                                                        "style":self.primary_input 
                                                    },
                                                    {
                                                        "name":"lbl",
                                                        "category":"label",
                                                        "text":"Mobil(Rp) ",
                                                        "style":self.primary_lbl + "border: none;"
                                                    },
                                                    {
                                                        "name":"add_mobil_biaya3",
                                                        "category":"lineEditInt",
                                                        "text": "0",
                                                        "style":self.primary_input 
                                                    }
                                                ]
                                                }
                                            ]
                                        },
                                        {
                                            "name":"widget_container_biaya4",
                                            "category":"widget",
                                            "layout": "VBoxLayout",
                                            "style":self.block_children,
                                            "children":[
                                                {
                                                "name":"sub_container1_biaya4",
                                                "category":"widget",
                                                "layout": "HBoxLayout",
                                                "style": "border:none;",
                                                "children":[
                                                    {
                                                        "name":"lbl",
                                                        "category":"label",
                                                        "text":"Tarif maksimal per ",
                                                        "style":self.primary_lbl + "border: none;"
                                                    },
                                                    {
                                                        "name":"add_time4",
                                                        "category":"lineEditInt",
                                                        "text": "0",
                                                        "style":self.primary_input 
                                                    },
                                                    {
                                                        "name":"lbl",
                                                        "category":"label",
                                                        "text":" jam",
                                                        "style":self.primary_lbl + "border: none;"
                                                    }
                                                ]
                                                },
                                                {
                                                "name":"sub_container2_biaya4",
                                                "category":"widget",
                                                "layout": "HBoxLayout",
                                                "style": "border:none;",
                                                "children":[
                                                    {
                                                        "name":"lbl",
                                                        "category":"label",
                                                        "text":"Motor(Rp) ",
                                                        "style":self.primary_lbl + "border: none;"
                                                    },
                                                    {
                                                        "name":"add_motor_biaya4",
                                                        "category":"lineEditInt",
                                                        "text": "0",
                                                        "style":self.primary_input 
                                                    },
                                                    {
                                                        "name":"lbl",
                                                        "category":"label",
                                                        "text":"Mobil(Rp) ",
                                                        "style":self.primary_lbl + "border: none;"
                                                    },
                                                    {
                                                        "name":"add_mobil_biaya4",
                                                        "category":"lineEditInt",
                                                        "text": "0",
                                                        "style":self.primary_input 
                                                    }
                                                ]
                                                }
                                            ]
                                        },
                                        {
                                            "name":"btn_add_tarif",
                                            "category":"pushButton",
                                            "text": "Save",
                                            "clicked": {
                                                    "method_name": self.set_tarif
                                            },
                                            "style": self.primary_button
                                        }
                                    ]
                    
                        

                case "voucher":
                    res = self.exec_query("select * from voucher where id="+id, "select")
                    
                    components = [{
                                        "name":"lbl_add_voucher_idpel",
                                        "category":"label",
                                        "text": "ID Pel",
                                        "style":self.primary_lbl
                                    },
                                    {
                                        "name":"add_voucher_idpel",
                                        "category":"lineEditInt",
                                        "text":str(res[0][1]),
                                        "style":self.primary_input
                                    },
                                    {
                                        "name":"lbl_add_voucher_lokasi",
                                        "category":"label",
                                        "text": "Lokasi",
                                        "style":self.primary_lbl + margin_top
                                    },
                                    {
                                        "name":"add_voucher_lokasi",
                                        "category":"lineEdit",
                                        "text":res[0][2],
                                        "style":self.primary_input
                                    },
                                    {
                                        "name":"lbl_add_voucher_tarif",
                                        "category":"label",
                                        "text": "Tarif",
                                        "style":self.primary_lbl + margin_top
                                    },
                                    {
                                        "name":"add_voucher_tarif",
                                        "category":"lineEditInt",
                                        "text":str(res[0][3]),
                                        "style":self.primary_input
                                    },
                                    {
                                        "name":"lbl_add_voucher_masa_berlaku",
                                        "category":"label",
                                        "text": "Masa Berlaku",
                                        "style":self.primary_lbl + margin_top
                                    },
                                    {
                                        "name":"add_voucher_masa_berlaku",
                                        "category":"date",
                                        "reg_date":str(res[0][4]),
                                        "style":self.primary_input
                                    },
                                    {
                                        "name":"lbl_add_voucher_jns_kendaraan",
                                        "category":"label",
                                        "text": "Jenis Kendaraan",
                                        "style":self.primary_lbl + margin_top
                                    },
                                    {
                                        "name":"add_voucher_jns_kendaraan",
                                        "category":"comboBox",
                                        "items":["Motor", "Mobil"],
                                        "selected_item":res[0][5],
                                        "style":self.primary_combobox
                                    },
                                    {
                                        "name":"btn_add_voucher",
                                        "category":"pushButton",
                                        "text": "Save",
                                        "clicked": {
                                                "method_name": self.save_edit_voucher
                                        },
                                        "style": self.primary_button
                                    }
                                ]

                case default:
                    pass    

            self.win = QMainWindow()
            central_widget = QWidget()
            central_lay = QVBoxLayout()
            scroll = QScrollArea()
            scroll.setWidget(central_widget)
            scroll.setWidgetResizable(True)
            # scroll.setMinimumWidth(250)
            # scroll.setMaximumHeight(700)

            central_lay.setContentsMargins(25,25,25,25)
            central_widget.setStyleSheet("background:#222b45;")

            self.CreateComponentLayout(components, central_lay)
            central_lay.addStretch(1)
            
            central_widget.setLayout(central_lay)
            # print("H: ", self.win.height())

            self.win.setWindowTitle(f"Edit Form {form_type}")
            self.win.resize(form_size[0], form_size[1])
            
            # self.win.setMinimumWidth(400)
            # self.win.setMinimumHeight(400)
            # self.win.setMaximumHeight(700)
            
            self.win.setCentralWidget(scroll)
            
            # Run method after components create
            if form_type.lower() == "tarif":
                self.check_tarif_type(tipe_tarif)
                # print("==> tipe tarif: ", tipe_tarif)

            self.win.show()
    
    
    
    def prevNext(self, btnType):
        
        if btnType=="prev":
            if self.row_offset > 0:
                self.row_offset -= self.row_limit
                self.start = self.row_offset + 1
                self.end = min( self.row_offset + self.row_limit, self.karcis_rows[0][0] )

        elif btnType=="next":
            if self.row_offset + self.row_limit < self.karcis_rows[0][0]:
                self.row_offset += self.row_limit
                self.start = self.row_offset + 1
                self.end = min( self.row_offset + self.row_limit, self.karcis_rows[0][0] )

        
        # refill/refresh table with new offset
        try:
            query = self.exec_query(f"{self.query_search} limit {self.row_limit} OFFSET {self.row_offset}", "SELECT")
        except:
            query = self.exec_query(f"SELECT id, barcode,  nopol, jenis_kendaraan, gate, cast(datetime as date), cast(date_keluar as date), lama_parkir, status_parkir, tarif, jns_transaksi, kd_shift FROM karcis order by id limit {self.row_limit} OFFSET {self.row_offset}", "SELECT")
        
        rows_count = len(query)

        if rows_count > 0:
            cols = 11

            self.laporan_table.setRowCount(rows_count)
            self.fillTableKarcis(self.laporan_table, cols, query, index_tgl_masuk=5, index_tgl_keluar=6)

            try:    
                self.lbl_count.setText(f"{self.start}-{self.end} from {self.karcis_rows[0][0]} results")
            except:
                ...
        
    # def set_image(self, image):
    #     self.image_label.setPixmap(QPixmap.fromImage(image))

    
    def play(self):
        ...
        # ret_1, frame_1 = self.cap_1.read()
        # ret_2, frame_2 = self.cap_2.read()

        # if ret_1:
        #     frame_1 = cv2.cvtColor(frame_1, cv2.COLOR_BGR2RGB)
        #     image_1 = QImage(frame_1, frame_1.shape[1], frame_1.shape[0], frame_1.strides[0], QImage.Format_RGB888)
        #     self.image_label.setPixmap(QPixmap.fromImage(image_1))

        # if ret_2:
        #     frame_2 = cv2.cvtColor(frame_2, cv2.COLOR_BGR2RGB)
        #     image_2 = QImage(frame_2, frame_2.shape[1], frame_2.shape[0], frame_2.strides[0], QImage.Format_RGB888)
        #     self.image_label2.setPixmap(QPixmap.fromImage(image_2))

    def findVoucher(self):
        print("search voucher status ... ")

    def PopUpReportUser(self):

        dlg = QMessageBox(self.window)
        dlg.setWindowTitle( "test title" )
        dlg.setLayout(QVBoxLayout())
        label = QLabel("This is a popup window")
        dlg.layout().addWidget(label)

        # dlg.setText( msg )
        # dlg.setIcon(QMessageBox.Information)
        
        dlg.exec()


    def openGate(self):
        print("OPEN GATE KELUAR")
        
        # modal
        dlg = QMessageBox(self.window)
        
        dlg.setWindowTitle("Alert")
        dlg.setText("OPEN GATE KELUAR --> send to microcontroller")
        dlg.setIcon(QMessageBox.Information)
        dlg.exec()

    def keyShortcut(self, keyCombination="", targetWidget=None, command=""):
        
        shortcut = QShortcut(QKeySequence(keyCombination), self.window)
        
        if command=="":
            shortcut.activated.connect( targetWidget.setFocus )
        elif command=="pay":
            shortcut.activated.connect( self.setPay )
        
        elif command=="save": #laporan user bermasalah
            shortcut.activated.connect( self.setReport )
        
        elif command=="popup-user-bermasalah":
            shortcut.activated.connect( self.PopUpReportUser )
            
        elif command=="open-gate":
            shortcut.activated.connect( self.openGate )
        elif command=="search-voucher":
            shortcut.activated.connect( self.findVoucher )

    def setColsStretch(self, table, cols):
        header = table.horizontalHeader()
        for i in range(cols):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

    def createPage(self, page=""):
        
        margin_top = "margin-top:30px;"

        match page:
            
            case "home":
                # welcome label
                self.welcome_lbl = QLabel("Manless Parking System")
                self.welcome_lbl.setFont( self.fontStyle("Helvetica", 50, 80) )
                self.welcome_lbl.setAlignment(Qt.AlignCenter)
                self.welcome_lbl.setStyleSheet("background-color:#151930; color:#fff;")
            
            case "rfid":
                # rfid content
                self.rfid_container = QWidget()
                self.rfid_container_lay = QVBoxLayout()
                rfid_tabs_container_widget = QWidget()
                
                rfid_tabs_container = QHBoxLayout()
                self.rfid_tab1 = QPushButton("Kelola RFID")
                rfid_tab2 = QPushButton("Tambah RFID")
                
                self.rfid_stack = QStackedWidget()
                rfid_content1 = QWidget()
                rfid_content2 = QWidget()
                
                # tabs
                self.setTabButton(tab1=self.rfid_tab1, tab2=rfid_tab2, tabsContainer=rfid_tabs_container, stackedWidget=self.rfid_stack)
                
                # set rfid layout & widget
                self.rfid_container_lay.setContentsMargins(0,0,0,0)
                self.rfid_container_lay.setSpacing(0)

                rfid_tabs_container_widget.setStyleSheet("background: #151930;")
                self.rfid_stack.setStyleSheet("background: #151930;")
                
                self.rfid_container.setLayout(self.rfid_container_lay)
                rfid_tabs_container_widget.setLayout(rfid_tabs_container)
                rfid_tabs_container.setContentsMargins(25, 20, 0, 0)

                self.rfid_container_lay.addWidget(rfid_tabs_container_widget)
                self.rfid_container_lay.addWidget(self.rfid_stack)

                # add tabs
                self.rfid_stack.addWidget(rfid_content1)
                self.rfid_stack.addWidget(rfid_content2)
                
                # set widget and layout
                rfid_content1_lay = QVBoxLayout()
                rfid_content1.setLayout( rfid_content1_lay )

                # set widget and layout
                rfid_content2_lay = QVBoxLayout()
                rfid_content2.setLayout( rfid_content2_lay )

                ############### FORM CONTAINER ##############
                res = self.createFormContainer()
                form_container = res[0]
                form_container_lay = res[1]
                ############################################

                rfid_content2_lay.setContentsMargins(25,25,25,25)
                rfid_content2_lay.addWidget(form_container)

                # set widget for tab1 layout
                tab1_h_widget = QWidget()
                tab1_h_layout = QHBoxLayout()
                tab1_h_widget.setLayout(tab1_h_layout)
                self.rfid_table = QTableWidget()
                
                # action layout
                action_widget = QWidget()
                action_lay = QVBoxLayout()
                action_widget.setLayout(action_lay)
                action_widget.setMaximumWidth(120)
                action_widget.setStyleSheet("border: none;")
                action_lay.setContentsMargins(0,0,0,0)
                action_lay.setSpacing(0)

                
                
                ################# action lineedit and button #####################
                row_label = QLabel("No Baris:")
                self.row_info_rfid = QLineEdit()
                row_search = QPushButton("edit")
                row_delete = QPushButton("delete")
                row_search.setIcon(QIcon(self.icon_path+"blog-pencil.png"))
                row_delete.setIcon(QIcon(self.icon_path+"trash.png"))


                row_label.setStyleSheet("color:#fff; font-size:13px; font-weight: 500; background:#384F67; margin-bottom: 5px; padding:5px;")
                self.row_info_rfid.setReadOnly(True)
                self.row_info_rfid.setStyleSheet("background:#fff; padding:8px; margin-bottom: 5px; color: #000; border:none;")
                row_search.setStyleSheet(View.edit_btn_action)
                row_delete.setStyleSheet(View.del_btn_action)

                # add lineedit and button into action_lay
                action_lay.addWidget(row_label)
                action_lay.addWidget(self.row_info_rfid)
                action_lay.addWidget(row_search)
                action_lay.addWidget(row_delete)
                action_lay.addStretch(1)

                ##################### action edit & delete ###################

                row_search.clicked.connect(lambda: self.editPopUp(form_type="RFID", form_size=(400, 300)))
                row_delete.clicked.connect(lambda: self.deleteData("RFID"))
                
                ###################################################################



                ######################### RFID Table ##############################
                # add table and action widget into tab1_h_layout
                tab1_h_layout.addWidget(self.rfid_table)
                tab1_h_layout.addWidget(action_widget)

                # create table widget
                
                # fetch data from DB
                query = self.exec_query("SELECT id, rfid, nama FROM rfid order by nama", "SELECT")
                rows_count = len(query)
                cols = 3

                self.rfid_table.resizeRowsToContents()
                self.rfid_table.horizontalHeader().setStretchLastSection(True)
                

                self.rfid_table.setRowCount(rows_count)
                self.rfid_table.setColumnCount(cols)
                
                self.rfid_table.setHorizontalHeaderLabels(["id", "RFID", "Nama Karyawan"])
                self.rfid_table.setStyleSheet(View.table_style)

                self.rfid_table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
                self.rfid_table.setColumnHidden(0, True) #hide id column
                
                self.fillTable(self.rfid_table, cols, query)
               
                # create edit & delete section
                self.rfid_table.setSelectionBehavior(QTableWidget.SelectRows)
                self.rfid_table.clicked.connect(lambda: self.getCellVal(self.rfid_table, page="rfid"))
                
                rfid_content1_lay.addWidget(tab1_h_widget)
               
                rfid_content1_lay.addWidget(tab1_h_widget)
                
                ###################################################################



                ###################### RFID Form ######################
                # components
                components_setter = [
                                    {
                                        "name":"lbl_add_rfid",
                                        "category":"label",
                                        "text": "RFID",
                                        "style":self.primary_lbl
                                    },
                                    {
                                        "name":"add_rfid",
                                        "category":"lineEditInt",
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
                
                self.CreateComponentLayout(components_setter, form_container_lay)
                rfid_content2_lay.addStretch(1)
                #######################################################            
            
            case "users":
                # users content
                self.users_container = QWidget()
                self.users_container_lay = QVBoxLayout()
                users_tabs_container_widget = QWidget()
                
                users_tabs_container = QHBoxLayout()
                self.users_tab1 = QPushButton("Kelola users")
                users_tab2 = QPushButton("Tambah users")
                
                self.users_stack = QStackedWidget()
                users_content1 = QWidget()
                users_content2 = QWidget()
                
                # tabs
                self.setTabButton(tab1=self.users_tab1, tab2=users_tab2, tabsContainer=users_tabs_container, stackedWidget=self.users_stack)
                
                # set users layout & widget
                self.users_container_lay.setContentsMargins(0,0,0,0)
                self.users_container_lay.setSpacing(0)

                users_tabs_container_widget.setStyleSheet("background: #151930;")
                self.users_stack.setStyleSheet("background: #151930;")
                
                self.users_container.setLayout(self.users_container_lay)
                users_tabs_container_widget.setLayout(users_tabs_container)
                users_tabs_container.setContentsMargins(25, 20, 0, 0)

                self.users_container_lay.addWidget(users_tabs_container_widget)
                self.users_container_lay.addWidget(self.users_stack)

                # add tabs
                self.users_stack.addWidget(users_content1)
                self.users_stack.addWidget(users_content2)
                
                # set widget and layout
                users_content1_lay = QVBoxLayout()
                users_content1.setLayout( users_content1_lay )

                # set widget and layout
                users_content2_lay = QVBoxLayout()
                users_content2.setLayout( users_content2_lay )

                ############### FORM CONTAINER ##############
                res = self.createFormContainer()
                form_container = res[0]
                form_container_lay = res[1]
                ############################################

                users_content2_lay.setContentsMargins(25,25,25,25)
                users_content2_lay.addWidget(form_container)

                # set widget for tab1 layout
                tab1_h_widget = QWidget()
                tab1_h_layout = QHBoxLayout()
                tab1_h_widget.setLayout(tab1_h_layout)
                self.user_table = QTableWidget()
                
                # action layout
                action_widget = QWidget()
                action_lay = QVBoxLayout()
                action_widget.setLayout(action_lay)
                action_widget.setMaximumWidth(120)
                action_widget.setStyleSheet("border: none;")
                action_lay.setContentsMargins(0,0,0,0)
                action_lay.setSpacing(0)

                ################# action lineedit and button ###################
                row_label = QLabel("No Baris:")
                self.row_info_users = QLineEdit()
                row_search = QPushButton("edit")
                row_delete = QPushButton("delete")
                row_search.setIcon(QIcon(self.icon_path+"blog-pencil.png"))
                row_delete.setIcon(QIcon(self.icon_path+"trash.png"))

                row_label.setStyleSheet("color:#fff; font-size:13px; font-weight: 500; background:#384F67; margin-bottom: 5px; padding:5px;")
                self.row_info_users.setReadOnly(True)
                self.row_info_users.setStyleSheet("background:#fff; padding:8px; margin-bottom: 5px; color: #000; border:none;")
                row_search.setStyleSheet(View.edit_btn_action)
                row_delete.setStyleSheet(View.del_btn_action)

                # add lineedit and button into action_lay
                action_lay.addWidget(row_label)
                action_lay.addWidget(self.row_info_users)
                action_lay.addWidget(row_search)
                action_lay.addWidget(row_delete)
                action_lay.addStretch(1)


                ##################### action edit & delete ###################
                
                row_search.clicked.connect(lambda: self.editPopUp(form_type="user", form_size=(400, 400)))
                row_delete.clicked.connect(lambda: self.deleteData("user"))

                ##############################################################


                ######################### User Table ##############################
                # add table and action widget into tab1_h_layout
                tab1_h_layout.addWidget(self.user_table)
                tab1_h_layout.addWidget(action_widget)

                # create table widget

                # fetch data from DB
                query = self.exec_query("SELECT id, username, user_level FROM users", "SELECT")
                rows_count = len(query)
                cols = 3

                self.user_table.resizeRowsToContents()
                self.user_table.horizontalHeader().setStretchLastSection(True)

                self.user_table.setRowCount(rows_count)
                self.user_table.setColumnCount(cols)

                self.user_table.setHorizontalHeaderLabels(["id", "Username", "Level"])
                self.user_table.setStyleSheet(View.table_style)

                self.user_table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
                self.user_table.setColumnHidden(0, True) #hide id column
                
                self.fillTable(self.user_table, cols, query)

                # create edit & delete section
                self.user_table.setSelectionBehavior(QTableWidget.SelectRows)
                self.user_table.clicked.connect(lambda: self.getCellVal(self.user_table, page="users"))
                
                # users_content1_lay.addWidget(table)
                users_content1_lay.addWidget(tab1_h_widget)

                ###########################################################


                ###################### users Form ######################
                # components
                components_setter = [
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
                                        "category":"lineeditpassword",
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
                                        "category":"lineeditpassword",
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
                
                self.CreateComponentLayout(components_setter, form_container_lay)
                users_content2_lay.addStretch(1)
                #######################################################
            
            case "kasir":
                # kasir content
                self.kasir_container = QWidget()
                self.kasir_container_lay = QVBoxLayout()
                kasir_tabs_container_widget = QWidget()
                
                kasir_tabs_container = QHBoxLayout()
                self.kasir_tab1 = QPushButton("Kelola kasir")
                kasir_tab2 = QPushButton("Tambah kasir")
                
                self.kasir_stack = QStackedWidget()
                kasir_content1 = QWidget()
                kasir_content2 = QWidget()
                
                # tabs
                self.setTabButton(tab1=self.kasir_tab1, tab2=kasir_tab2, tabsContainer=kasir_tabs_container, stackedWidget=self.kasir_stack)
                
                # set kasir layout & widget
                self.kasir_container_lay.setContentsMargins(0,0,0,0)
                self.kasir_container_lay.setSpacing(0)

                kasir_tabs_container_widget.setStyleSheet("background: #151930;")
                self.kasir_stack.setStyleSheet("background: #151930;")
                
                self.kasir_container.setLayout(self.kasir_container_lay)
                kasir_tabs_container_widget.setLayout(kasir_tabs_container)
                kasir_tabs_container.setContentsMargins(25, 20, 0, 0)

                self.kasir_container_lay.addWidget(kasir_tabs_container_widget)
                self.kasir_container_lay.addWidget(self.kasir_stack)

                # add tabs
                self.kasir_stack.addWidget(kasir_content1)
                self.kasir_stack.addWidget(kasir_content2)
                
                # set widget and layout
                kasir_content1_lay = QVBoxLayout()
                kasir_content1.setLayout( kasir_content1_lay )

                # set widget and layout
                kasir_content2_lay = QVBoxLayout()
                kasir_content2.setLayout( kasir_content2_lay )

                ############### FORM CONTAINER ##############
                res = self.createFormContainer(scrollable=True)
                form_container = res[0]
                # form_container.setMinimumHeight(650)
                form_container_lay = res[1]

                ############################################

                kasir_content2_lay.setContentsMargins(25,0,25,0)
                kasir_content2_lay.addWidget(form_container)

                

                # set widget for tab1 layout
                tab1_h_widget = QWidget()
                tab1_h_layout = QHBoxLayout()
                tab1_h_widget.setLayout(tab1_h_layout)
                self.kasir_table = QTableWidget()
                
                # action layout
                action_widget = QWidget()
                action_lay = QVBoxLayout()
                action_widget.setLayout(action_lay)
                action_widget.setMaximumWidth(120)
                action_widget.setStyleSheet("border: none;")
                action_lay.setContentsMargins(0,0,0,0)
                action_lay.setSpacing(0)

                ################# action lineedit and button ###################
                row_label = QLabel("No Baris:")
                self.row_info_kasir = QLineEdit()
                row_search = QPushButton("edit")
                row_delete = QPushButton("delete")
                row_search.setIcon(QIcon(self.icon_path+"blog-pencil.png"))
                row_delete.setIcon(QIcon(self.icon_path+"trash.png"))

                row_label.setStyleSheet("color:#fff; font-size:13px; font-weight: 500; background:#384F67; margin-bottom: 5px; padding:5px;")
                self.row_info_kasir.setReadOnly(True)
                self.row_info_kasir.setStyleSheet("background:#fff; padding:8px; margin-bottom: 5px; color: #000; border:none;")
                row_search.setStyleSheet(View.edit_btn_action)
                row_delete.setStyleSheet(View.del_btn_action)

                # add lineedit and button into action_lay
                action_lay.addWidget(row_label)
                action_lay.addWidget(self.row_info_kasir)
                action_lay.addWidget(row_search)
                action_lay.addWidget(row_delete)
                action_lay.addStretch(1)


                ##################### action edit & delete ###################
                
                row_search.clicked.connect(lambda: self.editPopUp(form_type="kasir", form_size=(500, 700)))
                row_delete.clicked.connect(lambda: self.deleteData("kasir"))

                ##############################################################


                ######################### kasir Table ##############################
                # add table and action widget into tab1_h_layout
                tab1_h_layout.addWidget(self.kasir_table)
                tab1_h_layout.addWidget(action_widget)

                # create table widget

                # fetch data from DB
                query = self.exec_query("SELECT id, nik, nama, hp, alamat, jm_masuk, jm_keluar, no_pos FROM kasir", "SELECT")
                rows_count = len(query)
                cols = 8

                self.kasir_table.resizeRowsToContents()
                self.kasir_table.horizontalHeader().setStretchLastSection(True)

                self.kasir_table.setRowCount(rows_count)
                self.kasir_table.setColumnCount(cols)

                self.kasir_table.setHorizontalHeaderLabels(["id", "NIK", "Nama", "HP", "Alamat", "Jam Masuk", "Jam Kel", "POS/GATE"])
                self.kasir_table.setStyleSheet(View.table_style)

                self.kasir_table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
                self.kasir_table.setColumnHidden(0, True) #hide id column
                
                self.fillTable(self.kasir_table, cols, query)

                # create edit & delete section
                self.kasir_table.setSelectionBehavior(QTableWidget.SelectRows)
                self.kasir_table.clicked.connect(lambda: self.getCellVal(self.kasir_table, page="kasir"))
                
                # kasir_content1_lay.addWidget(table)
                kasir_content1_lay.addWidget(tab1_h_widget)

                ###########################################################


                ###################### kasir Form ######################

                # components
                components_setter = [
                                    {
                                        "name":"lbl_add_nik",
                                        "category":"label",
                                        "text": "NIK",
                                        "style":self.primary_lbl
                                    },
                                    {
                                        "name":"add_nik",
                                        "category":"lineEditInt",
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
                                        "category":"lineEditInt",
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
                                    }
                                ]

                self.CreateComponentLayout(components_setter, form_container_lay)
                # kasir_content2_lay.addStretch(1)
                #######################################################

            case "karcis":
                # karcis content
                self.karcis_container = QWidget()
                self.karcis_container_lay = QVBoxLayout()
                karcis_tabs_container_widget = QWidget()
                
                karcis_tabs_container = QHBoxLayout()
                self.karcis_tab1 = QPushButton("Setting karcis")
                karcis_tab2 = QPushButton("Setting karcis")
                
                self.karcis_stack = QStackedWidget()
                karcis_content1 = QWidget()
                karcis_content2 = QWidget()
                
                # tabs
                self.setTabButton(tab1=self.karcis_tab1, tab2=None, tabsContainer=karcis_tabs_container, stackedWidget=self.karcis_stack)
                
                # set karcis layout & widget
                self.karcis_container_lay.setContentsMargins(0,0,0,0)
                self.karcis_container_lay.setSpacing(0)

                karcis_tabs_container_widget.setStyleSheet("background: #151930;")
                self.karcis_stack.setStyleSheet("background: #151930;")
                
                self.karcis_container.setLayout(self.karcis_container_lay)
                karcis_tabs_container_widget.setLayout(karcis_tabs_container)
                karcis_tabs_container.setContentsMargins(25, 20, 0, 0)

                self.karcis_container_lay.addWidget(karcis_tabs_container_widget)
                self.karcis_container_lay.addWidget(self.karcis_stack)

                # add tabs
                self.karcis_stack.addWidget(karcis_content2)
                # self.karcis_stack.addWidget(karcis_content2)
                
                # set widget and layout
                karcis_content1_lay = QVBoxLayout()
                karcis_content1.setLayout( karcis_content1_lay )

                # set widget and layout
                karcis_content2_lay = QVBoxLayout()
                karcis_content2.setLayout( karcis_content2_lay )

                ############### FORM CONTAINER ##############
                res = self.createFormContainer()
                form_container = res[0]
                form_container_lay = res[1]
                ############################################

                karcis_content2_lay.setContentsMargins(25,25,25,25)
                karcis_content2_lay.addWidget(form_container)

                # set widget for tab1 layout
                tab1_h_widget = QWidget()
                tab1_h_layout = QHBoxLayout()
                tab1_h_widget.setLayout(tab1_h_layout)
                self.karcis_table = QTableWidget()
                
                # action layout
                action_widget = QWidget()
                action_lay = QVBoxLayout()
                action_widget.setLayout(action_lay)
                action_widget.setMaximumWidth(120)
                action_widget.setStyleSheet("border: none;")
                action_lay.setContentsMargins(0,0,0,0)
                action_lay.setSpacing(0)

                ################# action lineedit and button ###################
                row_label = QLabel("Search Data:")
                self.search_data_karcis = QLineEdit()
                row_search = QPushButton("search")
                row_search.setIcon(QIcon(self.icon_path+"search.png"))
                row_detail = QPushButton("details")
                row_detail.setIcon(QIcon(self.icon_path+"layout-fluid.png"))
                row_refresh = QPushButton("refresh")
                row_refresh.setIcon(QIcon(self.icon_path+"refresh.png"))
                
                row_label.setStyleSheet("color:#fff; font-size:13px; font-weight: 500; background:#384F67; margin-bottom: 5px; padding:5px;")
                self.search_data_karcis.setStyleSheet("background:#fff; padding:8px; margin-bottom: 5px; color: #000; border:none;")
                row_search.setStyleSheet(View.edit_btn_action)
                row_detail.setStyleSheet(View.detail_btn_action)
                row_refresh.setStyleSheet(View.print_btn_action)
                
                # add lineedit and button into action_lay
                action_lay.addWidget(row_label)
                action_lay.addWidget(self.search_data_karcis)
                action_lay.addWidget(row_search)
                action_lay.addWidget(row_detail)
                action_lay.addWidget(row_refresh)
                action_lay.addStretch(1)


                ##################### action edit & delete ##################
                
                row_search.clicked.connect(self.searchKarcis)
                row_detail.clicked.connect(lambda: self.detailPopUp(form_type="karcis", form_size=(400, 600)))
                row_refresh.clicked.connect(self.refreshKarcis)
               
                ##############################################################


                ######################### karcis Table ##############################
                # add table and action widget into tab1_h_layout
                # prev next button
                prev_btn = QPushButton("PREV")
                next_btn = QPushButton("NEXT")
                prev_btn.setMaximumWidth(100)
                next_btn.setMaximumWidth(100)
                prev_btn.setIcon(QIcon(self.icon_path+"angle-left.png"))
                next_btn.setIcon(QIcon(self.icon_path+"angle-right.png"))
                next_btn.setLayoutDirection(Qt.RightToLeft)

                prev_btn.setStyleSheet("background: #00b894; color:#fff;")
                next_btn.setStyleSheet("background: #ff7675; color:#fff;")
                
                # set click method prev-next button
                prev_btn.clicked.connect(lambda: self.prevNext("prev"))
                next_btn.clicked.connect(lambda: self.prevNext("next"))

                # prev next buton container
                prev_next_cont_widget = QWidget()
                prev_next_cont_lay = QHBoxLayout()
                prev_next_cont_widget.setLayout( prev_next_cont_lay )
                prev_next_cont_lay.setAlignment(Qt.AlignCenter)
                prev_next_cont_lay.setContentsMargins(0,15,0,0)

                # add button prev-next into container
                prev_next_cont_lay.addWidget(prev_btn)
                prev_next_cont_lay.addWidget(next_btn)

                tabl_pg_cont_widget = QWidget()
                tabl_pg_cont = QVBoxLayout()

                tabl_pg_cont_widget.setLayout(tabl_pg_cont)

                tabl_pg_cont.addWidget(self.karcis_table)
                tabl_pg_cont.addWidget(prev_next_cont_widget)

                tabl_pg_cont.setContentsMargins(0,0,0,0)
                tabl_pg_cont.setSpacing(0)

                # add table and action widget container into horizontal layout
                tab1_h_layout.addWidget(tabl_pg_cont_widget)
                tab1_h_layout.addWidget(action_widget)

                # create table widget

                # fetch data from DB
                self.row_offset = 0
                query = self.exec_query(f"SELECT id, barcode,  cast(datetime as date), cast(date_keluar as date), gate, status_parkir, jenis_kendaraan, tarif FROM karcis limit 18 OFFSET {self.row_offset}", "SELECT")
                rows_count = len(query)
                cols = 8

                self.karcis_table.resizeRowsToContents()
                self.karcis_table.horizontalHeader().setStretchLastSection(True)

                self.karcis_table.setRowCount(rows_count)
                self.karcis_table.setColumnCount(cols)

                self.karcis_table.setHorizontalHeaderLabels(["id", "Barcode", "TGL Masuk", "TGL Keluar", "Gate", "Status Parkir", "Jenis Kendaraan" , "Tarif"])
                self.karcis_table.setStyleSheet(View.table_style)

                self.karcis_table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
                self.karcis_table.setColumnHidden(0, True) #hide id column
                
                self.fillTable(self.karcis_table, cols, query)

                # create edit & delete section
                self.karcis_table.setSelectionBehavior(QTableWidget.SelectRows)
                self.karcis_table.clicked.connect(lambda: self.getCellVal(self.karcis_table, page="karcis"))
                
                # karcis_content1_lay.addWidget(table)
                
                karcis_content1_lay.addWidget(tab1_h_widget)
                
                ###########################################################


                ###################### karcis Form ######################

                # components
                components_setter = [{
                                        "name":"lbl_nm_tempat",
                                        "category":"label",
                                        "text": "Nama Tempat",
                                        "style":self.primary_lbl
                                    },
                                    {
                                        "name":"add_tempat",
                                        "category":"lineEdit",
                                        "style":self.primary_input
                                    },
                                    {
                                        "name":"lbl_footer1",
                                        "category":"label",
                                        "text": "Footer-1",
                                        "style":self.primary_lbl + margin_top
                                    },
                                    {
                                        "name":"add_footer1",
                                        "category":"lineEdit",
                                        "text": "Simpan Karcis Anda",
                                        "style":self.primary_input
                                    },
                                    {
                                        "name":"lbl_footer2",
                                        "category":"label",
                                        "text": "Footer-2",
                                        "style":self.primary_lbl + margin_top
                                    },
                                    {
                                        "name":"add_footer2",
                                        "category":"lineEdit",
                                        "text": "Hilang Karcis Dikenakan Denda Rp 15.000",
                                        "style":self.primary_input
                                    },
                                    {
                                        "name":"lbl_footer3",
                                        "category":"label",
                                        "text": "Footer-3",
                                        "style":self.primary_lbl + margin_top
                                    },
                                    {
                                        "name":"add_footer3",
                                        "category":"lineEdit",
                                        "text": "Jangan Tinggalkan Barang Berharga",
                                        "style":self.primary_input
                                    },
                                    {
                                        "name":"btn_add_tarif",
                                        "category":"pushButton",
                                        "text": "Save",
                                        "clicked": {
                                                "method_name": self.save_edit_karcis
                                        },
                                        "style": self.primary_button
                                    }
                                ]

                self.CreateComponentLayout(components_setter, form_container_lay)
                karcis_content2_lay.addStretch(1)
                #######################################################

            case "tarif":
                # tarif content
                self.tarif_container = QWidget()
                self.tarif_container_lay = QVBoxLayout()
                tarif_tabs_container_widget = QWidget()
                
                tarif_tabs_container = QHBoxLayout()
                self.tarif_tab1 = QPushButton("Kelola tarif")
                self.tarif_tab2 = QPushButton("Add kendaraan-Denda")
                
                self.tarif_stack = QStackedWidget()
                self.tarif_content1 = QWidget()
                self.tarif_content2 = QWidget()
                
                # tabs
                self.setTabButton(tab1=self.tarif_tab1, tab2=self.tarif_tab2, tabsContainer=tarif_tabs_container, stackedWidget=self.tarif_stack)
                
                # set tarif layout & widget
                self.tarif_container_lay.setContentsMargins(0,0,0,0)
                self.tarif_container_lay.setSpacing(0)

                tarif_tabs_container_widget.setStyleSheet("background: #151930;")
                self.tarif_stack.setStyleSheet("background: #151930;")
                
                self.tarif_container.setLayout(self.tarif_container_lay)
                tarif_tabs_container_widget.setLayout(tarif_tabs_container)
                tarif_tabs_container.setContentsMargins(25, 20, 0, 0)

                self.tarif_container_lay.addWidget(tarif_tabs_container_widget)
                self.tarif_container_lay.addWidget(self.tarif_stack)

                # add tabs
                self.tarif_stack.addWidget(self.tarif_content1)
                self.tarif_stack.addWidget(self.tarif_content2)
                
                # set widget and layout
                self.tarif_content1_lay = QVBoxLayout()
                self.tarif_content1.setLayout( self.tarif_content1_lay )

                # set widget and layout
                self.tarif_content2_lay = QVBoxLayout()
                self.tarif_content2.setLayout( self.tarif_content2_lay )

                ############### FORM CONTAINER ##############
                res = self.createFormContainer(scrollable=True)
                self.form_container = res[0] # scrollarea widget
                # form_container.setStyleSheet("border: 2px solid red;")
                # self.tarif_content1.setMinimumWidth(700)
                # self.form_container.setMinimumWidth(700)
                self.form_tarif_container_lay = res[1] # scroll area layout
                ############################################

                # screen = self.app.primaryScreen()
                # size = screen.size()

                # tarif_content2.setMaximumHeight( size.height() - 200 )
                self.tarif_content1_lay.setContentsMargins(25,0,25,0)
                self.tarif_content2_lay.setContentsMargins(25,25,25,25)
                # tarif_content2_lay.setSpacing(0)

                self.tarif_content1_lay.addWidget(self.form_container)
                # tarif_content2.setStyleSheet("border: 2px solid blue;")

                # set widget for tab1 layout
                tab1_h_widget = QWidget()
                tab1_h_layout = QHBoxLayout()
                tab1_h_widget.setLayout(tab1_h_layout)
                self.tarif_table = QTableWidget()
                

                ###################### tarif Form ######################

                cols,res = self.exec_query("select * from tarif order by id", "cols_res")
                    
                tipe_tarif = str(res[0][cols.index('tipe_tarif')])
                toleransi = str(res[0][cols.index('toleransi')])
                rules_mtr = json.loads( str(res[0][cols.index('base_rules')]) )
                rules_mbl = json.loads( str(res[1][cols.index('base_rules')]) )
                json_keys = []                

                time_kondisi2 = "1" 
                time_kondisi3 = "1" 
                time_max = "24"

                tarif_motor_kondisi2 = "1000"
                tarif_motor_kondisi3 = "1000"
                tarif_motor_max = "5000"

                tarif_mobil_kondisi2 = "2000"
                tarif_mobil_kondisi3 = "2000"
                tarif_mobil_max = "6000"

                # extract ket-value from json
                for key in rules_mtr.keys():
                    json_keys.append( str(key) )

                time_kondisi1 = json_keys[0]
                tarif_motor_kondisi1 = rules_mtr[ json_keys[0] ]
                tarif_mobil_kondisi1 = rules_mbl[ json_keys[0] ]

                if tipe_tarif == "other":
                    time_kondisi2 = json_keys[1] 
                    time_kondisi3 = json_keys[2] 
                    time_max = json_keys[3]

                    tarif_motor_kondisi2 = rules_mtr[ json_keys[1] ]
                    tarif_motor_kondisi3 = rules_mtr[ json_keys[2] ]
                    tarif_motor_max = rules_mtr[ json_keys[3] ]

                    tarif_mobil_kondisi2 = rules_mbl[ json_keys[1] ]
                    tarif_mobil_kondisi3 = rules_mbl[ json_keys[2] ]
                    tarif_mobil_max = rules_mbl[ json_keys[3] ]


                # components
                self.tarif_form_setter = [
                                    {
                                        "name":"widget_tipe_tarif",
                                        "category":"widget",
                                        "layout": "HBoxLayout",
                                        "style":self.block_children,
                                        "max_height":50,
                                        "children":[
                                            {
                                                "name":"r_progressive",
                                                "category":"RadioButton",
                                                "text":"progresif",
                                                "checked": True if tipe_tarif == "progresif" else False, 
                                                "style":"border:none; color:#fff; font-size:12px; font-weight:500;",
                                                "toggled": {
                                                    "method_name": self.check_tarif_type
                                                }
                                            },
                                            {
                                                "name":"r_flat",
                                                "category":"RadioButton",
                                                "text":"flat",
                                                "checked": True if tipe_tarif == "flat" else False, 
                                                "style":"border:none; color:#fff; font-size:12px; font-weight:500;",
                                                "toggled": {
                                                    "method_name": self.check_tarif_type
                                                } 
                                            },
                                            {
                                                "name":"r_other",
                                                "category":"RadioButton",
                                                "text":"other",
                                                "checked": True if tipe_tarif == "other" else False, 
                                                "style":"border:none; color:#fff; font-size:12px; font-weight:500;",
                                                "toggled": {
                                                    "method_name": self.check_tarif_type
                                                }
                                            }
                                        ]
                                    },
                                    {
                                        "name":"widget_toleransi",
                                        "category":"widget",
                                        "layout": "HBoxLayout",
                                        "style":self.block_children,
                                        "max_height":50,
                                        "children":[
                                            {
                                                "name":"t_lbl1",
                                                "category":"label",
                                                "text":"Toleransi waktu ",
                                                "style":self.primary_lbl + "max-width:150px; border: none;"
                                            },
                                            {
                                                "name":"add_toleransi",
                                                "category":"spinbox",
                                                "range":(0,60),
                                                "value":toleransi,
                                                "style":self.primary_spinbox
                                            },
                                            {
                                                "name":"t_lbl2",
                                                "category":"label",
                                                "text":" menit",
                                                "style":self.primary_lbl + "border: none;"
                                            },
                                        ]
                                    },
                                    {
                                        "name":"widget_container_biaya1",
                                        "category":"widget",
                                        "layout": "VBoxLayout",
                                        "style":self.block_children,
                                        "children":[
                                            {
                                            "name":"sub_container1_biaya1",
                                            "category":"widget",
                                            "layout": "HBoxLayout",
                                            "style": "border:none;",
                                            "children":[
                                                {
                                                    "name":"lbl",
                                                    "category":"label",
                                                    "text":"Tarif: ",
                                                    "style":self.primary_lbl + "max-width:50px; border: none;"
                                                },
                                                {
                                                    "name":"add_time1",
                                                    "category":"spinbox",
                                                    "range":(0,24),
                                                    "value":time_kondisi1,
                                                    "style":self.primary_spinbox 
                                                },
                                                {
                                                    "name":"lbl",
                                                    "category":"label",
                                                    "text":" jam pertama",
                                                    "style":self.primary_lbl + "border: none;"
                                                }
                                            ]
                                            },
                                            {
                                            "name":"sub_container2_biaya1",
                                            "category":"widget",
                                            "layout": "HBoxLayout",
                                            "style": "border:none;",
                                            "children":[
                                                {
                                                    "name":"lbl",
                                                    "category":"label",
                                                    "text":"Motor(Rp) ",
                                                    "style":self.primary_lbl + "border: none;"
                                                },
                                                {
                                                    "name":"add_motor_biaya1",
                                                    "category":"lineEditInt",
                                                    "text": tarif_motor_kondisi1,
                                                    "style":self.primary_input 
                                                },
                                                {
                                                    "name":"lbl",
                                                    "category":"label",
                                                    "text":"Mobil(Rp) ",
                                                    "style":self.primary_lbl + "border: none;"
                                                },
                                                {
                                                    "name":"add_mobil_biaya1",
                                                    "category":"lineEditInt",
                                                    "text": tarif_mobil_kondisi1,
                                                    "style":self.primary_input 
                                                }
                                            ]
                                            }
                                        ]
                                    },
                                    {
                                        "name":"widget_container_biaya2",
                                        "category":"widget",
                                        "layout": "VBoxLayout",
                                        "style":self.block_children,
                                        "children":[
                                            {
                                            "name":"sub_container1_biaya2",
                                            "category":"widget",
                                            "layout": "HBoxLayout",
                                            "style": "border:none;",
                                            "children":[
                                                {
                                                    "name":"lbl",
                                                    "category":"label",
                                                    "text":"Tarif: ",
                                                    "style":self.primary_lbl + "max-width:50px; border: none;"
                                                },
                                                {
                                                    "name":"add_time2",
                                                    "category":"spinbox",
                                                    "range":(0,23),
                                                    "value":time_kondisi2,
                                                    "style":self.primary_spinbox
                                                },
                                                {
                                                    "name":"lbl",
                                                    "category":"label",
                                                    "text":" jam berikutnya",
                                                    "style":self.primary_lbl + "border: none;"
                                                }
                                            ]
                                            },
                                            {
                                            "name":"sub_container2_biaya2",
                                            "category":"widget",
                                            "layout": "HBoxLayout",
                                            "style": "border:none;",
                                            "children":[
                                                {
                                                    "name":"lbl",
                                                    "category":"label",
                                                    "text":"Motor(Rp) ",
                                                    "style":self.primary_lbl + "border: none;"
                                                },
                                                {
                                                    "name":"add_motor_biaya2",
                                                    "category":"lineEditInt",
                                                    "text": tarif_motor_kondisi2,
                                                    "style":self.primary_input 
                                                },
                                                {
                                                    "name":"lbl",
                                                    "category":"label",
                                                    "text":"Mobil(Rp) ",
                                                    "style":self.primary_lbl + "border: none;"
                                                },
                                                {
                                                    "name":"add_mobil_biaya2",
                                                    "category":"lineEditInt",
                                                    "text": tarif_mobil_kondisi2,
                                                    "style":self.primary_input 
                                                }
                                            ]
                                            }
                                        ]
                                    },
                                    {
                                        "name":"widget_container_biaya3",
                                        "category":"widget",
                                        "layout": "VBoxLayout",
                                        "style":self.block_children,
                                        "children":[
                                            {
                                            "name":"sub_container1_biaya3",
                                            "category":"widget",
                                            "layout": "HBoxLayout",
                                            "style": "border:none;",
                                            "children":[
                                                {
                                                    "name":"lbl",
                                                    "category":"label",
                                                    "text":"Tarif: ",
                                                    "style":self.primary_lbl + "max-width:50px; border: none;"
                                                },
                                                {
                                                    "name":"add_time3",
                                                    "category":"spinbox",
                                                    "range":(0,23),
                                                    "value":time_kondisi3,
                                                    "style":self.primary_spinbox
                                                },
                                                {
                                                    "name":"lbl",
                                                    "category":"label",
                                                    "text":" jam berikutnya",
                                                    "style":self.primary_lbl + "border: none;"
                                                }
                                            ]
                                            },
                                            {
                                            "name":"sub_container2_biaya3",
                                            "category":"widget",
                                            "layout": "HBoxLayout",
                                            "style": "border:none;",
                                            "children":[
                                                {
                                                    "name":"lbl",
                                                    "category":"label",
                                                    "text":"Motor(Rp) ",
                                                    "style":self.primary_lbl + "border: none;"
                                                },
                                                {
                                                    "name":"add_motor_biaya3",
                                                    "category":"lineEditInt",
                                                    "text": tarif_motor_kondisi3,
                                                    "style":self.primary_input 
                                                },
                                                {
                                                    "name":"lbl",
                                                    "category":"label",
                                                    "text":"Mobil(Rp) ",
                                                    "style":self.primary_lbl + "border: none;"
                                                },
                                                {
                                                    "name":"add_mobil_biaya3",
                                                    "category":"lineEditInt",
                                                    "text": tarif_mobil_kondisi3,
                                                    "style":self.primary_input 
                                                }
                                            ]
                                            }
                                        ]
                                    },
                                    {
                                        "name":"widget_container_biaya4",
                                        "category":"widget",
                                        "layout": "VBoxLayout",
                                        "style":self.block_children,
                                        "children":[
                                            {
                                            "name":"sub_container1_biaya4",
                                            "category":"widget",
                                            "layout": "HBoxLayout",
                                            "style": "border:none;",
                                            "children":[
                                                {
                                                    "name":"lbl",
                                                    "category":"label",
                                                    "text":"Tarif maksimal per ",
                                                    "style":self.primary_lbl + "max-width:150px; border: none;"
                                                },
                                                {
                                                    "name":"add_time4",
                                                    "category":"spinbox",
                                                    "range":(0,24),
                                                    "value":time_max,
                                                    "style":self.primary_spinbox
                                                },
                                                {
                                                    "name":"lbl",
                                                    "category":"label",
                                                    "text":" jam",
                                                    "style":self.primary_lbl + "border: none;"
                                                }
                                            ]
                                            },
                                            {
                                            "name":"sub_container2_biaya4",
                                            "category":"widget",
                                            "layout": "HBoxLayout",
                                            "style": "border:none;",
                                            "children":[
                                                {
                                                    "name":"lbl",
                                                    "category":"label",
                                                    "text":"Motor(Rp) ",
                                                    "style":self.primary_lbl + "border: none;"
                                                },
                                                {
                                                    "name":"add_motor_biaya4",
                                                    "category":"lineEditInt",
                                                    "text": tarif_motor_max,
                                                    "style":self.primary_input 
                                                },
                                                {
                                                    "name":"lbl",
                                                    "category":"label",
                                                    "text":"Mobil(Rp) ",
                                                    "style":self.primary_lbl + "border: none;"
                                                },
                                                {
                                                    "name":"add_mobil_biaya4",
                                                    "category":"lineEditInt",
                                                    "text": tarif_mobil_max,
                                                    "style":self.primary_input 
                                                }
                                            ]
                                            }
                                        ]
                                    },
                                    {
                                        "name":"btn_add_tarif",
                                        "category":"pushButton",
                                        "text": "Save",
                                        "clicked": {
                                                "method_name": self.set_tarif
                                        },
                                        "style": self.primary_button
                                    }
                                ]
                
                self.getKendaraanForm()   
                self.CreateComponentLayout(self.tarif_form_setter, self.form_tarif_container_lay)
                # tarif_content2_lay.addStretch(1)

                self.check_tarif_type( tipe_tarif )
                #######################################################



                ############# set kendaraan & denda ###################
                self.tarif_components_setter = [{
                                        "name":"main_kendaraan",
                                        "category":"widget",
                                        "layout": "VBoxLayout",
                                        "max_width":700,
                                        "style":self.block_children,
                                        "children":[]
                                    }]

                # loop component based on tarif table via method
                # return value as list
                # add new value into first and last index
                
                self.tarif_components_setter[0]["children"] = self.getKendaraanList()


                self.CreateComponentLayout(self.tarif_components_setter, self.tarif_content2_lay)
                # x = QLabel("tester")
                # y = QPushButton("tst btn")
                
                # x.setStyleSheet(self.primary_lbl + "}")
                # y.setStyleSheet(self.primary_button + "}")
                # self.tarif_content2_lay.addWidget(x)
                # self.tarif_content2_lay.addWidget(y)

                self.tarif_content2_lay.addStretch(1)
                #######################################################

            case "voucher":
                # voucher content
                self.voucher_container = QWidget()
                self.voucher_container_lay = QVBoxLayout()
                voucher_tabs_container_widget = QWidget()
                
                voucher_tabs_container = QHBoxLayout()
                self.voucher_tab1 = QPushButton("Kelola voucher")
                voucher_tab2 = QPushButton("Tambah voucher")
                
                self.voucher_stack = QStackedWidget()
                voucher_content1 = QWidget()
                voucher_content2 = QWidget()
                
                # tabs
                self.setTabButton(tab1=self.voucher_tab1, tab2=voucher_tab2, tabsContainer=voucher_tabs_container, stackedWidget=self.voucher_stack)
                
                # set voucher layout & widget
                self.voucher_container_lay.setContentsMargins(0,0,0,0)
                self.voucher_container_lay.setSpacing(0)

                voucher_tabs_container_widget.setStyleSheet("background: #151930;")
                self.voucher_stack.setStyleSheet("background: #151930;")
                
                self.voucher_container.setLayout(self.voucher_container_lay)
                voucher_tabs_container_widget.setLayout(voucher_tabs_container)
                voucher_tabs_container.setContentsMargins(25, 20, 0, 0)

                self.voucher_container_lay.addWidget(voucher_tabs_container_widget)
                self.voucher_container_lay.addWidget(self.voucher_stack)

                # add tabs
                self.voucher_stack.addWidget(voucher_content1)
                self.voucher_stack.addWidget(voucher_content2)
                
                # set widget and layout
                voucher_content1_lay = QVBoxLayout()
                voucher_content1.setLayout( voucher_content1_lay )

                # set widget and layout
                voucher_content2_lay = QVBoxLayout()
                voucher_content2.setLayout( voucher_content2_lay )

                ############### FORM CONTAINER ##############
                res = self.createFormContainer()
                form_container = res[0]
                form_container_lay = res[1]
                ############################################

                voucher_content2_lay.setContentsMargins(25,25,25,25)
                voucher_content2_lay.addWidget(form_container)

                # set widget for tab1 layout
                tab1_h_widget = QWidget()
                tab1_h_layout = QHBoxLayout()
                tab1_h_widget.setLayout(tab1_h_layout)
                self.voucher_table = QTableWidget()
                
                # action layout
                action_widget = QWidget()
                action_lay = QVBoxLayout()
                action_widget.setLayout(action_lay)
                action_widget.setMaximumWidth(120)
                action_widget.setStyleSheet("border: none;")
                action_lay.setContentsMargins(0,0,0,0)
                action_lay.setSpacing(0)

                ################# action lineedit and button ###################
                row_label = QLabel("No Baris:")
                self.row_info_voucher = QLineEdit()
                row_search = QPushButton("edit")
                row_delete = QPushButton("delete")
                row_print = QPushButton("PRINT")
                row_search.setIcon(QIcon(self.icon_path+"blog-pencil.png"))
                row_delete.setIcon(QIcon(self.icon_path+"trash.png"))
                row_print.setIcon(QIcon(self.icon_path+"print.png"))

                row_label.setStyleSheet("color:#fff; font-size:13px; font-weight: 500; background:#384F67; margin-bottom: 5px; padding:5px;")
                self.row_info_voucher.setReadOnly(True)
                self.row_info_voucher.setStyleSheet("background:#fff; padding:8px; margin-bottom: 5px; color: #000; border:none;")
                row_search.setStyleSheet(View.edit_btn_action)
                row_delete.setStyleSheet(View.del_btn_action)
                row_print.setStyleSheet(View.print_btn_action)

                # add lineedit and button into action_lay
                action_lay.addWidget(row_label)
                action_lay.addWidget(self.row_info_voucher)
                action_lay.addWidget(row_search)
                action_lay.addWidget(row_delete)
                action_lay.addWidget(row_print)
                action_lay.addStretch(1)


                ##################### action edit & delete ###################
                
                row_search.clicked.connect(lambda: self.editPopUp(form_type="voucher", form_size=(400, 600)))
                row_delete.clicked.connect(lambda: self.deleteData("voucher"))
                row_print.clicked.connect(lambda: self.printData("voucher"))

                ##############################################################


                ######################### voucher Table ##############################
                # add table and action widget into tab1_h_layout
                tab1_h_layout.addWidget(self.voucher_table)
                tab1_h_layout.addWidget(action_widget)

                # create table widget

                # fetch data from DB
                query = self.exec_query("SELECT id, id_pel, lokasi, tarif, masa_berlaku, jns_kendaraan FROM voucher", "SELECT")
                rows_count = len(query)
                cols = 6

                self.voucher_table.resizeRowsToContents()
                self.voucher_table.horizontalHeader().setStretchLastSection(True)

                self.voucher_table.setRowCount(rows_count)
                self.voucher_table.setColumnCount(cols)

                self.voucher_table.setHorizontalHeaderLabels(["id", "ID Pel", "Lokasi", "Saldo", "Masa Berlaku", "Jenis Kendaraan"])
                self.voucher_table.setStyleSheet(View.table_style)

                self.voucher_table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
                self.voucher_table.setColumnHidden(0, True) #hide id column
                
                self.fillTable(self.voucher_table, cols, query)

                # create edit & delete section
                self.voucher_table.setSelectionBehavior(QTableWidget.SelectRows)
                self.voucher_table.clicked.connect(lambda: self.getCellVal(self.voucher_table, page="voucher"))
                
                # voucher_content1_lay.addWidget(table)
                voucher_content1_lay.addWidget(tab1_h_widget)

                ###########################################################


                ###################### voucher Form ######################

                # components

                components_setter = [{
                                        "name":"lbl_add_voucher_idpel",
                                        "category":"label",
                                        "text": "ID Pelanggan",
                                        "style":self.primary_lbl
                                    },
                                    {
                                        "name":"add_voucher_idpel",
                                        "category":"lineEditInt",
                                        "style":self.primary_input
                                    },
                                    {
                                        "name":"lbl_add_voucher_lokasi",
                                        "category":"label",
                                        "text": "Lokasi",
                                        "style":self.primary_lbl + margin_top
                                    },
                                    {
                                        "name":"add_voucher_lokasi",
                                        "category":"lineEdit",
                                        "style":self.primary_input
                                    },
                                    {
                                        "name":"lbl_add_voucher_tarif",
                                        "category":"label",
                                        "text": "Tarif",
                                        "style":self.primary_lbl + margin_top
                                    },
                                    {
                                        "name":"add_voucher_tarif",
                                        "category":"lineEditInt",
                                        "style":self.primary_input
                                    },
                                    {
                                        "name":"lbl_add_voucher_masa_berlaku",
                                        "category":"label",
                                        "text": "Masa Berlaku",
                                        "style":self.primary_lbl + margin_top
                                    },
                                    {
                                        "name":"add_voucher_masa_berlaku",
                                        "category":"date",
                                        "style":self.primary_input
                                    },
                                    {
                                        "name":"lbl_add_voucher_jns_kendaraan",
                                        "category":"label",
                                        "text": "Jenis Kendaraan",
                                        "style":self.primary_lbl + margin_top
                                    },
                                    {
                                        "name":"add_voucher_jns_kendaraan",
                                        "category":"comboBox",
                                        "items":["Motor", "Mobil"],
                                        "style":self.primary_combobox
                                    },
                                    {
                                        "name":"btn_add_voucher",
                                        "category":"pushButton",
                                        "text": "Save",
                                        "clicked": {
                                                "method_name": self.add_voucher
                                        },
                                        "style": self.primary_button
                                    }
                                ]

                self.CreateComponentLayout(components_setter, form_container_lay)
                voucher_content2_lay.addStretch(1)
                #######################################################

            
            case "laporan":

                ###################### init widgets & layouts #########################
                laporan_tabs_container_widget = QWidget()
                self.laporan_container = QWidget()
                action_widget = QWidget()
                laporan_content1 = QWidget()
                tab1_h_widget = QWidget()
                self.laporan_stack = QStackedWidget()
                self.laporan_table = QTableWidget()
                tgl_container = QWidget()
                tgl_input_container = QWidget()
                lama_container_menit = QWidget()
                lama_input_menit_container = QWidget()
                lama_container_jam = QWidget()
                lama_input_jam_container = QWidget()
                jns_kendaraan_container = QWidget()
                stat_kendaraan_container = QWidget()
                jns_trans_container = QWidget()
                shift_container = QWidget()
                prev_next_cont_widget = QWidget()
                total_income_wgt = QWidget()
                
                
                filter_main_wgt, filter_main_lay = self.CreateContainer( QVBoxLayout() )
                kendaraan_container_wgt, kendaraan_container_wgt_lay = self.CreateContainer( QHBoxLayout() )

                gb_cari_lay = QVBoxLayout()
                gb_waktu_lay = QHBoxLayout()
                gb_kendaraan_lay = QHBoxLayout()
                gb_transaksi_lay = QHBoxLayout()
                laporan_tabs_container = QHBoxLayout()
                tab1_h_layout = QHBoxLayout()
                self.laporan_container_lay = QVBoxLayout() # coba scroll  disini (kalau scroll disini maka tabs juga akan ikut di scroll)
                action_lay = QVBoxLayout()
                laporan_content1_lay = QVBoxLayout() # coba scroll disini juga
                tgl_container_lay = QVBoxLayout()
                tgl_input_lay = QHBoxLayout()
                lama_container_menit_lay = QVBoxLayout()
                lama_input_menit_lay = QHBoxLayout()
                lama_container_jam_lay = QVBoxLayout()
                lama_input_jam_lay = QHBoxLayout()
                jns_kendaraan_lay = QVBoxLayout()
                stat_kendaraan_lay = QVBoxLayout()
                jns_trans_lay = QVBoxLayout()
                shift_lay = QVBoxLayout()
                prev_next_cont_lay = QHBoxLayout()
                total_income_lay = QHBoxLayout()

                screen = self.app.primaryScreen()
                size = screen.size()

                scroll = QScrollArea() 
                scroll.setWidget(laporan_content1)
                scroll.setWidgetResizable(True)
                scroll.setMaximumHeight( size.height() - 100 )

                ###################### end init widgets & layouts #########################
                
                
                ######################## components ########################
                self.laporan_tab1 = QPushButton("Kelola laporan")

                lbl_filter = QLabel("FILTER LAPORAN:")
                lbl_cari = QLabel("cari data:")
                lbl_tgl = QLabel("tanggal:")
                self.radio_btn_menit = QRadioButton("lama parkir(menit):")
                self.radio_btn_jam = QRadioButton("lama parkir(jam):")
                # lbl_lama_parkir = QLabel("lama parkir(menit):")
                lbl_jns_kendaraan = QLabel("jns kendaraan:")
                lbl_stat_kendaraan = QLabel("stat kendaraan:")
                lbl_jns_transaksi = QLabel("jns transaksi:")
                lbl_shift = QLabel("shift:")
                lbl_sd = QLabel("s/d")
                prev_btn = QPushButton("prev")
                next_btn = QPushButton("next")
                self.lbl_count = QLabel()
                self.total_income_lbl = QLabel("TOTAL INCOME: ... ")
                
                self.input_cari = QLineEdit()
                self.pilih_tgl1 = QDateEdit( calendarPopup=True )
                self.pilih_tgl2 = QDateEdit( calendarPopup=True )
                self.pilih_tgl1.setDateTime( QDateTime.currentDateTime() )
                self.pilih_tgl2.setDateTime( QDateTime.currentDateTime() )
                self.pilih_tgl1.setDisplayFormat("dd/MM/yyyy")
                self.pilih_tgl2.setDisplayFormat("dd/MM/yyyy")

                self.input_menit1 = QSpinBox()
                self.input_menit2 = QSpinBox()
                self.input_jam1 = QSpinBox()
                self.input_jam2 = QSpinBox()
                self.input_jam1.setMinimum(0)
                self.input_jam1.setMaximum(23)
                
                self.input_jam2.setMinimum(1)
                self.input_jam2.setMaximum(24)

                kendaraan = ["Mobil", "Motor", "Semua"]
                stat_parkir = ["Keluar", "Masuk", "Semua"]
                self.pilih_jns_kendaraan = QComboBox()
                self.pilih_stat_kendaraan = QComboBox()
                self.pilih_jns_kendaraan.addItems( kendaraan )
                self.pilih_stat_kendaraan.addItems( stat_parkir )
                self.pilih_jns_kendaraan.setCurrentIndex( 2 )
                self.pilih_stat_kendaraan.setCurrentIndex( 2 )

                trans = ["Casual", "Voucher", "Semua"]
                self.pilih_jns_transaksi = QComboBox()
                self.pilih_shift = QComboBox()
                self.pilih_jns_transaksi.addItems( trans )
                self.pilih_shift.addItems( ["s1", "s2", "s3", "s4", "s5", "Semua"] )
                self.pilih_jns_transaksi.setCurrentIndex(2)
                self.pilih_shift.setCurrentIndex( 5 )
                
            
                groupboxes = [
                        {
                            "name": "gb_cari",
                            "category":"GroupBox",
                            "min_width": 550,
                            "min_height": 80,
                            "style": self.filter_gb_styling
                        },
                        {
                            "name": "gb_waktu",
                            "category":"GroupBox",
                            "min_width": 550,
                            "min_height": 80,
                            "style": self.filter_gb_styling
                        },
                    ]
                
                groupboxes2 = [
                        {
                            "name": "gb_kendaraan",
                            "category":"GroupBox",
                            "min_width": 270,
                            "min_height": 80,
                            "style": self.filter_gb_styling
                        },
                        {
                            "name": "gb_transaksi",
                            "category":"GroupBox",
                            "min_width": 270,
                            "min_height": 80,
                            "style": self.filter_gb_styling
                        },
                    ]
                
                filter_main_lay.addWidget( lbl_filter )
                self.CreateComponentLayout(groupboxes, filter_main_lay)
                self.CreateComponentLayout(groupboxes2, kendaraan_container_wgt_lay)

                row_search = QPushButton("search")
                row_detail = QPushButton("details")
                row_refresh = QPushButton("refresh")
                self.row_print = QPushButton("PRINT")
                row_label = QLabel("No Baris:")
                row_label_print = QLabel("Opsi Print:")
                self.row_opsi_print = QComboBox()
                self.row_opsi_print.addItems( ["rekap/tgl", "rekap/jam", "semua"] )

                self.row_info_laporan = QLineEdit()
                

                # styling
                laporan_tabs_container_widget.setStyleSheet("background: #151930;")
                scroll.setStyleSheet("border: none;")
                self.laporan_stack.setStyleSheet("background: #151930;")
                lbl_filter.setStyleSheet( View.primary_lbl + "}" )
                lbl_cari.setStyleSheet( View.primary_lbl + "}" )
                lbl_sd.setMaximumWidth(30)
                lbl_sd.setStyleSheet( View.primary_lbl + "}" )
                lbl_tgl.setStyleSheet( View.primary_lbl + "}" )
                self.radio_btn_menit.setStyleSheet( View.primary_radio + "}" )
                self.radio_btn_jam.setStyleSheet( View.primary_radio + "}" )
                lbl_jns_kendaraan.setStyleSheet( View.primary_lbl + "}" )
                lbl_stat_kendaraan.setStyleSheet( View.primary_lbl + "}" )
                lbl_jns_transaksi.setStyleSheet( View.primary_lbl + "}" )
                lbl_shift.setStyleSheet( View.primary_lbl + " height: 25px; }" )
                self.input_cari.setStyleSheet( View.primary_input + " height: 25px; }" )
                
                self.pilih_tgl1.setStyleSheet( View.primary_date + "width: 250px; height: 25px; }" )
                self.pilih_tgl2.setStyleSheet( View.primary_date + "width: 250px; height: 25px; }" )
                
                self.pilih_jns_kendaraan.setStyleSheet( View.primary_combobox + " height: 25px; background:#fff; color: #000; }" )
                self.pilih_stat_kendaraan.setStyleSheet( View.primary_combobox + " height: 25px; background:#fff; color:#000; }" )
                self.pilih_jns_transaksi.setStyleSheet( View.primary_combobox + " height: 25px; background:#fff; color:#000; }" )
                self.pilih_shift.setStyleSheet( View.primary_combobox + " height: 25px; background:#fff; color:#000; }" )
                self.input_menit1.setStyleSheet( View.primary_spinbox + "height: 25px; }" )
                self.input_menit2.setStyleSheet( View.primary_spinbox + "height: 25px; }" )
                self.input_jam1.setStyleSheet( View.primary_spinbox + "height: 25px; }" )
                self.input_jam2.setStyleSheet( View.primary_spinbox + "height: 25px; }" )

                action_widget.setStyleSheet("border: none;")
                row_label.setStyleSheet("color:#fff; font-size:13px; font-weight: 500; background:#384F67; margin-bottom: 5px; padding:5px;")
                row_label_print.setStyleSheet("color:#fff; font-size:13px; font-weight: 500; background:#384F67; margin-top:35px; margin-bottom: 5px; padding:5px;")
                self.row_opsi_print.setStyleSheet("font-size:13px; background:#fff; margin-bottom: 5px; padding:5px;")
                self.row_info_laporan.setStyleSheet("background:#fff; padding:8px; margin-bottom: 5px; color: #000; border:none;")
                row_search.setStyleSheet(View.edit_btn_action)
                row_detail.setStyleSheet(View.detail_btn_action)
                self.row_print.setStyleSheet(View.del_btn_action + "QPushButton{ background:#951C3C; padding: 5px; }")
                row_refresh.setStyleSheet(View.print_btn_action)

                prev_next_cont_lay.setAlignment( Qt.AlignCenter )
                prev_btn.setIcon(QIcon(self.icon_path+"angle-left.png"))
                next_btn.setIcon(QIcon(self.icon_path+"angle-right.png"))
                prev_btn.setStyleSheet( View.prev_btn + "QPushButton{ background:#40407a; padding: 8px;}" )
                next_btn.setStyleSheet( View.next_btn + "QPushButton{ background:#40407a; padding: 8px;}" )
                self.lbl_count.setAlignment( Qt.AlignCenter )
                self.lbl_count.setStyleSheet( View.primary_lbl + "}" )
                next_btn.setLayoutDirection(Qt.RightToLeft)
                self.total_income_lbl.setAlignment( Qt.AlignLeft )
                self.total_income_lbl.setStyleSheet( View.primary_lbl + " padding-top:10px; font-size: 16px; color:#fa0; }" )

                # positioning
                laporan_tabs_container.setContentsMargins(25, 20, 0, 0)
                self.laporan_container_lay.setContentsMargins(0,0,0,0)
                action_lay.setContentsMargins(0,0,0,0)
                filter_main_lay.setContentsMargins(10,35,10,35)
                gb_waktu_lay.setContentsMargins(0,0,0,0)
                kendaraan_container_wgt_lay.setContentsMargins(0,0,0,0)
                prev_next_cont_lay.setContentsMargins(0,15,0,0)
                
                # spacing & strech
                self.laporan_container_lay.setSpacing(0)
                action_lay.setSpacing(0)

                # sizing
                action_widget.setMaximumWidth(120)
                prev_btn.setMaximumWidth(100)
                next_btn.setMaximumWidth(100)
                self.lbl_count.setMinimumWidth(200)
                
                # set layout
                laporan_tabs_container_widget.setLayout(laporan_tabs_container)
                self.laporan_container.setLayout(self.laporan_container_lay)
                action_widget.setLayout(action_lay)
                laporan_content1.setLayout( laporan_content1_lay )
                self.components["gb_cari"].setLayout(gb_cari_lay)
                self.components["gb_waktu"].setLayout(gb_waktu_lay)
                self.components["gb_kendaraan"].setLayout(gb_kendaraan_lay)
                self.components["gb_transaksi"].setLayout(gb_transaksi_lay)
                tgl_container.setLayout( tgl_container_lay )
                tgl_input_container.setLayout( tgl_input_lay )
                tab1_h_widget.setLayout(tab1_h_layout)
                lama_container_menit.setLayout( lama_container_menit_lay )
                lama_input_menit_container.setLayout( lama_input_menit_lay )
                lama_container_jam.setLayout( lama_container_jam_lay )
                lama_input_jam_container.setLayout( lama_input_jam_lay )
                jns_kendaraan_container.setLayout( jns_kendaraan_lay )
                stat_kendaraan_container.setLayout( stat_kendaraan_lay )
                jns_trans_container.setLayout( jns_trans_lay )
                shift_container.setLayout( shift_lay )
                prev_next_cont_widget.setLayout( prev_next_cont_lay )
                total_income_wgt.setLayout( total_income_lay )


                # add widget
                self.laporan_container_lay.addWidget(laporan_tabs_container_widget)

                gb_cari_lay.addWidget( lbl_cari )
                gb_cari_lay.addWidget( self.input_cari )
                filter_main_lay.addWidget( kendaraan_container_wgt )

                action_lay.addWidget(row_label)
                action_lay.addWidget(self.row_info_laporan)
                action_lay.addWidget(row_search)
                action_lay.addWidget(row_detail)
                action_lay.addWidget(row_label_print)
                action_lay.addWidget(self.row_opsi_print)
                action_lay.addWidget(self.row_print)
                action_lay.addWidget(row_refresh)
                action_lay.addStretch(1)

                tab1_h_layout.addWidget(self.laporan_table)
                tab1_h_layout.addWidget(action_widget)
                self.laporan_stack.addWidget(scroll)
                self.laporan_container_lay.addWidget(self.laporan_stack)
                gb_waktu_lay.addWidget( tgl_container )
                gb_waktu_lay.addWidget( lama_container_menit )
                gb_waktu_lay.addWidget( lama_container_jam )
                tgl_container_lay.addWidget( lbl_tgl )
                tgl_container_lay.addWidget( tgl_input_container )
                tgl_input_lay.addWidget( self.pilih_tgl1 )
                tgl_input_lay.addWidget( lbl_sd )
                tgl_input_lay.addWidget( self.pilih_tgl2 )

                lama_container_menit_lay.addWidget( self.radio_btn_menit )
                lama_container_menit_lay.addWidget( lama_input_menit_container )
                lama_container_jam_lay.addWidget( self.radio_btn_jam )
                lama_container_jam_lay.addWidget( lama_input_jam_container )
                
                lama_input_menit_lay.addWidget( self.input_menit1 )
                lama_input_menit_lay.addWidget( lbl_sd )
                lama_input_menit_lay.addWidget( self.input_menit2 )
                
                lama_input_jam_lay.addWidget( self.input_jam1 )
                lama_input_jam_lay.addWidget( lbl_sd )
                lama_input_jam_lay.addWidget( self.input_jam2 )
                
                gb_kendaraan_lay.addWidget( jns_kendaraan_container )
                gb_kendaraan_lay.addWidget( stat_kendaraan_container )
                jns_kendaraan_lay.addWidget( lbl_jns_kendaraan )
                jns_kendaraan_lay.addWidget( self.pilih_jns_kendaraan )
                stat_kendaraan_lay.addWidget( lbl_stat_kendaraan )
                stat_kendaraan_lay.addWidget( self.pilih_stat_kendaraan )
                gb_transaksi_lay.addWidget( jns_trans_container )
                gb_transaksi_lay.addWidget( shift_container )
                jns_trans_lay.addWidget( lbl_jns_transaksi )
                jns_trans_lay.addWidget( self.pilih_jns_transaksi )
                shift_lay.addWidget( lbl_shift )
                shift_lay.addWidget( self.pilih_shift )
                prev_next_cont_lay.addWidget( prev_btn )
                prev_next_cont_lay.addWidget( self.lbl_count )
                prev_next_cont_lay.addWidget( next_btn )
                total_income_lay.addWidget( self.total_income_lbl )

                # other
                row_search.setIcon(QIcon(self.icon_path+"search.png"))
                row_detail.setIcon(QIcon(self.icon_path+"layout-fluid.png"))
                row_refresh.setIcon(QIcon(self.icon_path+"refresh.png"))
                self.row_print.setIcon(QIcon(self.icon_path+"print.png"))
                self.row_print.setIconSize(QSize(40,40))

                row_search.clicked.connect( self.searchKarcis )
                self.row_print.clicked.connect( self.printLaporan )
                self.row_print.setEnabled(False)
                row_refresh.clicked.connect( self.refreshKarcis )
                row_detail.clicked.connect(lambda: self.detailPopUp(form_type="karcis", form_size=(400, 600)))

                self.row_info_laporan.setReadOnly(True)
                self.setTabButton(tab1=self.laporan_tab1, tab2=None, tabsContainer=laporan_tabs_container, stackedWidget=self.laporan_stack)
                self.radio_btn_menit.clicked.connect(self.radioFilterMenit)
                self.radio_btn_jam.clicked.connect(self.radioFilterJam)
                # self.radio_btn_jam.setAutoExclusive(True)
                # self.radio_btn_jam.setAutoExclusive(True)
                
                prev_btn.clicked.connect(lambda: self.prevNext("prev"))
                next_btn.clicked.connect(lambda: self.prevNext("next"))

                

                # create table widget
                # fetch data from DB
                q_income = self.exec_query("select SUM(tarif) as tot_income from karcis", "select")
                self.karcis_rows = self.exec_query("select count(*) as count from karcis", "select")
                self.row_limit = 18 if self.karcis_rows[0][0] >= 18 else self.karcis_rows[0][0]
                self.row_offset = 0
                query = self.exec_query(f"SELECT id, barcode,  nopol, jenis_kendaraan, gate, cast(datetime as date), cast(date_keluar as date), lama_parkir, status_parkir, tarif, jns_transaksi, kd_shift FROM karcis order by id limit {self.row_limit} OFFSET {self.row_offset}", "SELECT")
                rows_count = len(query)
                cols = 12

                self.laporan_table.resizeRowsToContents()
                self.laporan_table.horizontalHeader().setStretchLastSection(True)
                self.laporan_table.setRowCount( rows_count )
                self.laporan_table.setColumnCount( cols )
                self.laporan_table.setHorizontalHeaderLabels(["id", "No trans" ,"Nopol", "J.kendaraan", "Pos", "Tgl masuk", "Tgl keluar", "Lama Parkir", "Status parkir", "Biaya", "J.transaksi", "Shift"])
                self.laporan_table.setStyleSheet(View.table_style)

                self.laporan_table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
                self.laporan_table.setColumnHidden(0, True) #hide id column
                
                self.fillTableKarcis(self.laporan_table, cols, query, index_tgl_masuk=5, index_tgl_keluar=6)

                
                self.lbl_count.setText(f"1-{self.row_limit} from {self.karcis_rows[0][0]} results")

                self.total_income_lbl.setText("TOTAL INCOME: Rp " +  "{:,}".format( q_income[0][0] ).replace(",", ".") )
                # self.laporan_table.setItem(0, 0, QTableWidgetItem( "ID 1" )) # will be hidden id to edit & delete
                # self.laporan_table.setItem(0, 1, QTableWidgetItem( "test 2" ))
                # self.laporan_table.setItem(0, 2, QTableWidgetItem( "test 3" ))
                
                # self.laporan_table.setItem(1, 0, QTableWidgetItem( "ID 4" )) # will be hidden id to edit & delete
                # self.laporan_table.setItem(1, 1, QTableWidgetItem( "test 5" ))
                # self.laporan_table.setItem(1, 2, QTableWidgetItem( "test 6" ))

                # create edit & delete section
                self.laporan_table.setSelectionBehavior(QTableWidget.SelectRows)
                self.laporan_table.clicked.connect(lambda: self.getCellVal(self.laporan_table, page="laporan"))
                # btn.clicked.connect(lambda *args, row=rows: self.editData(row, table, "laporan"))

                # laporan_content1_lay.addWidget(table)
                laporan_content1_lay.addWidget( filter_main_wgt )
                laporan_content1_lay.addWidget(tab1_h_widget)
                laporan_content1_lay.addWidget(prev_next_cont_widget)
                laporan_content1_lay.addWidget(total_income_wgt)

                # print("css ==>: ", self.pilih_tgl1.styleSheet())
            case default:
                pass    

    def Login(self):
        # 2. create window based on defined size
        window_setter = {
            "title":"Login", 
            "size":(400,300),
            "style":"background-color: #fff; color:#000;"
        }
        
        
        # 3. create components
        component_setter = [
                    {
                        "name":"label_1",
                        "category":"label",
                        "text": "Username",
                        "move":(30,30),
                        "font":self.helvetica_13
                    },
                    {
                        "name":"input_uname",
                        "category":"lineEdit",
                        "min_width":320,
                        "move":(30,55),
                        "style": "border:1px solid #ecf0f1;" + self.bg_grey,
                        "font":self.helvetica_12
                    },
                    {
                        "name":"label_2",
                        "category":"label",
                        "text": "Password",
                        "move":(30,115),
                        "font":self.helvetica_13
                    },
                    {
                        "name":"input_pass",
                        "category":"lineEditPassword",
                        "min_width":320,
                        "move":(30,140),
                        "style": "border:1px solid #ecf0f1;" + self.bg_grey,
                        "font":self.helvetica_12,
                        "event": {
                            "method_name": self.login_ctrl, 
                            "arguments": (self.window,self)
                        }
                    },
                    {
                        "name":"btn_login",
                        "category":"pushButton",
                        "text": "LOGIN",
                        "min_width": 320,
                        "min_height": 45,
                        "move":(30,190),
                        "style": self.login_button,
                        "font":self.helvetica_13,
                        "clicked": {
                            "method_name": self.login_ctrl, 
                            "arguments": (self.window,self) # pelajari lagi cara kerja kode disamping
                        },
                    },
                ]

        self.CreateWindow( window_setter, self.window ) 
        self.CreateComponent(component_setter, self.window)
       
        self.window.show()

        if not self.app_stat:
            self.app_stat = True
            sys.exit(self.app.exec_())
   
    def KasirDashboard(self):

        ####### get ipcam ip ########
        ini = self.getPath(fileName="app.ini")
            
        configur = ConfigParser()
        configur.read(ini)

        ipcam1 = configur["gate1"]["ipcam1"]
        ipcam2 = configur["gate1"]["ipcam2"]
        ##############################

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


        class playCam1(QThread):
            
            cp = pyqtSignal(QImage)
            def run(self):
                debug = Debug()
                
                debug.logger.info("Run Cam Thread 1 ...")

                self.is_running = True
                self.capture = None
                
                while self.is_running:
                    try:

                        if not self.capture:
                            rtsp = ipcam1        
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
                            self.cp.emit(p)
                    
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

            def stop(self):
                self.terminate()
                # self.quit()
                self.wait()

        class playCam2(QThread):
            
            cp2 = pyqtSignal(QImage)
            def run(self):
                debug = Debug()
                
                debug.logger.info("Run Cam Thread 2 ...")

                self.is_running = True
                self.capture = None
                
                while self.is_running:
                    try:

                        if not self.capture:
                            rtsp = ipcam2        
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
                            self.cp2.emit(p)
                    
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

            def stop(self):
                self.terminate()
                # self.quit()
                self.wait()


        window_setter = {
            "title":"Kasir Dashboard", 
            "style":self.win_dashboard
        }

        # create window
        self.CreateWindow(window_setter, self.window)
        self.window.setWindowFlags(Qt.FramelessWindowHint)

        ################# create windows layout ###############
        # header
        header_img = QLabel()
        header_img.setPixmap(QPixmap('header_placeholder.png'))
        header_img.setAlignment(Qt.AlignCenter)
        # header_img.setMaximumWidth(1024)
        header_img.setMaximumHeight(80)
        
        header_container = QWidget()
        header_container_lay = QHBoxLayout()
        header_container.setLayout( header_container_lay )

        # content
        content_container = QWidget()
        content_container_lay = QHBoxLayout()
        content_container.setLayout( content_container_lay )

        # footer
        footer_container = QWidget()
        footer_container_lay = QHBoxLayout()
        footer_container.setLayout( footer_container_lay )

        # add all container to main windows
        main_layout = self.CreateLayout(("VBoxLayout", False), self.window)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        
        main_layout.addWidget(header_img)
        main_layout.addWidget(header_container)
        main_layout.addWidget(content_container)
        main_layout.addWidget(footer_container)
        
        #######################################################

        ################# fill all container ###############
        # get username login
        uname = self.components["input_uname"].text().upper()
        lbl1 = QLabel("KASIR LOGIN: " + uname)
        date_lbl = QLabel("DATE: ...")
        self.time_lbl = QLabel("TIME: ...")
        
        logout = QPushButton("LOGOUT")
        logout.setStyleSheet(View.logout_button)
        logout.setMaximumWidth(120)
        logout.setMaximumHeight(50)

        logout.clicked.connect( self.kasirLogout )

        ##### content #####
        groupboxes = [
                {
                    "name": "gb_left",
                    "category":"GroupBox",
                    "title":"Status",
                    "max_width": 440,
                    "max_height": 600,
                    "style": self.gb_styling
                },
                {
                    "name": "gb_center",
                    "category":"GroupBox",
                    "title": "Transaksi",
                    "max_width": 440,
                    "max_height": 600,
                    "style": self.gb_styling
                },
                {
                    "name": "gb_right",
                    "category":"GroupBox",
                    "title":"IP Cam",
                    "max_width": 440,
                    "max_height": 600,
                    "style": self.gb_styling
                }
            ]
        
        self.CreateComponentLayout(groupboxes, content_container_lay)
        
        # create layout for Groupbox
        left_vbox = self.CreateLayout(("VBoxLayout", False))
        right_vbox = self.CreateLayout(("VBoxLayout", False))
        center_vbox = self.CreateLayout(("VBoxLayout", False))

        # set gb layout
        self.components["gb_left"].setLayout(left_vbox)
        self.components["gb_right"].setLayout(right_vbox)
        self.components["gb_center"].setLayout(center_vbox)

        left_content = [
                    {
                        "name":"lbl_stat_koneksi",
                        "text":"STAT:",
                        "category":"label",
                        "style":self.primary_lbl
                    },
                    {
                        "name":"lbl_stat",
                        "text":"CONNECTED",
                        "category":"label",
                        "style":self.primary_lbl + "background: #00b894; padding:5px; color: #fff;"
                    },
                    {
                        "name":"lbl_ket_shift",
                        "text":"SHIFT:",
                        "category":"label",
                        "style":self.primary_lbl + "margin-top: 25px;"
                    },
                    {
                        "name":"lbl_stat",
                        "text":"shift ... ",
                        "category":"label",
                        "style":self.primary_lbl + "background: #0984e3; padding:5px; color: #fff;"
                    },
                    {
                        "name":"lbl_ket_pos",
                        "text":"POS:",
                        "category":"label",
                        "style":self.primary_lbl + "margin-top: 25px;"
                    },
                    {
                        "name":"lbl_pos",
                        "text":"PK1",
                        "category":"label",
                        "style":self.primary_lbl + "background: #0984e3; padding:5px; color: #fff;"
                    },
                    
                ]
    
        center_content = [
                    {
                        "name":"lbl_barcode_transaksi",
                        "text":"Barcode/Voucher:",
                        "category":"label",
                        "style":self.primary_lbl
                    },
                    {
                        "name":"barcode_transaksi",
                        "category":"lineEdit",
                        "style": self.primary_input + "font-weight: 600;",
                        "event": {
                            "method_name": self.getPrice
                        }
                    },
                    {
                        "name":"lbl_jns_kendaraan",
                        "text":"Jenis Kendaraan:",
                        "category":"label",
                        "style":self.primary_lbl + "margin-top:15px;"
                    },
                    {
                        "name":"jns_kendaraan",
                        "category":"lineEdit",
                        "editable":False,
                        "style": self.primary_input + "font-weight: 600;"
                    },
                    {
                        "name":"lbl_status",
                        "text":"Status:",
                        "category":"label",
                        "style":self.primary_lbl + "margin-top:15px;"
                    },
                    {
                        "name":"ket_status",
                        "category":"lineEdit",
                        "editable":False,
                        "style": self.primary_input + "font-weight: 600;"
                    },
                    {
                        "name":"lbl_tarif_transaksi",
                        "text":"Tarif(Rp):",
                        "category":"label",
                        "style":self.primary_lbl + "margin-top:15px;"
                    },
                    {
                        "name":"tarif_transaksi",
                        "category":"lineEdit",
                        "editable": False,
                        "style": self.primary_input + "height: 45px; font-weight: 600; font-size:23px; background:#ffeaa7;",
                    },
                    
                ]
    
        # center_content = [
        #         {
        #                 "name":"lbl_barcode_bermasalah",
        #                 "text":"BL/Barcode",
        #                 "category":"label",
        #                 "style":self.primary_lbl
        #             },
        #             {
        #                 "name":"barcode_bermasalah",
        #                 "category":"lineEdit",
        #                 "style": self.primary_input
        #             },
        #             # {
        #             #     "name":"lbl_tarif_bermasalah",
        #             #     "text":"Tarif(Rp)",
        #             #     "category":"label",
        #             #     "style":self.primary_lbl + "margin-top:15px;"
        #             # },
        #             # {
        #             #     "name":"tarif_bermasalah",
        #             #     "category":"lineEdit",
        #             #     "min_height": 40,
        #             #     "editable": False,
        #             #     "style":self.primary_input
        #             # },
        #             {
        #                 "name":"lbl_ket_bermasalah",
        #                 "text":"Keterangan",
        #                 "category":"label",
        #                 "style":self.primary_lbl + "margin-top:15px;"
        #             },
        #             {
        #                 "name":"ket_bermasalah",
        #                 "category":"lineEdit",
        #                 "min_height": 40,
        #                 "style": "border:1px solid #ecf0f1;"+self.bg_grey,
        #                 "font":self.helvetica_12
        #             },
        #             # {
        #             #     "name":"btn_simpan_bermasalah",
        #             #     "category":"pushButton",
        #             #     "text": "Simpan",
        #             #     "style": self.primary_button
        #             # }
        # ]

        # add components to left
        left_vbox.addStretch(1)
        self.CreateComponentLayout(left_content, left_vbox)
        
        left_vbox.setContentsMargins(8,40,8,0)
        left_vbox.addStretch(1)

        # add components to center
        center_vbox.addStretch(1)
        self.CreateComponentLayout(center_content, center_vbox)
        center_vbox.addStretch(1)
        
        # add components to right
        # self.CreateComponentLayout(right_content, right_vbox)
        ipcam_lbl1 = QLabel("CAM 1")
        self.image_label = QLabel()
        self.image_label.setMaximumSize(380, 200) # 4:3
        self.image_label.setAlignment(Qt.AlignCenter)

        ipcam_lbl2 = QLabel("CAM 2")
        self.image_label2 = QLabel()
        self.image_label2.setMaximumSize(380, 200) # 4:3
        self.image_label2.setAlignment(Qt.AlignCenter)

        # self.stream_url_1 = 'rtsp://admin:admin@192.168.100.121'
        # self.stream_url_2 = 'http://192.168.100.69:4747/video'


        self.th = playCam1(parent=self.window)
        # self.th = playCam1()
        self.th.cp.connect(self.setImageKasir) 
        self.th.start()
        
        self.th2 = playCam2(parent=self.window)
        # self.th2 = playCam2()
        self.th2.cp2.connect(self.setImageKasir2) 
        self.th2.start()

       

        # self.cap_1 = cv2.VideoCapture(self.stream_url_1)
        # self.cap_2 = cv2.VideoCapture(self.stream_url_2)

        # self.timer = QTimer()
        # self.timer.timeout.connect(self.play)
        # self.timer.start(30)



        right_vbox.addWidget(ipcam_lbl1)
        right_vbox.addWidget(self.image_label)
        
        right_vbox.addWidget(ipcam_lbl2)
        right_vbox.addWidget(self.image_label2)
        
        # right_vbox.addStretch(1)
        ###################

        footer_lbl = QLabel()
        footer_lbl.setPixmap(QPixmap('footer_placeholder.png'))
        # footer_lbl.setMaximumWidth(1020)
        footer_lbl.setMaximumHeight(40)
        footer_lbl.setAlignment( Qt.AlignCenter )

        lbl1.setStyleSheet("background: #fade72; color: #222f3e; font-weight:600; padding: 5px;")
        date_lbl.setStyleSheet("background: #f8d343; color: #222f3e; font-weight:600; padding: 5px;")
        self.time_lbl.setStyleSheet("background: #f7c815; color: #222f3e; font-weight:600; padding: 5px;")
        # lbl3.setStyleSheet("color: #fff;")

        ###### set date & time value

        # Get & set current date
        current_date = QDate.currentDate().toString('MM/dd/yyyy')
        date_lbl.setText("TANGGAL: " + current_date)

        # get & set time
        timer = QTimer(self.window)
        timer.timeout.connect(self.updateTime)
        timer.start(1000) 

        header_container_lay.setSpacing(0)
        header_container_lay.addWidget(lbl1)
        header_container_lay.addWidget(date_lbl)
        header_container_lay.addWidget(self.time_lbl)
        header_container_lay.addWidget(logout)
        
        footer_container_lay.addWidget(footer_lbl)
        
        #######################################################
        
        ################# create shortcut key #################
        # transaksi
        self.keyShortcut(keyCombination="Ctrl+t", targetWidget=self.components["barcode_transaksi"])
        
        # search voucher
        self.keyShortcut(keyCombination="Ctrl+f", command="search-voucher")
        
        # btn bayar
        self.keyShortcut(keyCombination="Ctrl+b", command="pay")
        
        # lap user bermasalah
        # self.keyShortcut(keyCombination="Ctrl+l", targetWidget=self.components["barcode_bermasalah"])
        self.keyShortcut(keyCombination="Ctrl+l", command="popup-user-bermasalah")
        
        # save btn - lap user bermasalah
        self.keyShortcut(keyCombination="Ctrl+s", command="save")
        
        # open gate keluar
        self.keyShortcut(keyCombination="Ctrl+o", command="open-gate")
        
        #######################################################

        self.window.setCentralWidget(main_widget)
        self.window.show()

    def updateTime(self):
        # Get current time
        current_time = QTime.currentTime().toString('hh:mm:ss')

        # Update digital clock label
        self.time_lbl.setText("JAM: "+ current_time)
    
    def kasirLogout(self):
        self.th.stop()
        self.th2.stop()    
        # print("==> thread: ", self.th, type(self.th))

        self.closeWindow(self.window)
        # self.window = QMainWindow()
       
        # window_setter = {
        #     "title":"Kasir Dashboard", 
        #     "style":self.win_dashboard
        # }

        # # create window
        # self.CreateWindow(window_setter, self.window)

        # self.window.show()
       
        self.Login()
        
    def setImageKasir(self, image):
        try:
            self.image_label.setPixmap(QPixmap.fromImage(image))
            
        except Exception as e:
            self.debug.logger.info("Something wrong with set image frame to QLabel ...")
            self.debug.logger.error(str(e))
    
    def setImageKasir2(self, image):
        try:
            self.image_label2.setPixmap(QPixmap.fromImage(image))
            
        except Exception as e:
            self.debug.logger.info("Something wrong with set image frame to QLabel ...")
            self.debug.logger.error(str(e))
       


    def AdminDashboard(self):
            window_setter = {
                "title":"Admin Dashboard", 
                "style":self.win_dashboard
            }
            
            # Get path
            path = os.path.dirname(os.path.realpath(__file__))
            os_name = os.name

            if os_name == 'posix':
                self.icon_path = '/icons'.join([path, "/"])
            elif os_name == 'nt':
                self.icon_path = '\icons'.join([path, "\\"])

            # create window
            self.CreateWindow(window_setter, self.window)
            self.window.setWindowFlags(Qt.FramelessWindowHint)

            # create main layouts
            main_win_layout = self.CreateLayout(("VBoxLayout", False))
            main_win_layout.setContentsMargins(0, 0, 0, 0)
            main_win_layout.setSpacing(0)
            
            # create and set widget for layout
            main_win_widget = QWidget()
            main_win_widget.setLayout(main_win_layout)


            ###################### top layout ###################
            self.top_lay_widget = QWidget()
            self.top_lay = QHBoxLayout()
            
            self.top_lay.setContentsMargins(0, 0, 0, 0)
            self.top_lay.setSpacing(0)
            self.top_lay_widget.setStyleSheet("background: #363A3E;")
            self.top_lay_widget.setLayout(self.top_lay)

            # burger menu
            self.burger_menu = QPushButton()
            self.burger_menu.setIcon(QIcon(self.icon_path+"menu-burger.png"))
            self.burger_menu.setFixedSize(30, 30)
            self.burger_menu.setStyleSheet("background-color: #1d262d;")
            self.burger_menu.clicked.connect(lambda: self.toggleMenu(250, True, self.icon_path))
            self.top_lay.addWidget(self.burger_menu)
            
            # top label
            dashboard_lbl = QLabel()
            dashboard_lbl.setText("Admin Dashboard")
            dashboard_lbl.setFont( self.fontStyle("Helvetica", 11, 500) )
            dashboard_lbl.setStyleSheet("background:#363A3E; color: #FFF; margin-left:10px; padding-top:8px; padding-bottom:8px;")
            dashboard_lbl.setAlignment(Qt.AlignCenter)
            self.top_lay.addWidget(dashboard_lbl)
            #############################################


            # add top component to main layout
            main_win_layout.addWidget(self.top_lay_widget)

            # set layout & widget for bottom component
            horizontal_lay = QHBoxLayout()
            horizontal_widget = QFrame()
            self.left_widget = QFrame()
            right_widget = QFrame()
            left_menu_lay =  QVBoxLayout()
            self.right_content_lay =  QVBoxLayout()
            self.stacked_widget = QStackedWidget()
            
            left_menu_lay.setContentsMargins(0, 0, 0, 0)
            left_menu_lay.setSpacing(0)
            
            self.right_content_lay.setContentsMargins(0, 0, 0, 0)
            self.right_content_lay.setSpacing(0)
            self.right_content_lay.addWidget(self.stacked_widget)
            
            self.left_widget.setMaximumSize(30, 2000)
            self.left_widget.setLayout(left_menu_lay)
            right_widget.setLayout(self.right_content_lay)

            horizontal_lay.setContentsMargins(0, 0, 0, 0)
            horizontal_lay.setSpacing(0)
            horizontal_lay.addWidget(self.left_widget)
            horizontal_lay.addWidget(right_widget)

            horizontal_widget.setLayout(horizontal_lay)
            horizontal_widget.setStyleSheet("background-color:#2c3e50;")

            main_win_layout.addWidget(horizontal_widget)

            ################ Home #################
            self.home_btn =QPushButton()
            self.home_btn.setFixedSize(30,30)
            self.home_btn.setIcon( QIcon(self.icon_path+"home.png") )
            self.home_btn.setStyleSheet(View.left_menu_btn)
            self.home_lbl = ClickableLabel("Home")
            self.home_lbl.setFont( self.fontStyle("Helvetica", 10, 500) )
            self.home_lbl.setStyleSheet(View.left_menu_lbl)

            left_menu_horizontal = QHBoxLayout()
            left_menu_horizontal.addWidget(self.home_btn)
            left_menu_horizontal.addWidget(self.home_lbl)
            left_menu_lay.addLayout(left_menu_horizontal)

            self.setMenuClicked(button=self.home_btn, label=self.home_lbl, page="dashboard")
            ###########################################
            
            
            ################ RFID #################
            self.rfid_btn =QPushButton()
            self.rfid_btn.setFixedSize(30,30)
            self.rfid_btn.setIcon( QIcon(self.icon_path+"share.png") )
            self.rfid_btn.setStyleSheet(View.left_menu_btn)
            self.rfid_lbl = ClickableLabel("RFID")
            self.rfid_lbl.setFont( self.fontStyle("Helvetica", 10, 500) )
            self.rfid_lbl.setStyleSheet(View.left_menu_lbl)

            left_menu_horizontal = QHBoxLayout()
            left_menu_horizontal.addWidget(self.rfid_btn)
            left_menu_horizontal.addWidget(self.rfid_lbl)
            left_menu_lay.addLayout(left_menu_horizontal)
            
            self.setMenuClicked(button=self.rfid_btn, label=self.rfid_lbl, page="kelola rfid")
            # self.rfid_btn.clicked.connect(lambda: self.windowBarAction("kelola rfid"))
            # self.rfid_lbl.clicked.connect(lambda: self.windowBarAction("kelola rfid"))
            ###########################################
            
            
            ################ Users #################
            self.users_btn =QPushButton()
            self.users_btn.setFixedSize(30,30)
            self.users_btn.setIcon( QIcon(self.icon_path+"users.png") )
            self.users_btn.setStyleSheet(View.left_menu_btn)
            self.users_lbl = ClickableLabel("Users")
            self.users_lbl.setFont( self.fontStyle("Helvetica", 10, 500) )
            self.users_lbl.setStyleSheet(View.left_menu_lbl)

            left_menu_horizontal = QHBoxLayout()
            left_menu_horizontal.addWidget(self.users_btn)
            left_menu_horizontal.addWidget(self.users_lbl)
            left_menu_lay.addLayout(left_menu_horizontal)

            self.setMenuClicked(button=self.users_btn, label=self.users_lbl, page="kelola user")
            ###########################################
            
            
            ################ Cashier #################
            self.kasir_btn =QPushButton()
            self.kasir_btn.setFixedSize(30,30)
            self.kasir_btn.setIcon( QIcon(self.icon_path+"computer.png") )
            self.kasir_btn.setStyleSheet(View.left_menu_btn)
            self.kasir_lbl = ClickableLabel("Kasir")
            self.kasir_lbl.setFont( self.fontStyle("Helvetica", 10, 500) )
            self.kasir_lbl.setStyleSheet(View.left_menu_lbl)

            left_menu_horizontal = QHBoxLayout()
            left_menu_horizontal.addWidget(self.kasir_btn)
            left_menu_horizontal.addWidget(self.kasir_lbl)
            left_menu_lay.addLayout(left_menu_horizontal)

            self.setMenuClicked(button=self.kasir_btn, label=self.kasir_lbl, page="kelola kasir")
            ###########################################
            
            
            ################ Karcis #################
            self.karcis_btn =QPushButton()
            self.karcis_btn.setFixedSize(30,30)
            self.karcis_btn.setIcon( QIcon(self.icon_path+"receipt.png") )
            self.karcis_btn.setStyleSheet(View.left_menu_btn)
            self.karcis_lbl = ClickableLabel("karcis")
            self.karcis_lbl.setFont( self.fontStyle("Helvetica", 10, 500) )
            self.karcis_lbl.setStyleSheet(View.left_menu_lbl)

            left_menu_horizontal = QHBoxLayout()
            left_menu_horizontal.addWidget(self.karcis_btn)
            left_menu_horizontal.addWidget(self.karcis_lbl)
            left_menu_lay.addLayout(left_menu_horizontal)

            self.setMenuClicked(button=self.karcis_btn, label=self.karcis_lbl, page="setting karcis")
            ###########################################


            ################ Tarif #################
            self.tarif_btn =QPushButton()
            self.tarif_btn.setFixedSize(30,30)
            self.tarif_btn.setIcon( QIcon(self.icon_path+"usd-circle.png") )
            self.tarif_btn.setStyleSheet(View.left_menu_btn)
            self.tarif_lbl = ClickableLabel("Tarif")
            self.tarif_lbl.setFont( self.fontStyle("Helvetica", 10, 500) )
            self.tarif_lbl.setStyleSheet(View.left_menu_lbl)

            left_menu_horizontal = QHBoxLayout()
            left_menu_horizontal.addWidget(self.tarif_btn)
            left_menu_horizontal.addWidget(self.tarif_lbl)
            left_menu_lay.addLayout(left_menu_horizontal)

            self.setMenuClicked(button=self.tarif_btn, label=self.tarif_lbl, page="kelola tarif")
            ###########################################
            
            
            ################ Voucher #################
            self.voucher_btn =QPushButton()
            self.voucher_btn.setFixedSize(30,30)
            self.voucher_btn.setIcon( QIcon(self.icon_path+"ticket.png") )
            self.voucher_btn.setStyleSheet(View.left_menu_btn)
            self.voucher_lbl = ClickableLabel("Voucher")
            self.voucher_lbl.setFont( self.fontStyle("Helvetica", 10, 500) )
            self.voucher_lbl.setStyleSheet(View.left_menu_lbl)

            left_menu_horizontal = QHBoxLayout()
            left_menu_horizontal.addWidget(self.voucher_btn)
            left_menu_horizontal.addWidget(self.voucher_lbl)
            left_menu_lay.addLayout(left_menu_horizontal)

            self.setMenuClicked(button=self.voucher_btn, label=self.voucher_lbl, page="kelola voucher")
            ###########################################
            
            
            ################ Laporan #################
            self.laporan_btn =QPushButton()
            self.laporan_btn.setFixedSize(30,30)
            self.laporan_btn.setIcon( QIcon(self.icon_path+"document-signed.png") )
            self.laporan_btn.setStyleSheet(View.left_menu_btn)
            self.laporan_lbl = ClickableLabel("Laporan")
            self.laporan_lbl.setFont( self.fontStyle("Helvetica", 10, 500) )
            self.laporan_lbl.setStyleSheet(View.left_menu_lbl)

            left_menu_horizontal = QHBoxLayout()
            left_menu_horizontal.addWidget(self.laporan_btn)
            left_menu_horizontal.addWidget(self.laporan_lbl)
            left_menu_lay.addLayout(left_menu_horizontal)

            self.setMenuClicked(button=self.laporan_btn, label=self.laporan_lbl, page="kelola laporan")
            ###########################################
            
            
            ################ Logout #################
            self.logout_btn =QPushButton()
            self.logout_btn.setFixedSize(30,30)
            self.logout_btn.setIcon( QIcon(self.icon_path+"sign-out-alt.png") )
            self.logout_btn.setStyleSheet(View.left_menu_btn)
            self.logout_lbl = ClickableLabel("Logout")
            self.logout_lbl.setFont( self.fontStyle("Helvetica", 10, 500) )
            self.logout_lbl.setStyleSheet(View.left_menu_lbl)

            left_menu_horizontal = QHBoxLayout()
            left_menu_horizontal.addWidget(self.logout_btn)
            left_menu_horizontal.addWidget(self.logout_lbl)
            left_menu_lay.addLayout(left_menu_horizontal)

            self.setMenuClicked(button=self.logout_btn, label=self.logout_lbl, page="logout")
            ###########################################


            left_menu_lay.addStretch(1)
            # spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
            # left_menu_lay.addSpacerItem(spacer)

            ################ QStackedWidget here #################
            
            # pages -> set pages container
            self.createPage(page="home")
            self.createPage(page="rfid")
            self.createPage(page="users")
            self.createPage(page="kasir")
            self.createPage(page="karcis")
            self.createPage(page="tarif")
            self.createPage(page="voucher")
            self.createPage(page="laporan")
            
            # put page container into stacked widget
            self.stacked_widget.addWidget(self.welcome_lbl)     # --> 0
            self.stacked_widget.addWidget(self.rfid_container)  # --> 1
            self.stacked_widget.addWidget(self.users_container) # --> 2
            self.stacked_widget.addWidget(self.kasir_container) # --> 3
            self.stacked_widget.addWidget(self.karcis_container)    # --> 4
            self.stacked_widget.addWidget(self.tarif_container)     # --> 5
            self.stacked_widget.addWidget(self.voucher_container)   # --> 6
            self.stacked_widget.addWidget(self.laporan_container)   # --> 7
            self.stacked_widget.setCurrentIndex(0)
            
            # set the animation stacked widget
            self.stacked_animation = QPropertyAnimation(self.stacked_widget, b"geometry")
            ###########################################

            
            self.window.setCentralWidget(main_win_widget)

            self.window.show()
            
            # self.windowBarAction("kelola laporan")

            # sys.exit(self.app.exec_())
            
m = Main()


m.Login()()
# m.AdminDashboard()
