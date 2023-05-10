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

import json, math

rules = json.loads( '{"0" : "1000", "4":"1500", "10":"1500", "16":"1500", "24":"5500"}' )
els = list(rules.items()) 

# key,value = next( iter(rules.items()) )
# last_key,last_value = rules.popitem()
lk,lv = els[-1]

print("els len: ", len(els))
print(lk, lv)
# print(last_key, last_value)

# print(math.floor(10/3))

# dict1 = {"key1": "value1", "key2": "value2", "key3": "value3"}
# dict2 = {"key4_1": "value4_1", "key5_1": "value5_1"}

# dict1.update(dict2)
# # dict1[list(dict1.keys())[-1]] = dict1.pop(list(dict1.keys())[-1])

# print(dict1)
