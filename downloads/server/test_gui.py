import sys
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QStackedWidget, QTabWidget, QPushButton, QLabel

class SampleWindow:
    def __init__(self):
        self.win = QMainWindow()

        self.win.setWindowTitle("QStackedWidget with QPropertyAnimation")
        self.win.setFixedSize(500, 400)

        central = QWidget()
        layout = QVBoxLayout()
        central.setLayout(layout)
        
        self.win.setCentralWidget(central)
        # Create the layout

        
        # Create the stacked widget
        # self.stacked_widget = QTabWidget()
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)
        self.stacked_widget.setStyleSheet("background: green;")
        
        lbl1 = QLabel("test lbl 1")
        lbl2 = QLabel("test lbl 2")
        
        # self.stacked_widget.addTab(lbl1, "Tab 1")
        # self.stacked_widget.addTab(lbl2, "Tab 2")

        self.stacked_widget.addWidget(lbl1)
        self.stacked_widget.addWidget(lbl2)

        # self.anim = QPropertyAnimation(self.stacked_widget, b"minimumWidth")
        self.anim = QPropertyAnimation(self.stacked_widget, b"geometry")
        
        

        # Create the first tab widget
        # tab1 = QTabWidget()
        # tab1.addTab(QLabel("Tab 1 - Page 1"), "Page 1")
        # tab1.addTab(QLabel("Tab 1 - Page 2"), "Page 2")
        
        # # Create the second tab widget
        # tab2 = QTabWidget()
        # tab2.addTab(QLabel("Tab 2 - Page 1"), "Page 1")
        # tab2.addTab(QLabel("Tab 2 - Page 2"), "Page 2")
        
        # Add the tab widgets to the stacked widget
        # self.stacked_widget.addWidget(tab1)
        # self.stacked_widget.addWidget(tab2)
        
        
        
        # # Create buttons to change the stacked widget
        btn1 = QPushButton("Tab 1")
        btn1.clicked.connect(lambda: self.change_stacked_widget(0))
        layout.addWidget(btn1)
        
        btn2 = QPushButton("Tab 2")
        btn2.clicked.connect(lambda: self.change_stacked_widget(1))
        layout.addWidget(btn2)
        
        # # Set the layout
        # self.setLayout(layout)
        self.win.show()
    
    def change_stacked_widget(self, index):
        self.anim.setDuration(400)
        self.anim.setStartValue(QRect(0,0, 0, 0))
        self.anim.setEndValue(QRect(0,0, 200, 200))
        self.anim.setEasingCurve(QEasingCurve.InOutQuart)
        self.anim.start()
        print("masuk")

        # self.anim.setDuration(400)
        # self.anim.setStartValue(100)
        # self.anim.setEndValue(250)
        # self.anim.setEasingCurve(QEasingCurve.InOutQuart)
        # self.anim.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wind = SampleWindow()
    # wind.show()
    sys.exit(app.exec_())

    # https://stackoverflow.com/questions/60476632/qtabwidget-access-actual-tab-not-the-content-widget
    # https://stackoverflow.com/questions/6952852/qpropertyanimation-doesnt-work-with-a-child-widget
