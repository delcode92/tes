# self.limit = 18
# self.offset = 0


# def updateLabel(self):
#         # start = 0 + 1
#         # start = 18 + 1
#         # start = 36 + 1
#         start = self.offset + 1
        
#         # min( 0 + 18, 51 )
#         # min( 18 + 18, 51 )
#         # min( 36 + 18, 51 )
#         end = min(self.offset + self.limit, len(self.data))
        
#         # total = 51
#         total = len(self.data)
#         self.label.setText("{}-{} from {} results".format(start, end, total))
        
# def nextPage(self):
#     # 1) 0 + 18 < 51
#     # 2) 18 + 18 < 51
#     # 2) 36 + 18 < 51
#     if self.offset + self.limit < len(self.data):
        
#         # self.offset = 0 + 18
#         # self.offset = 18 + 18
#         # self.offset = 36 + 18
#         self.offset += self.limit
#         self.updateTable()
#         self.updateLabel()
    
# def prevPage(self):
#     if self.offset > 0:
#         self.offset -= self.limit
#         self.updateTable()
#         self.updateLabel()


# l1 = [
#     {"k1":"v1"},
#     {"k2":"v2"},
#     {"k3":"v3"}
# ]

# new_list = [{"k0":"v0"}] + l1 + [{"k4":"v4"}]

# # print( new_list )

# components_setter = [{
#                         "name":"main_kendaraan",
#                         "category":"widget",
#                         "layout": "VBoxLayout",
#                         "max_width":700,
#                         "style":"style here",
#                         "children":[]
#                     }]

# components_setter[0]["children"] = new_list

# # print( components_setter[0]["children"] )

# l = []
# l = l+ [{"k1":"v1"}]
# l = l+ [{"k2":"v2"}]

# print( l )









# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QStackedWidget

# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()

#         self.initUI()

#     def initUI(self):
#         self.label1 = QLabel('Label 1-1')
#         self.label2 = QLabel('Label 1-2')
#         self.label3 = QLabel('Label 2-1')
#         self.label4 = QLabel('Label 2-2')
#         self.btn_replace = QPushButton('Replace')

#         self.Stack = QStackedWidget()

#         # ==> main_kendaraan widget as main container
#         self.container_wgt1 =QWidget()
#         self.container_wgt2 =QWidget()

#         self.win_lay = QVBoxLayout()
#         self.container_lay1 = QHBoxLayout()
#         self.container_lay2 = QHBoxLayout()


#         self.setLayout(self.win_lay)

#         self.win_lay.addWidget( self.Stack )
#         self.win_lay.addWidget( self.btn_replace )


#         self.container_wgt1.setLayout( self.container_lay1 )
#         self.container_wgt2.setLayout( self.container_lay2 )
        
#         self.container_lay1.addWidget(self.label1)
#         self.container_lay1.addWidget(self.label2)

#         self.container_lay2.addWidget(self.label3)
#         self.container_lay2.addWidget(self.label4)
        

#         self.Stack.addWidget( self.container_wgt1 )
#         self.Stack.addWidget( self.container_wgt2 )
        
#         self.Stack.setStyleSheet("border: 4px solid red;")
#         self.container_wgt1.setStyleSheet("border: 2px solid blue;")
#         self.container_wgt2.setStyleSheet("border: 2px solid yellow;")

#         self.Stack.setCurrentIndex(0) 

#         # self.container_lay.addWidget(self.btn_replace)
        
#         # self.container_lay.addStretch(1)
#         # # self.setLayout(self.vbox)

#         self.btn_replace.clicked.connect(self.replace_label)

#     def replace_label(self):
#         self.container_new = QWidget()
#         self.container_new_lay = QHBoxLayout()
#         self.container_new.setLayout( self.container_new_lay )
#         self.label5 = QLabel('Label next')
        
#         self.Stack.removeWidget( self.container_wgt1 )
#         print( "==>", self.Stack.count() )

#         self.container_new.setStyleSheet("background: grey;")
#         self.Stack.addWidget( self.container_new )
#         self.Stack.setCurrentIndex(1) 
#         # self.container_wgt.deleteLater()




#         # self.win_lay.addWidget( self.container_wgt )

#         # self.label2.deleteLater()
#         # self.label2 = None
        

#         # self.label3 = QLabel('Label 3')
#         # self.win_lay.addWidget( self.label3 )

#         # # self.vbox.removeWidget( self.label1 )
#         # self.vbox.addWidget( self.label3 )
#         # self.layout().removeWidget(self.label1)
        
#         # self.label1.deleteLater()
#         # self.label1 = None

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())

# import json, math

# rules = json.loads( '{"0" : "1000", "4":"1500", "10":"1500", "16":"1500", "24":"5500"}' )
# els = list(rules.items()) 

# # key,value = next( iter(rules.items()) )
# # last_key,last_value = rules.popitem()
# lk,lv = els[-1]

# print("els len: ", len(els))
# print(lk, lv)
# print(last_key, last_value)

# print(math.floor(10/3))

# dict1 = {"key1": "value1", "key2": "value2", "key3": "value3"}
# dict2 = {"key4_1": "value4_1", "key5_1": "value5_1"}

# dict1.update(dict2)
# # dict1[list(dict1.keys())[-1]] = dict1.pop(list(dict1.keys())[-1])

# print(dict1)

# start code
# from configparser import ConfigParser
# from framework import *

# class IPCam(Util, View):
#     img_name = ""

#     ####### get ipcam ip ########
#     ini = Util.getPath(None,fileName="app.ini")
        
#     configur = ConfigParser()
#     configur.read(ini)

#     jum_gate = 0
#     for i in range(8):
#         try:
#             n = i+1
#             ip = configur[f"gate{n}"]["ipcam1"]
#             ip2 = configur[f"gate{n}"]["ipcam2"]

#             jum_gate+=1
#         except:
#             break;

    
#     def __init__(self) -> None:
#         x = IPCam.jum_gate
#         self.methods = []

#         for i in range(IPCam.jum_gate):
#             method_name = f"initGate{i+1}"
#             method = getattr(self, method_name, None)
            
#             method()

        

#     def initGate1(self):
#         print("init gate1")
    
#     def initGate2(self):
#         print("init gate2")
    
#     def initGate3(self):
#         print("init gate3")
    
#     def initGate4(self):
#         print("init gate4")
    
#     def initGate5(self):
#         print("init gate5")
    
#     def initGate6(self):
#         print("init gate6")
    
#     def initGate7(self):
#         print("init gate7")
    
#     def initGate8(self):
#         print("init gate8")

# IPCam()

# end code



# importing libraries
# from PyQt5.QtWidgets import *
# from PyQt5 import QtCore, QtGui
# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
# import sys


# class Window(QMainWindow):

# 	def __init__(self):
# 		super().__init__()

# 		# setting title
# 		self.setWindowTitle("Python ")

# 		# setting geometry
# 		self.setGeometry(100, 100, 600, 400)

# 		# calling method
# 		self.UiComponents()

# 		# showing all the widgets
# 		self.show()

# 	# method for widgets
# 	def UiComponents(self):

# 		# creating a combo box widget
# 		self.combo_box = QComboBox(self)

# 		# setting geometry of combo box
# 		self.combo_box.setGeometry(200, 150, 120, 30)

# 		# geek list
# 		geek_list = ["Geek", "Geeky Geek", "Legend Geek", "Ultra Legend Geek"]

# 		# adding list of items to combo box
# 		self.combo_box.addItems(geek_list)

# 		# item
# 		item ="Legend Geek"

# 		# setting current item
# 		self.combo_box.currentText()


# # create pyqt5 app
# App = QApplication(sys.argv)

# # create the instance of our Window
# window = Window()

# # start the app
# sys.exit(App.exec())

import sys,re
# from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout, QLabel,QLineEdit


# class PopupWindow(QDialog):
#     def __init__(self, parent=None):
#         super().__init__(parent)
        
#         layout = QVBoxLayout()
#         label = QLabel("This is a popup window.")
#         n_input = QLineEdit()
#         layout.addWidget(label)
#         layout.addWidget(n_input)
        
#         self.setLayout(layout)
#         self.setWindowModality(Qt.ApplicationModal)
#         self.setWindowTitle("Popup Window")

#     def keyPressEvent(self, event):
#         if event.key() == Qt.Key_Escape:
#             self.close()


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("Main Window")
#         self.setGeometry(100, 100, 400, 300)

#     def keyPressEvent(self, event):
#         if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_N:
#             self.open_popup_window()

#     def open_popup_window(self):
#         popup_window = PopupWindow(self)
#         popup_window.exec_()


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())




gate_number = re.search('roller#(.+?)#end', 'roller#"2"#end').group(1)
print("==> gate number: ", gate_number)