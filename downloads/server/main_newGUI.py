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
            main_win_layout = self.CreateLayout(("VBoxLayout", False))
            
            # create and set widget for layout
            main_win_widget = QWidget()
            main_win_widget.setLayout(main_win_layout)

            # QFrame
            self.Top_Bar = QFrame()
            self.Top_Bar.setObjectName(u"Top_Bar")
            self.Top_Bar.setMaximumSize(QSize(16777215, 40))
            self.Top_Bar.setStyleSheet(u"background-color: rgb(35, 35, 35); border: 2px solid red;")
            self.Top_Bar.setFrameShape(QFrame.NoFrame)
            self.Top_Bar.setFrameShadow(QFrame.Raised)

            # welcome label
            welcome_lbl = QLabel("Manless Parking System")
            welcome_lbl.setFont( self.fontStyle("Helvetica", 50, 80) )
            welcome_lbl.setAlignment(Qt.AlignCenter)
            welcome_lbl.setStyleSheet("background-color:red; color:#fff;")
            
            # add component to layout
            main_win_layout.addWidget(self.Top_Bar)
            main_win_layout.addWidget(welcome_lbl)
            
            # menubar
            # self.createMenuBar(menubar)
            
            self.window.setCentralWidget(main_win_widget)

            self.window.show()
            sys.exit(self.app.exec_())

m = Main()
m.AdminDashboard()