import sys,cv2,os
# from client.client_service import Client
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QPushButton, QAction,
QLineEdit, QCheckBox, QGroupBox, QComboBox, QRadioButton, QScrollArea, QMdiArea, QMdiSubWindow, QVBoxLayout, QFormLayout, QHBoxLayout, QGridLayout, QStackedLayout
)

from PyQt5.QtGui import QImage, QPixmap, QFont, QCursor
from PyQt5.QtCore import QThread, Qt, QCoreApplication, pyqtSignal, pyqtSlot

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

    # button styling
    primary_button ="""QPushButton {
                    margin-top:60px; 
                    height:45px; 
                    background-color: #50cedd; 
                    color:#fff; 
                    border:none;

                    font-family: Helvetica;
                    font-size: 18px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #4CB0BC;
    """

    edit_btn_action = """QPushButton {
                        background-color:#DDF9FF; 
                        color: #fff; 
                        font-weight:500; 
                        font-size: 14px; 
                        border:none; 
                        border-radius:8px; 
                        margin-top: 3px;
                    }
                    QPushButton:hover {
                        background-color: #58D5F1;
                    }
    """

    del_btn_action = """QPushButton {
                        background-color: #FFE4DE; 
                        color: #fff; 
                        font-weight:500; 
                        font-size: 14px; 
                        border-radius:8px; 
                        border:none; 
                        margin-top: 3px; 
                        margin-left:3px;
                    }
                    QPushButton:hover {
                        background-color: #f88369;
                    }
    """

    login_button ="""QPushButton {
                    height:45px; 
                    background-color: #50cedd; 
                    color:#fff; 
                    border:none;
                }
                QPushButton:hover {
                    background-color: #4CB0BC;
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
                        font-size: 16px;
                        background-color: #fff;                  
    """
    
    
    # success label
    success_lbl = """QLabel{
                        font-family: Helvetica;
                        font-size: 18px;
                        padding: 6px;
                        color: #fff;
                        font-weight: 500;
                        background-color: #0CD0AA;
                                     
    """
    
    # lineedit styling
    primary_input = """QLineEdit{
                        height:40px; 
                        border:1px solid #ecf0f1;
                        background-color: #f4f4f4;

                        font-family: Helvetica;
                        font-size: 14px;
    """
    
    # comboBox styling
    primary_combobox = """QComboBox{
                        height:40px; 
                        border:1px solid #ecf0f1;
                        background-color: #f4f4f4;

                        font-family: Helvetica;
                        font-size: 14px;
    """
    
    # groupBox styling
    gb_styling = """QGroupBox { 
                        font-size: 14px; 
                        font-weight:600;
                        border: 1px solid #D3D3D3; 
                        border-radius: 6px; 
                        margin-top: 6px; 
                        background-color: #FFFFFF; 
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

    table_style = """QTableView {
                        border: 1px solid #30c2a5;
                        border-radius: 5px;

                        padding: 0;
                        font-family: sans-serif;
                        font-size: 14px;
                        background-color: #fff;
                        margin-top: 40px;
                        min-height: 700px;
                    }

                    
                    QTableView QTableCornerButton::section {
                        background-color: #30c2a5;
                        border: none;
                    }
                    
                    QHeaderView{
                        background-color: #30c2a5;
                        margin:0;
                        padding: 0;
                    }
                    QHeaderView::section {
                        background-color: #30c2a5;
                        border:1px solid #75d6c3;
                        font-size: 16px;
                        font-weight:600;
                        font-size: 15px;
                        text-align: left;
                        color: #fff;
                        padding: 6px ;
                        margin:0;
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

class Util(Controller):
    def __init__(self) -> None:
        super().__init__()
          
        self.app = QApplication(sys.argv)
        
        self.screenSize = self.ScreenSize(self.app)
        self.components = {}
        self.mdi_stat = False
        
        # ========== steps ========
        print("\nUtil constructor: ")
        print("run QApplication .......")
        print("init screensize .......")
        print("init components dict .......\n")
        
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
                    # if isinstance(params, str) and params.lower()=="fullscreen":
                    #     print( "from window method ",window_reference, self.screenSize, self.screenSize)
                    #     self.setCenter( window_reference, self.screenSize, self.screenSize)
                    
                    if isinstance(params, tuple):
                        self.setCenter( window_reference, self.screenSize, params)

                case "style":

                    if "{" in params:
                        params = params + "}"

                    window_reference.setStyleSheet(params)
                case "scroll":
                    if(params):
                        print("ok")
                        self.scroll = QScrollArea()             
                        self.scroll.setWidget(window_reference)
                    
                case default:
                    pass
        except Exception as e:
            print(e)


    def CreateWindow(self, setters, window, type=""):
        
        # set default window size fullscreen
        self.setCenter( window, self.screenSize, self.screenSize)
        
        if(type==""):
            # loop setters dictionary above
            for key, value in setters.items():
                self.WindowMethods(window, key, value)

            return window

        elif(type=="mdi"):

            # ======== old code ===========
            # if(self.mdi_stat==False):
            #     self.mdi = QMdiArea(window)
            #     window.setCentralWidget(self.mdi)
            #     self.mdi_stat = True
            # ==============================

            #dengan membuat qmdiarea yg baru maka secara otomatis
            # semua sub window pada mdi area yg lama akan dihapus secra otomatis
            # artinya mdi area kan selalu bersih dari sub window 
            
            self.mdi = QMdiArea(window)
            window.setCentralWidget(self.mdi)
            # self.mdi_stat = True

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
                    print("name - category not available/empty")
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
                    print("name - category not available/empty")
                    sys.exit()

    def CreateComponent(self, components:list, parent=None ):
        
        for i in components:
            
            if ("name" in i and i["name"] != "") and ("category" in i and i["category"] != "") :
                
                # pengecekan nama komponenen tidak boleh sama, penting dilakukan saat
                # 2 dua subwindow bekerja secara berdampingan, maka ini akan menyebabkan konflik

                # if i["name"] in self.components:
                #     print(i["name"], " => Component name has already exist")
                #     sys.exit()

                # create element object save to self.componenets dictionary, based on category
                match i["category"].lower():
                    case "label":
                        self.components[i["name"]] = QLabel(parent)
                    case "pushbutton":
                        self.components[i["name"]] = QPushButton(parent)
                        self.components[i["name"]].setCursor(QCursor(Qt.PointingHandCursor))
                    case "checkbox":
                        self.components[i["name"]] = QCheckBox(parent)
                    case "combobox":
                        self.components[i["name"]] = QComboBox(parent)
                    case "lineedit":
                        self.components[i["name"]] = QLineEdit(parent)
                    case "lineeditpassword":
                        self.components[i["name"]] = QLineEdit(parent)
                        self.components[i["name"]].setEchoMode(QLineEdit.Password)
                    case "radiobutton":
                        self.components[i["name"]] = QRadioButton(parent)
                        
                    case "groupbox":
                        self.components[i["name"]] = QGroupBox(parent)

                    case default:
                        pass
                
                for key,value in i.items():
                    # print(key)
                    if(key != "name" and key != "category"):
                        match key.lower():
                            case "move":
                                self.components[i["name"]].move( i["move"][0], i["move"][1] )
                            case "text":
                                self.components[i["name"]].setText( i["text"] )
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
                            
                            case "items":
                                self.components[i["name"]].addItems(i["items"])
                            case "children":
                                self.CreateComponent(value, self.components[i["name"]])

            else:
                print("name - category not available/empty")
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