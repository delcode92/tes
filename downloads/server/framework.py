import sys,cv2,os
# from client.client_service import Client
from PyQt5.QtWidgets import (QMessageBox, QShortcut, QDateEdit, QTableWidget, QHeaderView, QTableWidgetItem, QStackedWidget, QTabWidget, QSpacerItem, QLayout, QSizePolicy,QApplication, QMainWindow, QWidget, QFrame, QLabel, QPushButton, QAction,
QLineEdit, QSpinBox, QCheckBox, QGroupBox, QComboBox, QRadioButton, QScrollArea, QMdiArea, QMdiSubWindow, QVBoxLayout, QFormLayout, QHBoxLayout, QGridLayout, QStackedLayout
)

from PyQt5.QtGui import QKeySequence, QImage, QPixmap, QFont, QCursor, QIcon, QDoubleValidator
from PyQt5.QtCore import QTimer, QTime, QDate, QDateTime, QPropertyAnimation, QThread, QSize, Qt, QEvent, QObject, QCoreApplication, pyqtSignal, pyqtSlot

from controller import Controller

# from view_resource.adm_dashboard import AdminDashboard

class View:
    border_none = "border: transparent;"
    border = "border: 1px solid black;"
    border_light_grey = "border: 1px solid #D3D3D3;"
    color_white = "color: #ffffff;"
    bg_black = "background-color: #000000;"
    bg_grey = "background-color: #f4f4f4;"
    bg_red = "background-color: red;"
    bg_light_green = "background-color: #0CD0AA;"
    bg_light_red = "background-color: #FF7B7B;"
    bg_white = "background-color: #FFFFFF;"
    bg_aspal = "background-color: #34495e;"
    block_children = "border: 1px solid #b2bec3;"
    
    # main windows dashboard styling
    win_dashboard = """
                    QMainWindow{
                        background-color: #34495e; 
                        color:#fff;
                    }
                    QMenuBar {
                        background-color: rgb(49,49,49);
                        color: rgb(255,255,255);
                        border: 1px solid #000;
                    }

                    QMenuBar::item {
                        padding: 8px;
                        background-color: rgb(49,49,49);
                        color: rgb(255,255,255);
                    }

                    QMenuBar::item::selected {
                        background-color: rgb(30,30,30);
                    }

                    QMenu {
                        background-color: rgb(49,49,49);
                        color: rgb(255,255,255);
                        border: 1px solid #000;           
                    }

                    QMenu::item::selected {
                        background-color: rgb(30,30,30);

                """
    
    # admin left menu styling
    left_menu_btn = """QPushButton{
                            background:#2c3e50;
                        }
                        QPushButton:hover{
                            background:#fa0;
                        }
                        QPushButton[active="true"]{
                            background:#fa0;
                        }
                        """


    left_menu_lbl = """QLabel{
                            background:#2c3e50; 
                            color:#fff;margin-left:12px; 
                            border-bottom: 1px solid #8395a7;
                            padding-top: 8px;
                            padding-bottom: 8px;
                        }
                        QLabel:hover{
                            background: #525A62;
                        }
                        QLabel[active="true"]{
                            background: #525A62;
                        }
            """
    tab_button = """QPushButton{
                        color:#fff; 
                        font-size:13px; 
                        font-weight:600;

                        background: #7f89ff;
                        border: none;
                        padding: 8px;
                        border-radius: 15px;
                    }
                    QPushButton:hover{
                        background: #ff7675;
                    }

                    QPushButton[active="true"]{
                        background: #ff7675;
                    }

    """

    # filter
    

    # button styling
    primary_button ="""QPushButton {
                    margin-top:15px; 
                    height:35px; 
                    background-color: #36f; 
                    color:#fff; 
                    border:none;

                    font-family: Helvetica;
                    font-size: 13px;
                    font-weight: 500;
                }
                QPushButton:focus{ background-color: #4B78FF; }
                QPushButton:hover {
                    background-color: #4B78FF;
    """

    primary_update_button ="""QPushButton {
                    height:35px; 
                    background-color: #36f; 
                    color:#fff; 
                    border:none;

                    font-family: Helvetica;
                    font-size: 13px;
                    font-weight: 500;
                }
                QPushButton:focus{ background-color: #4B78FF; }
                QPushButton:hover {
                    background-color: #4B78FF;
    """

    primary_add_button ="""QPushButton {
                    height:35px; 
                    background-color: #fa0; 
                    color:#fff; 
                    border:none;

                    font-family: Helvetica;
                    font-size: 13px;
                    font-weight: 500;
                }
                QPushButton:focus{ background-color: #4B78FF; }
                QPushButton:hover {
                    background-color: #9A711E;
    """

    # edit_btn_action = """QPushButton {
    #                     background-color:#DDF9FF; 
    #                     color: #fff; 
    #                     font-weight:500; 
    #                     font-size: 14px; 
    #                     border:none; 
    #                     border-radius:8px; 
    #                     margin-top: 3px;
    #                 }
    #                 QPushButton:hover {
    #                     background-color: #58D5F1;
    #                 }
    # """
    edit_btn_action = """QPushButton {
                        background:#fa0; 
                        padding:5px; 
                        margin-bottom:5px;
                        color:#fff;
                        font-size:13px; 
                        font-weight: 500;
                    }
                    QPushButton:hover {
                        background-color: #9A711E;
                    }
    """

    prev_btn = """QPushButton {
                        background:#00b894; 
                        padding:5px; 
                        color:#fff;
                        font-size:13px; 
                        font-weight: 500;
                    }
                    QPushButton:hover {
                        background-color: #0b8a71;
                    }
    """

    next_btn = """QPushButton {
                        background:#ff7675; 
                        padding:5px; 
                        color:#fff;
                        font-size:13px; 
                        font-weight: 500;
                    }
                    QPushButton:hover {
                        background-color: #cc6362;
                    }
    """
    
    detail_btn_action = """QPushButton {
                        background:#ff7675; 
                        padding:5px; 
                        margin-bottom:5px;
                        color:#fff;
                        font-size:13px; 
                        font-weight: 500;
                    }
                    QPushButton:hover {
                        background-color: #FF5A59;
                    }
    """

    del_btn_action = """QPushButton {
                        background:#ff3d71; 
                        padding:5px;
                        color:#fff;
                        font-size:13px; 
                        font-weight: 500;
                    }
                    QPushButton:hover {
                        background-color: #951C3C;
                    }
    """
    
    print_btn_action = """QPushButton {
                        background:#36f; 
                        padding:12px;
                        color:#fff;
                        font-size:13px; 
                        font-weight: 500;
                        margin-top: 50px;
                        border-radius: 8px;
                    }
                    QPushButton:hover {
                        background-color: #4B78FF;
                    }
    """

    # del_btn_action = """QPushButton {
    #                     background-color: #FFE4DE; 
    #                     color: #fff; 
    #                     font-weight:500; 
    #                     font-size: 14px; 
    #                     border-radius:8px; 
    #                     border:none; 
    #                     margin-top: 3px; 
    #                     margin-left:3px;
    #                 }
    #                 QPushButton:hover {
    #                     background-color: #f88369;
    #                 }
    # """

    login_button ="""QPushButton {
                    height:45px; 
                    background-color: #50cedd; 
                    color:#fff; 
                    border:none;
                }
                QPushButton:hover {
                    background-color: #4CB0BC;
    """

    logout_button = """QPushButton {
                        background-color:#FF7B7B; 
                        color:#fff; 
                        border:none;
                        padding: 8px;

                        font-family: Helvetica;
                        font-size: 13px;
                        font-weight: 600;
                    }

                    QPushButton:hover {
                        background-color: #ED7575;
                    }
    """

    emergency_button = """QPushButton {
                        background-color:#FF7B7B; 
                        color:#fff; 
                        font-weight:600; 
                        margin-left:60px; 
                        margin-right:60px;
                        border:none;

                        font-family: Helvetica;
                        font-size: 18px;
                        font-weight: 500;
                    }

                    QPushButton:hover {
                        background-color: #ED7575;
    """

    # primary label
    primary_lbl = """QLabel{
                        font-family: Helvetica;
                        font-size: 13px;
                        font-weight:600;
                        margin-bottom: 5px;
                        color: #fff;
    """
    
    primary_radio = """QRadioButton{
                        font-family: Helvetica;
                        font-size: 13px;
                        font-weight:600;
                        margin-bottom: 5px;
                        color: #fff;
    """
    
    primary_checkbox = """QCheckBox{
                        font-family: Helvetica;
                        font-size: 13px;
                        font-weight:600;
                        margin-bottom: 5px;
                        color: #fff;
    """
    
    detail_lbl = """QLabel{
                        font-family: Helvetica;
                        font-size: 12px;
                        font-weight:400;
                        margin-bottom: 20px;
                        color: #fff;
    """

    primary_lbl_kasir = """QLabel{
                        font-family: Helvetica;
                        font-size: 13px;
                        font-weight:600;
                        margin-bottom: 5px;
                        /*background:#2C3E50;*/
                        color: #fff;
                        padding:8px;               
    """
    
    
    # success label
    success_lbl = """QLabel{
                        font-family: Helvetica;
                        font-size: 13px;
                        padding: 5px;
                        color: #fff;
                        font-weight: 500;
                        background-color: #0CD0AA;
                                     
    """
    
    # lineedit styling
    primary_input = """QLineEdit{
                        height:30px; 
                        border:1px solid #dfe6e9;
                        background-color: #dfe6e9;
                        color: #000;
                        font-family: Helvetica;
                        font-size: 14px;
    """
    
    primary_spinbox = """QSpinBox{
                        height:30px; 
                        border:1px solid #dfe6e9;
                        background-color: #dfe6e9;
                        color: #000;
                        font-family: Helvetica;
                        font-size: 14px;
    """
    
    primary_date = """QCalendarWidget QTableView {
                        background-color: white;
                    }
                    QDateEdit{
                        height:30px; 
                        border:1px solid #dfe6e9;
                        background-color: #dfe6e9;
                        color: #000;
                        font-family: Helvetica;
                        font-size: 14px;
                    
                    
    """


    primary_spinbox = """QSpinBox{
                        height:30px; 
                        border:1px solid #dfe6e9;
                        background-color: #dfe6e9;
                        color: #000;
                        font-family: Helvetica;
                        font-size: 14px;
                                           
    """
    
    # comboBox styling
    primary_combobox = """
                        QComboBox QAbstractItemView {
                            background: #fff;
                        }
                        QComboBox{
                            height:40px; 
                            background-color: blue;
                            selection-background-color: #192038;
                            color: #fff;
                            font-family: Helvetica;
                            font-size: 14px;
    """
    
    # groupBox styling
    gb_styling = """QGroupBox { 
                        font-size: 14px; 
                        font-weight:600;
                        /*border: 1px solid #D3D3D3;*/ 
                        border-radius: 6px; 
                        margin-top: 6px; 
                        background-color: #222B45; 
                        padding-left:15px; 
                        padding-right:15px;
                    } 
                    QGroupBox::title { 
                        subcontrol-origin: margin; 
                        left: 8px; 
                        padding: 5px 5px 10px 5px; 
                        color:#fff; 
                        background-color:#e74c3c;
    """
    
    filter_gb_styling = """QGroupBox { 
                        font-size: 14px; 
                        border: 1px solid #394245; 
                        margin-top: 6px; 
                        padding-left:15px; 
                        padding-right:15px;
                    
    """

    tbl_font_weight = ""
    os_name = os.name
    
    if os_name == 'posix':
        tbl_font_weight = "400"      
    elif os_name == 'nt':
        tbl_font_weight = "500"

    table_style = """
                            QTableView {
                                background-color: white;
                                color: black;
                                gridline-color: #e0e0e0;
                                selection-background-color: #008080;
                                selection-color: white;
                                border: none;
                                font-size: 13px; 
                                font-weight:"""+tbl_font_weight+""";
                            }
                            QTableView::item:selected{ background-color: #00A3A3; }

                            QHeaderView{
                                background-color: #008080;
                                color:#fff;
                                font-size:14px; 
                                font-weight: 500;
                            }
                            QTableView QTableCornerButton::section {
                                background-color: #008080;
                            }
                            QHeaderView::section {
                                background-color: #008080;
                                color: white;
                                padding: 4px;
                            }
                            """

   
    def __init__(self) -> None:
        ...

    # def Show():
    #     ...
    
    def Position():
        ...
    
    def Size():
        ...
    
    def Style():
        ...

    def fontStyle(self, fontFamily:str, point:int, weight:int):
        font = QFont( fontFamily )
        font.setPointSize( point )
        font.setWeight( weight )

        return font

    def ScreenSize(self, app):
        # get available screen geometry        
        screen = app.primaryScreen()
        rect = screen.availableGeometry()
        
        return rect.width(), rect.height()

    def GetCenterHorizontal(self, screenWidth, windowWidth):
        center_horizontal = int((screenWidth/2)-(windowWidth/2))
        return center_horizontal
    
    def GetCenterVertical(self, screenHeight,windowHeight):
        center_vetical = int((screenHeight/2)-(windowHeight/2))    
        return center_vetical

class EventBinder(QObject):

    def __init__(self, target, event_target):
        super().__init__(target)
        self._target = target
        self.eventTarget = event_target
        self.target.installEventFilter(self)
    
    @property
    def target(self):
        return self._target

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress and source is self.target:
            if event.key() == Qt.Key_Return and self.target.hasFocus():
                print('Enter pressed')
                self.eventTarget()

        return super().eventFilter(source, event)

class Util(Controller ):
    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        super().__init__()
        
        self.screenSize = self.ScreenSize(self.app)
        self.components = {}
        self.container_lay = None
        self.mdi_stat = False
        
        # ========== steps ========
        self.logger.info("\nUtil constructor: ")
        self.logger.info("run QApplication .......")
        self.logger.info("init screensize .......")
        self.logger.info("init components dict .......\n")

     

    def setCenter(self, window_reference, screen_size:tuple, window_size:tuple):
        center_horizontal = self.GetCenterHorizontal(screen_size[0], window_size[0])
        center_vetical = self.GetCenterVertical(screen_size[1], window_size[1])
        
        window_reference.move(center_horizontal, center_vetical);
        window_reference.setFixedSize(window_size[0], window_size[1]);

    def WindowMethods( self, window_reference, method_name, params):
        
        # method is all setter type
        try:
            match method_name:
                case "title":
                    window_reference.setWindowTitle(params)    
                case "geometry":
                    window_reference.setGeometry(params[0], params[1], params[2], params[3])
                case "size":
                    if isinstance(params, tuple):
                        self.setCenter( window_reference, self.screenSize, params)

                case "style":

                    if "{" in params:
                        params = params + "}"

                    window_reference.setStyleSheet(params)
                case "scroll":
                    if(params):
                        self.scroll = QScrollArea()             
                        self.scroll.setWidget(window_reference)
                    
                case default:
                    pass
        except Exception as e:
            self.logger.error(str(e))


    def CreateWindow(self, setters, window, type=""):
        
        # set default window size fullscreen
        self.setCenter( window, self.screenSize, self.screenSize)
        
        if(type==""):
            # loop setters dictionary above
            for key, value in setters.items():
                self.WindowMethods(window, key, value)

            return window

        elif(type=="mdi"):

            self.mdi = QMdiArea(window)
            window.setCentralWidget(self.mdi)
            
            sub = QMdiSubWindow()
            
            # set default sub window full screen
            self.setCenter( sub, self.screenSize, self.screenSize)

            for key, value in setters.items():
                self.WindowMethods(sub, key, value)

            self.mdi.addSubWindow(sub)
            return sub
        
        elif(type=="add-mdi"):

            # mdi = QMdiArea(window)
            window.setCentralWidget(self.mdi)
            
            sub = QMdiSubWindow()
            
            # set default sub window full screen
            self.setCenter( sub, self.screenSize, self.screenSize)

            for key, value in setters.items():
                self.WindowMethods(sub, key, value)

            self.mdi.addSubWindow(sub)
            return sub
        

    def closeWindow(self, windowTarget):
        windowTarget.close()

        # reset window object from child class
        self.window = QMainWindow()     

    def createMenuBar(self, menus):
        
        bar = self.window.menuBar()
        
        # for key,value in i.items():
        add_stat = False
        for m in menus:
            for key,val in m.items():
                
                if add_stat == False:
                    main = bar.addMenu(key)
                    main.triggered[QAction].connect(self.windowBarAction)

                    add_stat=True
                
                if isinstance(val, str):
                    main.addAction(val)
                elif isinstance(val, tuple):
                    for x in range( len(val) ):
                        main.addAction(val[x])

                
            add_stat=False

    def CreateContainer(self, layout):
        wgt = QWidget()
        wgt.setLayout(layout)

        return wgt,layout
    
    def CreateLayout(self, params:tuple, parent=None):
        # create layout & check if scroll true/false
        tuple_length = len(params)
        lay = params[0].lower()
        init_layout = None
        scroll = None

        if( lay == "vboxlayout"):
            init_layout = QVBoxLayout()
        elif( lay == "hboxlayout"):
            init_layout = QHBoxLayout()
        elif( lay == "gridlayout"):
            init_layout = QGridLayout()
        elif( lay == "stackedlayout"):
            init_layout = QStackedLayout()
        elif( lay == "formlayout"):
            init_layout = QFormLayout()

        if tuple_length==2:
            if(params[1]):

                widget = QWidget()
                scroll = QScrollArea() 
                widget.setLayout(init_layout)
                scroll.setWidget(widget)
                scroll.setWidgetResizable(True)
                scroll.setMinimumWidth(100)

                parent.setWidget(scroll)

        return init_layout

    def CreateComponentLayout(self, components:list, layout, layout_type:str="" ):
        
        if layout_type == "":
            for i in components:
                
                if ("name" in i and i["name"] != "") and ("category" in i and i["category"] != "") :
                    self.CreateComponent([i])
                    layout.addWidget( self.components[i["name"]] )

                else:
                    self.logger.info("name - category not available/empty")
                    sys.exit()

        elif layout_type.lower() == "formlayout":
            
            for i in components:

                # check if component has name and category key
                if (("name" in i[0] and i[0]["name"] != "" and 
                    "name" in i[1] and i[1]["name"] != "") and 
                   ("category" in i[0] and i[0]["category"] != "" and 
                   "category" in i[1] and i[1]["category"] != ""
                   )):

                        # CreateComponent() --> argument must in list
                        self.CreateComponent( [i[0]] )
                        self.CreateComponent( [i[1]] )
                        layout.addRow(self.components[i[0]["name"]], self.components[i[1]["name"]])

                else:
                    self.logger.info("name - category not available/empty")
                    sys.exit()

    def CreateComponent(self, components:list, parent=None ):
        
        for i in components:
            
            if ("name" in i and i["name"] != "") and ("category" in i and i["category"] != "") :
                
                # pengecekan nama komponenen tidak boleh sama, penting dilakukan saat
                # 2 dua subwindow bekerja secara berdampingan, maka ini akan menyebabkan konflik

                # if i["name"] in self.components:
                #     print(i["name"], " => Component name has already exist")
                #     sys.exit()

                # create element object save to self.components dictionary, based on category
                match i["category"].lower():
                    case "label":
                        self.components[i["name"]] = QLabel(parent)
                    case "image":
                        self.components[i["name"]] = QLabel(parent)
                    case "pushbutton":
                        self.components[i["name"]] = QPushButton(parent)
                        self.components[i["name"]].setCursor(QCursor(Qt.PointingHandCursor))
                    case "checkbox":
                        self.components[i["name"]] = QCheckBox(parent)
                    case "combobox":
                        self.components[i["name"]] = QComboBox(parent)
                    case "spinbox":
                        self.components[i["name"]] = QSpinBox(parent)
                    case "lineedit":
                        self.components[i["name"]] = QLineEdit(parent)
                    case "lineeditpassword":
                        self.components[i["name"]] = QLineEdit(parent)
                        self.components[i["name"]].setEchoMode(QLineEdit.Password)
                    case "lineeditint":
                        self.components[i["name"]] = QLineEdit(parent)
                        self.components[i["name"]].setValidator(QDoubleValidator())

                    case "date":
                        self.components[i["name"]] = QDateEdit(parent)
                        self.components[i["name"]].setDisplayFormat("yyyy-MM-dd")
                        self.components[i["name"]].setMinimumDate(QDate.currentDate())
                        self.components[i["name"]].setCalendarPopup(True)

                    case "radiobutton":
                        self.components[i["name"]] = QRadioButton(parent)
                        
                    case "groupbox":
                        self.components[i["name"]] = QGroupBox(parent)
                    
                    case "widget":
                        # create a container
                        self.components[i["name"]] = QWidget()

                    case default:
                        pass
                
                for key,value in i.items():
                    if(key != "name" and key != "category"):
                        match key.lower():
                            case "move":
                                self.components[i["name"]].move( i["move"][0], i["move"][1] )
                            case "text":
                                self.components[i["name"]].setText( i["text"] )
                            case "img_path":

                                # default pixmap set 
                                pixmap = QPixmap(640, 358)
                                
                                if i["img_path"] != "":
                                    pixmap = QPixmap(i["img_path"])
                                
                                self.components[i["name"]].setPixmap(pixmap)
                            case "editable":
                                if i["editable"] == False:
                                    self.components[i["name"]].setReadOnly(True)    
                            case "title":
                                self.components[i["name"]].setTitle( i["title"] )
                            case "min_height":
                                self.components[i["name"]].setMinimumHeight( i["min_height"] )
                            case "min_width":
                                self.components[i["name"]].setMinimumWidth( i["min_width"] )
                            case "max_height":
                                self.components[i["name"]].setMaximumHeight( i["max_height"] )
                            case "max_width":
                                self.components[i["name"]].setMaximumWidth( i["max_width"] )
                            case "maximum_size":
                                self.components[i["name"]].setMaximumSize( i["maximum_size"][0], i["maximum_size"][1] )
                            case "move":
                                self.components[i["name"]].move( i["move"][0], i["move"][1] )
                            case "style":
                                style = i["style"]

                                if "{" in style:
                                    style = style + "}"

                                self.components[i["name"]].setStyleSheet( style )
                            case "font":
                                font = QFont( i["font"][0] )
                                font.setPointSize( i["font"][1] )
                                font.setWeight( i["font"][2] )

                                self.components[i["name"]].setFont( font )
                            case "clicked":
                                method_name = i["clicked"]["method_name"]
                                
                                if "arguments" in i["clicked"]:
                                    self.components[i["name"]].clicked.connect( lambda: method_name(i["clicked"]["arguments"]) )
                                elif "arguments" not in i["clicked"]:
                                    self.components[i["name"]].clicked.connect( method_name )
                            
                            case "event":
                                method_name = i["event"]["method_name"]
                                
                                if "arguments" in i["event"]:
                                    arg = i["event"]["arguments"]
                                    EventBinder(self.components[i["name"]], lambda: method_name(arg) )
                                elif "arguments" not in i["event"]:
                                    EventBinder(self.components[i["name"]], method_name )
                                                           

                            case "items":
                                self.components[i["name"]].addItems(i["items"])

                            case "selected_item":
                                combo_box = self.components[i["name"]]
                                combo_box.setCurrentText( i["selected_item"] )
                            
                            case "checked":
                                if i["checked"]:
                                    self.components[i["name"]].setChecked(True)

                            case "toggled":
                                method_name = i["toggled"]["method_name"]
                                self.components[i["name"]].clicked.connect( lambda: method_name( self.components[i["name"]] ) )

                            case "value":
                                self.components[i["name"]].setValue( int(i["value"]) )
                            
                            case "range":
                                n1,n2 = i["range"]
                                self.components[i["name"]].setRange(n1,n2)

                            case "reg_date":
                                ds = i["reg_date"].split("-")
                                self.components[i["name"]].setDate( QDate(int(ds[0]), int(ds[1]), int(ds[2])) )

                            case "layout":
                                self.container_lay = self.CreateLayout ( (i["layout"], False) )

                            case "children":
                                # set layout for widget container
                                self.components[i["name"]].setLayout( self.container_lay )

                                # self.CreateComponent(value, self.components[i["name"]])
                                self.CreateComponentLayout( value, self.components[i["name"]].layout() )

            else:
                self.logger.info("name - category not available/empty")
                sys.exit()


    def SubWinVerticalForm(self, sub_window_setter:dict, components_setter:list, type=""):
        # create subwindows
        if type == "":
            sub = self.CreateWindow(sub_window_setter, self.window, "mdi")
        elif type == "add-mdi":
            sub = self.CreateWindow(sub_window_setter, self.window, "add-mdi")
        
        
        # create layout for sub windows
        sub_lay = self.CreateLayout(("VBoxLayout", True), sub)
        sub_lay.setContentsMargins(20,0,20,0)
        # sub_lay.setSpacing(0)
        
        sub_lay.addStretch(1)
        self.CreateComponentLayout(components_setter, sub_lay)
        sub_lay.addStretch(1)

        # show subwindows
        sub.show()

    def SubWinVerticalTable(self, sub_window_setter:dict, widgets:list):
        # create subwindows
        sub = self.CreateWindow(sub_window_setter, self.window, "mdi")
        
        # create layout for sub windows
        sub_lay = self.CreateLayout(("VBoxLayout", True), sub)
        sub_lay.setContentsMargins(20,0,20,0)
        
        # sub_lay.addStretch(1)
        
        # add widgets into layout
        for w in widgets:
            sub_lay.addWidget(w)

        sub_lay.addStretch(1)

        # show subwindows
        sub.show()

    def getPath(self,fileName):
        path = os.path.dirname(os.path.realpath(__file__))
        
        return '/'.join([path, fileName])

    def getComboIndex(self, combo, txt):
        index = combo.findText(txt, Qt.MatchFixedString)
        if index >= 0:
            return index
            # combo.setCurrentIndex(index)

    def eventFilter(self, component, obj, event):
        if event.type() == QEvent.KeyPress and obj is self.text_box:
            if event.key() == Qt.Key_Return and self.text_box.hasFocus():
                print('Enter pressed bawah')
        return super().eventFilter(obj, event)
