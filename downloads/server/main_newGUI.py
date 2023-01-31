import sys,cv2,os

from framework import *


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

    # def menu_func(self, type=""):
    #     match type:
    #         case "home":
    #             ...
    #         case default:
    #             pass    

    def AdminDashboard(self):
            window_setter = {
                "title":"Admin Dashboard", 
                "style":self.win_dashboard
            }
            
            # # create window
            self.CreateWindow(window_setter, self.window)
            self.window.setWindowFlags(Qt.FramelessWindowHint)

            # create layouts
            main_win_layout = self.CreateLayout(("VBoxLayout", False))
            
            # create and set widget for layout
            main_win_widget = QWidget()
            main_win_widget.setLayout(main_win_layout)

            # QFrame
            # self.Top_Bar = QFrame()
            # self.Top_Bar.setObjectName(u"Top_Bar")
            # # self.Top_Bar.setMaximumSize(QSize(16777215, 40))
            # self.Top_Bar.setStyleSheet(u"background-color: red;")
            # self.Top_Bar.setFrameShape(QFrame.NoFrame)
            # self.Top_Bar.setFrameShadow(QFrame.Raised)
            #  # self.Top_Bar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            # self.Top_Bar.setFixedHeight(30)

            # top layout
            top_lay_widget = QWidget()
            top_lay = QHBoxLayout()
            
            top_lay.setContentsMargins(0, 0, 0, 0)
            top_lay.setSpacing(0)
            top_lay_widget.setStyleSheet("background: #363A3E;")
            top_lay_widget.setLayout(top_lay)

            # Get path
            path = os.path.dirname(os.path.realpath(__file__))
            os_name = os.name

            if os_name == 'posix':
                icon_path = '/icons'.join([path, "/"])
            elif os_name == 'nt':
                icon_path = '\icons'.join([path, "\\"])
            
            self.burger_menu = QPushButton()
            self.burger_menu.setIcon(QIcon(icon_path+"menu-burger.png"))
            self.burger_menu.setFixedSize(30, 30)
            self.burger_menu.setStyleSheet("background-color: #1d262d;")
            self.burger_menu.clicked.connect(lambda: self.toggleMenu(250, True, icon_path))

            dashboard_lbl = QLabel()
            dashboard_lbl.setText("Admin Dashboard")
            dashboard_lbl.setFont( self.fontStyle("Helvetica", 11, 500) )
            dashboard_lbl.setStyleSheet("background:#363A3E; color: #FFF; margin-left:10px; padding-top:8px; padding-bottom:8px;")
            dashboard_lbl.setAlignment(Qt.AlignCenter)
            
            top_lay.addWidget(self.burger_menu)
            top_lay.addWidget(dashboard_lbl)
            # dashboard_lbl.setFixedWidth(dashboard_lbl.width()+610)
            # print("lbl width", dashboard_lbl.width())

            # welcome label
            welcome_lbl = QLabel("Manless Parking System")
            welcome_lbl.setFont( self.fontStyle("Helvetica", 50, 80) )
            welcome_lbl.setAlignment(Qt.AlignCenter)
            welcome_lbl.setStyleSheet("background-color:#bada55; color:#fff;")
            

            ################ Home #################
            # page_layout = QHBoxLayout()
            ###########################################


            ################ RFID page #################
            
            # rfid widget
            # rfid_page = QWidget()
            # rfid_page.setLayout(page_layout)

            # rfid content
            rfid_container = QWidget()
            rfid_container_lay = QVBoxLayout()
            rfid_tabs_container_widget = QWidget()
            rfid_tabs_container = QHBoxLayout()
            rfid_tab1 = QPushButton("Tab 1")
            rfid_tab2 = QPushButton("Tab 2")
            rfid_stack = QStackedWidget()
            rfid_content1 = QWidget()
            rfid_content2 = QWidget()

            # tabs
            rfid_tab1.setStyleSheet("background: #fff; color: #000;")
            rfid_tab2.setStyleSheet("background: #fff; color: #000;")
            rfid_tabs_container.addWidget(rfid_tab1)
            rfid_tabs_container.addWidget(rfid_tab2)

            # set rfid layout & widget
            # rfid_tabs_container.setContentsMargins(0,0,0,0)
            # rfid_tabs_container.setSpacing(0)
            rfid_container_lay.setContentsMargins(0,0,0,0)
            rfid_container_lay.setSpacing(0)

            rfid_tabs_container_widget.setStyleSheet("background: #bada55;")
            rfid_stack.setStyleSheet("background: #bada55;")
            # rfid_stack.setContentsMargins(-100,0,0,0)
            # rfid_stack.setSpacing(0)

            

            rfid_container.setLayout(rfid_container_lay)
            rfid_tabs_container_widget.setLayout(rfid_tabs_container)

            rfid_container_lay.addWidget(rfid_tabs_container_widget)
            rfid_container_lay.addWidget(rfid_stack)

            # add tabs
            rfid_stack.addWidget(rfid_content1)
            rfid_stack.addWidget(rfid_content2)
           
            # set widget and layout
            rfid_content1_lay = QVBoxLayout()
            rfid_content1.setLayout( rfid_content1_lay )
            
            # set widget and layout
            rfid_content2_lay = QVBoxLayout()
            rfid_content2.setLayout( rfid_content2_lay )

            # set widget for tab1 layout
            rfid_content1 = QLabel("Another Page 1")
            rfid_content1.setFont( self.fontStyle("Helvetica", 50, 80) )
            rfid_content1.setAlignment(Qt.AlignCenter)
            rfid_content1.setStyleSheet("background-color:#bada55; color:#fff;")
            rfid_content1_lay.addWidget(rfid_content1)

            # set widget for tab2 layout
            rfid_content2 = QLabel("Another Page 2")
            rfid_content2.setFont( self.fontStyle("Helvetica", 50, 80) )
            rfid_content2.setAlignment(Qt.AlignCenter)
            rfid_content2.setStyleSheet("background-color:#bada55; color:#fff;")
            rfid_content2_lay.addWidget(rfid_content2)
            
            # add rfid tabs widget into main page layout
            # page_layout.addWidget(rfid_tabs)
            ###########################################



            # add component to layout
            # main_win_layout.addStretch(1)
            main_win_layout.setContentsMargins(0, 0, 0, 0)
            main_win_layout.setSpacing(0)
            # main_win_layout.addWidget(self.Top_Bar)
            # main_win_layout.addLayout(top_lay)
            main_win_layout.addWidget(top_lay_widget)
          
            horizontal_lay = QHBoxLayout()
            horizontal_widget = QFrame()
            self.left_widget = QFrame()
            right_widget = QFrame()
            left_menu_lay =  QVBoxLayout()
            self.right_content_lay =  QVBoxLayout()
            self.stacked_widget = QStackedWidget()
            
            # self.left_widget.setStyleSheet("border-right: 0.5px solid #ffffff;")
            left_menu_lay.setContentsMargins(0, 0, 0, 0)
            left_menu_lay.setSpacing(0)
            
            ################ Home #################
            home_btn =QPushButton()
            home_btn.setFixedSize(30,30)
            home_btn.setIcon( QIcon(icon_path+"home.png") )
            home_btn.setStyleSheet("background:#2c3e50;margin-top: 3px;")
            home_lbl = ClickableLabel("Home")
            home_lbl.setFont( self.fontStyle("Helvetica", 10, 500) )
            home_lbl.setStyleSheet(View.left_menu_lbl)

            left_menu_h1 = QHBoxLayout()
            left_menu_h1.addWidget(home_btn)
            left_menu_h1.addWidget(home_lbl)
            left_menu_lay.addLayout(left_menu_h1)

            home_lbl.clicked.connect(lambda: self.windowBarAction("dashboard"))
            ###########################################
            
            
            ################ Home #################
            rfid_btn =QPushButton()
            rfid_btn.setFixedSize(30,30)
            rfid_btn.setIcon( QIcon(icon_path+"share.png") )
            rfid_btn.setStyleSheet("background:#2c3e50;margin-top: 3px;")
            rfid_lbl = ClickableLabel("RFID")
            rfid_lbl.setFont( self.fontStyle("Helvetica", 10, 500) )
            rfid_lbl.setStyleSheet(View.left_menu_lbl)

            left_menu_h2 = QHBoxLayout()
            left_menu_h2.addWidget(rfid_btn)
            left_menu_h2.addWidget(rfid_lbl)
            left_menu_lay.addLayout(left_menu_h2)
            rfid_lbl.clicked.connect(lambda: self.windowBarAction("kelola rfid"))
            ###########################################
            
            
            ################ Home #################
            users_btn =QPushButton()
            users_btn.setFixedSize(30,30)
            users_btn.setIcon( QIcon(icon_path+"users.png") )
            users_btn.setStyleSheet("background:#2c3e50;margin-top: 3px;")
            users_lbl = QLabel("Users")
            users_lbl.setFont( self.fontStyle("Helvetica", 10, 500) )
            users_lbl.setStyleSheet(View.left_menu_lbl)

            left_menu_h3 = QHBoxLayout()
            left_menu_h3.addWidget(users_btn)
            left_menu_h3.addWidget(users_lbl)
            left_menu_lay.addLayout(left_menu_h3)
            ###########################################
            
            
            ################ Home #################
            kasir_btn =QPushButton()
            kasir_btn.setFixedSize(30,30)
            kasir_btn.setIcon( QIcon(icon_path+"usd-circle.png") )
            # kasir_btn.setIconSize(QSize(16, 16))
            kasir_btn.setStyleSheet("background:#2c3e50; margin-top: 5px;")
            kasir_lbl = QLabel("kasir")
            kasir_lbl.setFont( self.fontStyle("Helvetica", 10, 500) )
            kasir_lbl.setStyleSheet(View.left_menu_lbl)

            left_menu_h4 = QHBoxLayout()
            left_menu_h4.addWidget(kasir_btn)
            left_menu_h4.addWidget(kasir_lbl)
            left_menu_lay.addLayout(left_menu_h4)
            ###########################################
            

            left_menu_lay.addStretch(1)
            # spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
            # left_menu_lay.addSpacerItem(spacer)

            ################ QStackedWidget here #################
            rfid_stack.setCurrentIndex(0)
            self.stacked_widget.addWidget(welcome_lbl)
            self.stacked_widget.addWidget(rfid_container)
            self.stacked_widget.setCurrentIndex(0)
            
            # set the animation stacked widget
            self.stacked_animation = QPropertyAnimation(self.stacked_widget, b"geometry")
            ###########################################

            self.right_content_lay.setContentsMargins(0, 0, 0, 0)
            self.right_content_lay.setSpacing(0)
            self.right_content_lay.addWidget(self.stacked_widget)
            
            # self.left_widget.setMinimumSize(40, 0)
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
            
            # menubar
            # self.createMenuBar(menubar)
            
            self.window.setCentralWidget(main_win_widget)

            self.window.show()
            sys.exit(self.app.exec_())

m = Main()
m.AdminDashboard()