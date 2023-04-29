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









import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.label1 = QLabel('Label 1')
        self.label2 = QLabel('Label 2')
        self.btn_replace = QPushButton('Replace')

        # ==> main_kendaraan widget as main container
        self.container_wgt =QWidget()

        self.win_lay = QVBoxLayout()
        self.container_lay = QVBoxLayout()


        self.setLayout(self.win_lay)

        self.win_lay.addWidget( self.container_wgt )

        self.container_wgt.setLayout( self.container_lay )
        
        self.container_lay.addWidget(self.label1)
        self.container_lay.addWidget(self.label2)
        self.container_lay.addWidget(self.btn_replace)
        
        self.container_lay.addStretch(1)
        # self.setLayout(self.vbox)

        self.btn_replace.clicked.connect(self.replace_label)

    def replace_label(self):
        self.container_wgt.deleteLater()

        self.win_lay.addWidget( self.container_wgt )

        # self.label2.deleteLater()
        # self.label2 = None
        

        self.label3 = QLabel('Label 3')
        self.win_lay.addWidget( self.label3 )

        # # self.vbox.removeWidget( self.label1 )
        # self.vbox.addWidget( self.label3 )
        # self.layout().removeWidget(self.label1)
        
        # self.label1.deleteLater()
        # self.label1 = None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
