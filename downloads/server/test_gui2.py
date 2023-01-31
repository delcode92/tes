import sys
from PyQt5.QtWidgets import QStackedWidget,QVBoxLayout,QMainWindow, QWidget, QApplication
from PyQt5.QtCore import QRect, QPropertyAnimation, QPoint, QEasingCurve

class Window:
    def __init__(self):
        # super().__init__()
        self.win = QMainWindow()

        self.win.setWindowTitle("QStackedWidget with QPropertyAnimation")
        self.win.setFixedSize(500, 400)

        central = QWidget()
        layout = QVBoxLayout()
        central.setLayout(layout)
        
        self.win.setCentralWidget(central)

        self.child = QWidget()
        self.child.setStyleSheet("background-color:red;border-radius:15px;")
        
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background: green;")
        layout.addWidget(self.stacked_widget)
        
        # self.stacked_widget.addWidget(self.child)
        # self.child.resize(100, 100)
        
        self.win.show()

        self.anim = QPropertyAnimation(self.stacked_widget, b"geometry")
        
        self.anim.setEasingCurve(QEasingCurve.InOutQuart)
        
        self.anim.setStartValue(QRect(0,0, 0, 0))
        self.anim.setEndValue(QRect(0,0, 200, 200))
        self.anim.setDuration(1500)
        self.anim.start()


app = QApplication(sys.argv)
w = Window()
sys.exit(app.exec_())
