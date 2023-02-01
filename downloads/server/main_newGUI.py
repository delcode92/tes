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
    
    def setMenuClicked(self, button=None, label=None, page=""):
        button.clicked.connect(lambda: self.windowBarAction(page))
        label.clicked.connect(lambda: self.windowBarAction(page))

    def createPage(self, page=""):
        match page:
            
            case "home":
                dashboard_lbl = QLabel()
                dashboard_lbl.setText("Admin Dashboard")
                dashboard_lbl.setFont( self.fontStyle("Helvetica", 11, 500) )
                dashboard_lbl.setStyleSheet("background:#363A3E; color: #FFF; margin-left:10px; padding-top:8px; padding-bottom:8px;")
                dashboard_lbl.setAlignment(Qt.AlignCenter)
                
                self.top_lay.addWidget(self.burger_menu)
                self.top_lay.addWidget(dashboard_lbl)
                
                # welcome label
                self.welcome_lbl = QLabel("Manless Parking System")
                self.welcome_lbl.setFont( self.fontStyle("Helvetica", 50, 80) )
                self.welcome_lbl.setAlignment(Qt.AlignCenter)
                self.welcome_lbl.setStyleSheet("background-color:#bada55; color:#fff;")
            
            
            case "rfid":
                # rfid content
                self.rfid_container = QWidget()
                self.rfid_container_lay = QVBoxLayout()
                rfid_tabs_container_widget = QWidget()
                rfid_tabs_container = QHBoxLayout()
                rfid_tab1 = QPushButton("Tab 1")
                rfid_tab2 = QPushButton("Tab 2")
                self.rfid_stack = QStackedWidget()
                rfid_content1 = QWidget()
                rfid_content2 = QWidget()

                # tabs
                rfid_tab1.setMaximumWidth(180)
                rfid_tab2.setMaximumWidth(180)
                rfid_tab1.setStyleSheet("background: #fff; color: #000;")
                rfid_tab2.setStyleSheet("background: #fff; color: #000;")
                rfid_tab1.clicked.connect(lambda: self.Tabs(self.rfid_stack, index=0))
                rfid_tab2.clicked.connect(lambda: self.Tabs(self.rfid_stack, index=1))

                rfid_tabs_container.setAlignment(Qt.AlignLeft)
                rfid_tabs_container.addWidget(rfid_tab1)
                rfid_tabs_container.addWidget(rfid_tab2)

                # set rfid layout & widget
                self.rfid_container_lay.setContentsMargins(0,0,0,0)
                self.rfid_container_lay.setSpacing(0)

                rfid_tabs_container_widget.setStyleSheet("background: #bada55;")
                self.rfid_stack.setStyleSheet("background: #bada55;")
                
                self.rfid_container.setLayout(self.rfid_container_lay)
                rfid_tabs_container_widget.setLayout(rfid_tabs_container)

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
            
            case "users":
                # users content
                self.users_container = QWidget()
                self.users_container_lay = QVBoxLayout()
                users_tabs_container_widget = QWidget()
                users_tabs_container = QHBoxLayout()
                users_tab1 = QPushButton("Tab 1")
                users_tab2 = QPushButton("Tab 2")
                self.users_stack = QStackedWidget()
                users_content1 = QWidget()
                users_content2 = QWidget()

                # tabs
                users_tab1.setMaximumWidth(180)
                users_tab2.setMaximumWidth(180)
                users_tab1.setStyleSheet("background: #fff; color: #000;")
                users_tab2.setStyleSheet("background: #fff; color: #000;")
                users_tab1.clicked.connect(lambda: self.Tabs(self.users_stack, index=0))
                users_tab2.clicked.connect(lambda: self.Tabs(self.users_stack, index=1))

                users_tabs_container.setAlignment(Qt.AlignLeft)
                users_tabs_container.addWidget(users_tab1)
                users_tabs_container.addWidget(users_tab2)

                # set users layout & widget
                self.users_container_lay.setContentsMargins(0,0,0,0)
                self.users_container_lay.setSpacing(0)

                users_tabs_container_widget.setStyleSheet("background: #bada55;")
                self.users_stack.setStyleSheet("background: #bada55;")
                
                self.users_container.setLayout(self.users_container_lay)
                users_tabs_container_widget.setLayout(users_tabs_container)

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

                # set widget for tab1 layout
                users_content1 = QLabel("Another Page 1")
                users_content1.setFont( self.fontStyle("Helvetica", 50, 80) )
                users_content1.setAlignment(Qt.AlignCenter)
                users_content1.setStyleSheet("background-color:#badaee; color:#fff;")
                users_content1_lay.addWidget(users_content1)

                # set widget for tab2 layout
                users_content2 = QLabel("Another Page 2")
                users_content2.setFont( self.fontStyle("Helvetica", 50, 80) )
                users_content2.setAlignment(Qt.AlignCenter)
                users_content2.setStyleSheet("background-color:#badaff; color:#fff;")
                users_content2_lay.addWidget(users_content2)
            
            case "kasir":
                # kasir content
                self.kasir_container = QWidget()
                self.kasir_container_lay = QVBoxLayout()
                kasir_tabs_container_widget = QWidget()
                kasir_tabs_container = QHBoxLayout()
                kasir_tab1 = QPushButton("Tab 1")
                kasir_tab2 = QPushButton("Tab 2")
                self.kasir_stack = QStackedWidget()
                kasir_content1 = QWidget()
                kasir_content2 = QWidget()

                # tabs
                kasir_tab1.setMaximumWidth(180)
                kasir_tab2.setMaximumWidth(180)
                kasir_tab1.setStyleSheet("background: #fff; color: #000;")
                kasir_tab2.setStyleSheet("background: #fff; color: #000;")
                kasir_tab1.clicked.connect(lambda: self.Tabs(self.kasir_stack, index=0))
                kasir_tab2.clicked.connect(lambda: self.Tabs(self.kasir_stack, index=1))

                kasir_tabs_container.setAlignment(Qt.AlignLeft)
                kasir_tabs_container.addWidget(kasir_tab1)
                kasir_tabs_container.addWidget(kasir_tab2)

                # set kasir layout & widget
                self.kasir_container_lay.setContentsMargins(0,0,0,0)
                self.kasir_container_lay.setSpacing(0)

                kasir_tabs_container_widget.setStyleSheet("background: #bada55;")
                self.kasir_stack.setStyleSheet("background: #bada55;")
                
                self.kasir_container.setLayout(self.kasir_container_lay)
                kasir_tabs_container_widget.setLayout(kasir_tabs_container)

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

                # set widget for tab1 layout
                kasir_content1 = QLabel("Another Page 1")
                kasir_content1.setFont( self.fontStyle("Helvetica", 50, 80) )
                kasir_content1.setAlignment(Qt.AlignCenter)
                kasir_content1.setStyleSheet("background-color:#badaee; color:#fff;")
                kasir_content1_lay.addWidget(kasir_content1)

                # set widget for tab2 layout
                kasir_content2 = QLabel("Another Page 2")
                kasir_content2.setFont( self.fontStyle("Helvetica", 50, 80) )
                kasir_content2.setAlignment(Qt.AlignCenter)
                kasir_content2.setStyleSheet("background-color:#badaff; color:#fff;")
                kasir_content2_lay.addWidget(kasir_content2)
            
            case "karcis":
                # karcis content
                self.karcis_container = QWidget()
                self.karcis_container_lay = QVBoxLayout()
                karcis_tabs_container_widget = QWidget()
                karcis_tabs_container = QHBoxLayout()
                karcis_tab1 = QPushButton("Tab 1")
                karcis_tab2 = QPushButton("Tab 2")
                self.karcis_stack = QStackedWidget()
                karcis_content1 = QWidget()
                karcis_content2 = QWidget()

                # tabs
                karcis_tab1.setMaximumWidth(180)
                karcis_tab2.setMaximumWidth(180)
                karcis_tab1.setStyleSheet("background: #fff; color: #000;")
                karcis_tab2.setStyleSheet("background: #fff; color: #000;")
                karcis_tab1.clicked.connect(lambda: self.Tabs(self.karcis_stack, index=0))
                karcis_tab2.clicked.connect(lambda: self.Tabs(self.karcis_stack, index=1))

                karcis_tabs_container.setAlignment(Qt.AlignLeft)
                karcis_tabs_container.addWidget(karcis_tab1)
                karcis_tabs_container.addWidget(karcis_tab2)

                # set karcis layout & widget
                self.karcis_container_lay.setContentsMargins(0,0,0,0)
                self.karcis_container_lay.setSpacing(0)

                karcis_tabs_container_widget.setStyleSheet("background: #bada55;")
                self.karcis_stack.setStyleSheet("background: #bada55;")
                
                self.karcis_container.setLayout(self.karcis_container_lay)
                karcis_tabs_container_widget.setLayout(karcis_tabs_container)

                self.karcis_container_lay.addWidget(karcis_tabs_container_widget)
                self.karcis_container_lay.addWidget(self.karcis_stack)

                # add tabs
                self.karcis_stack.addWidget(karcis_content1)
                self.karcis_stack.addWidget(karcis_content2)
                
                # set widget and layout
                karcis_content1_lay = QVBoxLayout()
                karcis_content1.setLayout( karcis_content1_lay )
                
                # set widget and layout
                karcis_content2_lay = QVBoxLayout()
                karcis_content2.setLayout( karcis_content2_lay )

                # set widget for tab1 layout
                karcis_content1 = QLabel("Another Page 1")
                karcis_content1.setFont( self.fontStyle("Helvetica", 50, 80) )
                karcis_content1.setAlignment(Qt.AlignCenter)
                karcis_content1.setStyleSheet("background-color:#badaee; color:#fff;")
                karcis_content1_lay.addWidget(karcis_content1)

                # set widget for tab2 layout
                karcis_content2 = QLabel("Another Page 2")
                karcis_content2.setFont( self.fontStyle("Helvetica", 50, 80) )
                karcis_content2.setAlignment(Qt.AlignCenter)
                karcis_content2.setStyleSheet("background-color:#badaff; color:#fff;")
                karcis_content2_lay.addWidget(karcis_content2)
            
            case "tarif":
                # tarif content
                self.tarif_container = QWidget()
                self.tarif_container_lay = QVBoxLayout()
                tarif_tabs_container_widget = QWidget()
                tarif_tabs_container = QHBoxLayout()
                tarif_tab1 = QPushButton("Tab 1")
                tarif_tab2 = QPushButton("Tab 2")
                self.tarif_stack = QStackedWidget()
                tarif_content1 = QWidget()
                tarif_content2 = QWidget()

                # tabs
                tarif_tab1.setMaximumWidth(180)
                tarif_tab2.setMaximumWidth(180)
                tarif_tab1.setStyleSheet("background: #fff; color: #000;")
                tarif_tab2.setStyleSheet("background: #fff; color: #000;")
                tarif_tab1.clicked.connect(lambda: self.Tabs(self.tarif_stack, index=0))
                tarif_tab2.clicked.connect(lambda: self.Tabs(self.tarif_stack, index=1))

                tarif_tabs_container.setAlignment(Qt.AlignLeft)
                tarif_tabs_container.addWidget(tarif_tab1)
                tarif_tabs_container.addWidget(tarif_tab2)

                # set tarif layout & widget
                self.tarif_container_lay.setContentsMargins(0,0,0,0)
                self.tarif_container_lay.setSpacing(0)

                tarif_tabs_container_widget.setStyleSheet("background: #bada55;")
                self.tarif_stack.setStyleSheet("background: #bada55;")
                
                self.tarif_container.setLayout(self.tarif_container_lay)
                tarif_tabs_container_widget.setLayout(tarif_tabs_container)

                self.tarif_container_lay.addWidget(tarif_tabs_container_widget)
                self.tarif_container_lay.addWidget(self.tarif_stack)

                # add tabs
                self.tarif_stack.addWidget(tarif_content1)
                self.tarif_stack.addWidget(tarif_content2)
                
                # set widget and layout
                tarif_content1_lay = QVBoxLayout()
                tarif_content1.setLayout( tarif_content1_lay )
                
                # set widget and layout
                tarif_content2_lay = QVBoxLayout()
                tarif_content2.setLayout( tarif_content2_lay )

                # set widget for tab1 layout
                tarif_content1 = QLabel("Another Page 1")
                tarif_content1.setFont( self.fontStyle("Helvetica", 50, 80) )
                tarif_content1.setAlignment(Qt.AlignCenter)
                tarif_content1.setStyleSheet("background-color:#badaee; color:#fff;")
                tarif_content1_lay.addWidget(tarif_content1)

                # set widget for tab2 layout
                tarif_content2 = QLabel("Another Page 2")
                tarif_content2.setFont( self.fontStyle("Helvetica", 50, 80) )
                tarif_content2.setAlignment(Qt.AlignCenter)
                tarif_content2.setStyleSheet("background-color:#badaff; color:#fff;")
                tarif_content2_lay.addWidget(tarif_content2)
            
            case "voucher":
                # voucher content
                self.voucher_container = QWidget()
                self.voucher_container_lay = QVBoxLayout()
                voucher_tabs_container_widget = QWidget()
                voucher_tabs_container = QHBoxLayout()
                voucher_tab1 = QPushButton("Tab 1")
                voucher_tab2 = QPushButton("Tab 2")
                self.voucher_stack = QStackedWidget()
                voucher_content1 = QWidget()
                voucher_content2 = QWidget()

                # tabs
                voucher_tab1.setMaximumWidth(180)
                voucher_tab2.setMaximumWidth(180)
                voucher_tab1.setStyleSheet("background: #fff; color: #000;")
                voucher_tab2.setStyleSheet("background: #fff; color: #000;")
                voucher_tab1.clicked.connect(lambda: self.Tabs(self.voucher_stack, index=0))
                voucher_tab2.clicked.connect(lambda: self.Tabs(self.voucher_stack, index=1))

                voucher_tabs_container.setAlignment(Qt.AlignLeft)
                voucher_tabs_container.addWidget(voucher_tab1)
                voucher_tabs_container.addWidget(voucher_tab2)

                # set voucher layout & widget
                self.voucher_container_lay.setContentsMargins(0,0,0,0)
                self.voucher_container_lay.setSpacing(0)

                voucher_tabs_container_widget.setStyleSheet("background: #bada55;")
                self.voucher_stack.setStyleSheet("background: #bada55;")
                
                self.voucher_container.setLayout(self.voucher_container_lay)
                voucher_tabs_container_widget.setLayout(voucher_tabs_container)

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

                # set widget for tab1 layout
                voucher_content1 = QLabel("Another Page 1")
                voucher_content1.setFont( self.fontStyle("Helvetica", 50, 80) )
                voucher_content1.setAlignment(Qt.AlignCenter)
                voucher_content1.setStyleSheet("background-color:#badaee; color:#fff;")
                voucher_content1_lay.addWidget(voucher_content1)

                # set widget for tab2 layout
                voucher_content2 = QLabel("Another Page 2")
                voucher_content2.setFont( self.fontStyle("Helvetica", 50, 80) )
                voucher_content2.setAlignment(Qt.AlignCenter)
                voucher_content2.setStyleSheet("background-color:#badaff; color:#fff;")
                voucher_content2_lay.addWidget(voucher_content2)
            
            case "laporan":
                # laporan content
                self.laporan_container = QWidget()
                self.laporan_container_lay = QVBoxLayout()
                laporan_tabs_container_widget = QWidget()
                laporan_tabs_container = QHBoxLayout()
                laporan_tab1 = QPushButton("Tab 1")
                laporan_tab2 = QPushButton("Tab 2")
                self.laporan_stack = QStackedWidget()
                laporan_content1 = QWidget()
                laporan_content2 = QWidget()

                # tabs
                laporan_tab1.setMaximumWidth(180)
                laporan_tab2.setMaximumWidth(180)
                laporan_tab1.setStyleSheet("background: #fff; color: #000;")
                laporan_tab2.setStyleSheet("background: #fff; color: #000;")
                laporan_tab1.clicked.connect(lambda: self.Tabs(self.laporan_stack, index=0))
                laporan_tab2.clicked.connect(lambda: self.Tabs(self.laporan_stack, index=1))

                laporan_tabs_container.setAlignment(Qt.AlignLeft)
                laporan_tabs_container.addWidget(laporan_tab1)
                laporan_tabs_container.addWidget(laporan_tab2)

                # set laporan layout & widget
                self.laporan_container_lay.setContentsMargins(0,0,0,0)
                self.laporan_container_lay.setSpacing(0)

                laporan_tabs_container_widget.setStyleSheet("background: #bada55;")
                self.laporan_stack.setStyleSheet("background: #bada55;")
                
                self.laporan_container.setLayout(self.laporan_container_lay)
                laporan_tabs_container_widget.setLayout(laporan_tabs_container)

                self.laporan_container_lay.addWidget(laporan_tabs_container_widget)
                self.laporan_container_lay.addWidget(self.laporan_stack)

                # add tabs
                self.laporan_stack.addWidget(laporan_content1)
                self.laporan_stack.addWidget(laporan_content2)
                
                # set widget and layout
                laporan_content1_lay = QVBoxLayout()
                laporan_content1.setLayout( laporan_content1_lay )
                
                # set widget and layout
                laporan_content2_lay = QVBoxLayout()
                laporan_content2.setLayout( laporan_content2_lay )

                # set widget for tab1 layout
                laporan_content1 = QLabel("Another Page 1")
                laporan_content1.setFont( self.fontStyle("Helvetica", 50, 80) )
                laporan_content1.setAlignment(Qt.AlignCenter)
                laporan_content1.setStyleSheet("background-color:#badaee; color:#fff;")
                laporan_content1_lay.addWidget(laporan_content1)

                # set widget for tab2 layout
                laporan_content2 = QLabel("Another Page 2")
                laporan_content2.setFont( self.fontStyle("Helvetica", 50, 80) )
                laporan_content2.setAlignment(Qt.AlignCenter)
                laporan_content2.setStyleSheet("background-color:#badaff; color:#fff;")
                laporan_content2_lay.addWidget(laporan_content2)
            
            case "logout":
                ...

            case default:
                pass    


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

            # top layout
            self.top_lay_widget = QWidget()
            self.top_lay = QHBoxLayout()
            
            self.top_lay.setContentsMargins(0, 0, 0, 0)
            self.top_lay.setSpacing(0)
            self.top_lay_widget.setStyleSheet("background: #363A3E;")
            self.top_lay_widget.setLayout(self.top_lay)

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

            # add component to layout
            main_win_layout.setContentsMargins(0, 0, 0, 0)
            main_win_layout.setSpacing(0)
            main_win_layout.addWidget(self.top_lay_widget)
          
            horizontal_lay = QHBoxLayout()
            horizontal_widget = QFrame()
            self.left_widget = QFrame()
            right_widget = QFrame()
            left_menu_lay =  QVBoxLayout()
            self.right_content_lay =  QVBoxLayout()
            self.stacked_widget = QStackedWidget()
            
            left_menu_lay.setContentsMargins(0, 0, 0, 0)
            left_menu_lay.setSpacing(0)
            
            ################ Home #################
            self.home_btn =QPushButton()
            self.home_btn.setFixedSize(30,30)
            self.home_btn.setIcon( QIcon(icon_path+"home.png") )
            self.home_btn.setStyleSheet(View.left_menu_btn)
            self.home_lbl = ClickableLabel("Home")
            self.home_lbl.setFont( self.fontStyle("Helvetica", 10, 500) )
            self.home_lbl.setStyleSheet(View.left_menu_lbl)

            left_menu_horizontal = QHBoxLayout()
            left_menu_horizontal.addWidget(self.home_btn)
            left_menu_horizontal.addWidget(self.home_lbl)
            left_menu_lay.addLayout(left_menu_horizontal)

            self.setMenuClicked(button=self.home_btn, label=self.home_lbl, page="dashboard")
            # self.home_btn.clicked.connect(lambda: self.windowBarAction("dashboard"))
            # self.home_lbl.clicked.connect(lambda: self.windowBarAction("dashboard"))
            ###########################################
            
            
            ################ RFID #################
            self.rfid_btn =QPushButton()
            self.rfid_btn.setFixedSize(30,30)
            self.rfid_btn.setIcon( QIcon(icon_path+"share.png") )
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
            self.users_btn.setIcon( QIcon(icon_path+"users.png") )
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
            self.kasir_btn.setIcon( QIcon(icon_path+"computer.png") )
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
            self.karcis_btn.setIcon( QIcon(icon_path+"receipt.png") )
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
            self.tarif_btn.setIcon( QIcon(icon_path+"usd-circle.png") )
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
            self.voucher_btn.setIcon( QIcon(icon_path+"ticket.png") )
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
            self.laporan_btn.setIcon( QIcon(icon_path+"document-signed.png") )
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
            self.logout_btn.setIcon( QIcon(icon_path+"sign-out-alt.png") )
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
            
            # pages
            self.createPage(page="home")
            self.createPage(page="rfid")
            self.createPage(page="users")
            self.createPage(page="kasir")
            self.createPage(page="karcis")
            self.createPage(page="tarif")
            self.createPage(page="voucher")
            self.createPage(page="laporan")
            self.createPage(page="logout")
            
            self.rfid_stack.setCurrentIndex(0)
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