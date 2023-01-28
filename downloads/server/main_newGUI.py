import sys,cv2,os
from framework import *



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

    def AdminDashboard(self):
            window_setter = {
                "title":"Admin Dashboard", 
                "style":self.win_dashboard
            }
            
            # # create window
            self.CreateWindow(window_setter, self.window)
 
            # create layouts
            main_win_layout = self.CreateLayout(("VBoxLayout", False))
            
            # create and set widget for layout
            main_win_widget = QWidget()
            main_win_widget.setLayout(main_win_layout)

            # QFrame
            self.Top_Bar = QFrame()
            self.Top_Bar.setObjectName(u"Top_Bar")
            # self.Top_Bar.setMaximumSize(QSize(16777215, 40))
            self.Top_Bar.setStyleSheet(u"background-color: rgb(35, 35, 35);")
            self.Top_Bar.setFrameShape(QFrame.NoFrame)
            self.Top_Bar.setFrameShadow(QFrame.Raised)

            burger_menu = QPushButton(self.Top_Bar)
            burger_menu.setText("Menus")
            burger_menu.setMaximumSize(100, 40)
            burger_menu.setStyleSheet("background-color: rgb(85, 170, 255);")
           
            # welcome label
            welcome_lbl = QLabel("Manless Parking System")
            welcome_lbl.setFont( self.fontStyle("Helvetica", 50, 80) )
            welcome_lbl.setAlignment(Qt.AlignCenter)
            welcome_lbl.setStyleSheet("background-color:red; color:#fff;")
            
            # add component to layout
            # main_win_layout.addStretch(1)
            main_win_layout.setContentsMargins(0, 0, 0, 0)
            main_win_layout.setSpacing(0)
            main_win_layout.addWidget(self.Top_Bar)
          
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
            left_menu_lay.addStretch(1)
            # spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
            # left_menu_lay.addSpacerItem(spacer)


            right_content_lay.setContentsMargins(0, 0, 0, 0)
            right_content_lay.setSpacing(0)
            right_content_lay.addWidget(welcome_lbl)

            left_widget.setMinimumWidth(50)
            left_widget.setMaximumWidth(200)
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