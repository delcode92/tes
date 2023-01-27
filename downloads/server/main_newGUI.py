import sys,cv2,os
# from client.client_service import Client
from PyQt5.QtWidgets import (QSpacerItem, QLayout, QSizePolicy,QApplication, QMainWindow, QWidget, QFrame, QLabel, QPushButton, QAction,
QLineEdit, QCheckBox, QGroupBox, QComboBox, QRadioButton, QScrollArea, QMdiArea, QMdiSubWindow, QVBoxLayout, QFormLayout, QHBoxLayout, QGridLayout, QStackedLayout
)

from PyQt5.QtGui import QPalette, QColor, QImage, QPixmap, QFont, QCursor
from PyQt5.QtCore import QThread, QSize, Qt, QEvent, QObject, QCoreApplication, pyqtSignal, pyqtSlot



class Main:
    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
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
            # window_setter = {
            #     "title":"Admin Dashboard", 
            #     "style":self.win_dashboard
            # }
            
            # menubar = [
            #     {"Main":"Dashboard"},
            #     {"RFID":("Kelola RFID", "Tambah RFID")},
            #     {"User":("Kelola User", "Tambah User")},
            #     {"Kasir":("Kelola Kasir", "Tambah Kasir")},
            #     {"Gate":("Kelola Gate", "Tambah Gate", "Setting Karcis")},
            #     {"Tarif":("Kelola Tarif", "Aturan Tarif")},
            #     {"Voucher":("Kelola Voucher", "Aturan Voucher")},
            #     {"Laporan":("Kelola Laporan")},
            #     {"App":("Logout")}
            # ]

            
            # # create window
            # self.CreateWindow(window_setter, self.window)

            self.window = QMainWindow()
            
            # create layouts
            # main_win_layout = self.CreateLayout(("VBoxLayout", False))
            main_win_layout = QVBoxLayout()
            
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

            # self.horizontalLayout = QHBoxLayout(self.Top_Bar)
            # self.horizontalLayout.setSpacing(0)

            # self.frame_toggle = QFrame(self.Top_Bar)
            # self.frame_toggle.setObjectName(u"frame_toggle")
            # self.frame_toggle.setMaximumSize(QSize(70, 40))
            # self.frame_toggle.setStyleSheet(u"background-color: rgb(85, 170, 255);")
            # self.frame_toggle.setFrameShape(QFrame.StyledPanel)
            # self.frame_toggle.setFrameShadow(QFrame.Raised)
            # self.horizontalLayout.addWidget(self.frame_toggle)

            test_btn = QPushButton(self.Top_Bar)
            test_btn.setText("clickme")
            test_btn.setMinimumSize(200, 40)
            test_btn.setStyleSheet("background-color: rgb(85, 170, 255);")
            # hori_1 = QHBoxLayout(self.Top_Bar)
            # hori_1.addWidget(test_btn)

            # left frame
            # create widget to horizontal layout parent
            # horizontal_widget = QWidget()
            
            # add horizontal layout into vertical layout
            # horizontal_lay = self.CreateLayout(("HBoxLayout", False))
            # horizontal_widget.setLayout(horizontal_lay)
            # horizontal_widget.setStyleSheet(u"background-color: grey;")

            # add qframe into that horizontal layout
            # left_qframe = QFrame()
            # left_qframe.setMaximumSize(QSize(120, 100))
            # left_qframe.setStyleSheet(u"background-color: red;")
            # horizontal_lay.addWidget( left_qframe )

            # welcome label
            welcome_lbl = QLabel("Manless Parking System")
            # welcome_lbl.setFont( self.fontStyle("Helvetica", 50, 80) )
            welcome_lbl.setAlignment(Qt.AlignCenter)
            welcome_lbl.setStyleSheet("background-color:red; color:#fff;")
            
            # add component to layout
            # main_win_layout.addStretch(1)
            main_win_layout.setContentsMargins(0, 0, 0, 0)
            main_win_layout.setSpacing(0)
            main_win_layout.addWidget(self.Top_Bar)
            # main_win_layout.addWidget(horizontal_widget)

            horizontal_lay = QHBoxLayout()
            horizontal_widget = QFrame()
            left_widget = QFrame()
            right_widget = QFrame()
            left_menu_lay =  QVBoxLayout()
            right_content_lay =  QVBoxLayout()

            btn_menu1 =QPushButton("button 1")
            btn_menu2 =QPushButton("button 2")
            
            self.Top_Bar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.Top_Bar.setFixedSize(250, 40)

            left_menu_lay.setContentsMargins(0, 0, 0, 0)
            left_menu_lay.setSpacing(0)
            left_menu_lay.addWidget(btn_menu1)
            left_menu_lay.addWidget(btn_menu2)
            # left_menu_lay.addStretch(1)
            # spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
            # left_menu_lay.addSpacerItem(spacer)


            right_content_lay.setContentsMargins(0, 0, 0, 0)
            right_content_lay.setSpacing(0)
            right_content_lay.addWidget(welcome_lbl)

            # left_widget.setStyleSheet("background-color:grey;")
            left_widget.setMaximumWidth(200)
            # left_widget.setMaximumHeight(300)
            left_widget.setLayout(left_menu_lay)
            right_widget.setLayout(right_content_lay)


            horizontal_lay.setContentsMargins(0, 0, 0, 0)
            horizontal_lay.setSpacing(0)
            horizontal_lay.addWidget(left_widget)
            horizontal_lay.addWidget(right_widget)

            horizontal_widget.setLayout(horizontal_lay)
            horizontal_widget.setStyleSheet("background-color:green;")

            main_win_layout.addWidget(horizontal_widget)
            
            # menubar
            # self.createMenuBar(menubar)
            
            self.window.setCentralWidget(main_win_widget)

            self.window.show()
            sys.exit(self.app.exec_())

m = Main()
m.AdminDashboard()