import sys
from framework import *


class Main( Util, View):
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
        sys.exit(self.app.exec_())
   
    def AdminDashboard(self):
        window_setter = {
            "title":"Admin Dashboard", 
            "style":self.win_dashboard
        }
        
        menubar = [
            {"Main":"Dashboard"},
            {"RFID":("Kelola RFID", "Tambah RFID")},
            {"User":("Kelola User", "Tambah User")},
            {"Kasir":("Kelola Kasir", "Tambah Kasir")},
            {"Gate":("Kelola Gate", "Tambah Gate", "Setting Karcis")},
            {"Tarif":("Kelola Tarif", "Aturan Tarif")},
            {"Voucher":("Kelola Voucher", "Aturan Voucher")},
            {"Laporan":("Kelola Laporan")},
            {"App":("Logout")}
        ]

        
        # create window
        self.CreateWindow(window_setter, self.window)
        
        # create layouts
        main_win_layout = self.CreateLayout(("VBoxLayout", False), self.window)
        
        # create and set widget for layout
        main_win_widget = QWidget()
        main_win_widget.setLayout(main_win_layout)

        # welcome label
        welcome_lbl = QLabel("Manless Parking System")
        welcome_lbl.setFont( self.fontStyle("Helvetica", 50, 80) )
        welcome_lbl.setAlignment(Qt.AlignCenter)
        welcome_lbl.setStyleSheet("color:#fff;")
        
        # add component to layout
        main_win_layout.addWidget(welcome_lbl)
        
        # menubar
        self.createMenuBar(menubar)
        
        self.window.setCentralWidget(main_win_widget)

        self.window.show()

        # if self.app_stat == False:
        #     self.app_stat = True 
        # sys.exit(self.app.exec_())
    
    def KasirDashboard(self):
        window_setter = {
            "title":"Kasir Dashboard", 
            "style":self.win_dashboard
        }

        menubar = [ {"App":"Logout"} ]

        # create groupbox
        groupboxes = [
                {
                    "name": "gb_left",
                    "category":"GroupBox",
                    "title":"Transaksi",
                    "max_width": 440,
                    "max_height": 500,
                    "style": self.gb_styling
                },
                {
                    "name": "gb_center",
                    "category":"GroupBox",
                    "title":"Emergency",
                    "max_width": 440,
                    "max_height": 500,
                    "style": self.gb_styling
                },
                {
                    "name": "gb_right",
                    "category":"GroupBox",
                    "title": "Lap.User Bermasalah",
                    "max_width": 440,
                    "max_height": 500,
                    "style": self.gb_styling
                }
            ]
        
        left_content = [
                    {
                        "name":"lbl_barcode_transaksi",
                        "text":"BL/Barcode",
                        "category":"label",
                        "style":self.primary_lbl
                    },
                    {
                        "name":"barcode_transaksi",
                        "category":"lineEdit",
                        "style": self.primary_input
                    },
                    {
                        "name":"lbl_tarif_transaksi",
                        "text":"Tarif(Rp)",
                        "category":"label",
                        "style":self.primary_lbl+"margin-top: 40px;"
                    },
                    {
                        "name":"tarif_transaksi",
                        "category":"lineEdit",
                        "editable": False,
                        "style": self.primary_input,
                    },
                    {
                        "name":"btn_bayar",
                        "category":"pushButton",
                        "text": "Bayar",
                        "style": self.primary_button
                    }
                ]
        

        center_content = [
                {
                    "name": "btn_emergency_kasir",
                    "category":"PushButton",
                    "text": "Emergency Button",
                    "min_width": 212,
                    "min_height": 150,
                    "style": self.emergency_button
                }
        ]

        right_content = [
                {
                        "name":"lbl_barcode_bermasalah",
                        "text":"BL/Barcode",
                        "category":"label",
                        "style":self.primary_lbl
                    },
                    {
                        "name":"barcode_bermasalah",
                        "category":"lineEdit",
                        "style": self.primary_input
                    },
                    {
                        "name":"lbl_tarif_bermasalah",
                        "text":"Tarif(Rp)",
                        "category":"label",
                        "style":self.primary_lbl + "margin-top:15px;"
                    },
                    {
                        "name":"tarif_bermasalah",
                        "category":"lineEdit",
                        "min_height": 40,
                        "editable": False,
                        "style":self.primary_input
                    },
                    {
                        "name":"lbl_ket_bermasalah",
                        "text":"Keterangan",
                        "category":"label",
                        "style":self.primary_lbl + "margin-top:15px;"
                    },
                    {
                        "name":"ket_bermasalah",
                        "category":"lineEdit",
                        "min_height": 40,
                        "style": "border:1px solid #ecf0f1;"+self.bg_grey,
                        "font":self.helvetica_12
                    },
                    {
                        "name":"btn_simpan_bermasalah",
                        "category":"pushButton",
                        "text": "Simpan",
                        "style": self.primary_button
                    }
        ]

        self.CreateWindow( window_setter, self.window )

        # create main layout
        main_layout = self.CreateLayout(("HBoxLayout", False), self.window)

        # create widget & set to main layout
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        
        # add groupboxes into main layout
        self.CreateComponentLayout(groupboxes, main_layout)

        # create layout for Groupbox
        left_vbox = self.CreateLayout(("VBoxLayout", False))
        
        right_vbox = self.CreateLayout(("VBoxLayout", False))
        center_vbox = self.CreateLayout(("VBoxLayout", False))

        # set gb layout
        self.components["gb_left"].setLayout(left_vbox)
        self.components["gb_right"].setLayout(right_vbox)
        self.components["gb_center"].setLayout(center_vbox)

        # add components to left
        left_vbox.addStretch(1)
        self.CreateComponentLayout(left_content, left_vbox)
        
        left_vbox.setContentsMargins(8,40,8,0)
        left_vbox.addStretch(1)

        # add components to center
        self.CreateComponentLayout(center_content, center_vbox)
        
        # add components to right
        right_vbox.addStretch(1)
        self.CreateComponentLayout(right_content, right_vbox)
        right_vbox.addStretch(1)

        # menubar
        self.createMenuBar(menubar)
        
        # show app
        self.window.setCentralWidget(main_widget)
        self.window.show()
        # sys.exit(self.app.exec_())
        

m = Main()
m.Login()
