import sys
from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QStackedWidget, QTabWidget, QPushButton, QLabel

class SampleWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QStackedWidget with QPropertyAnimation")
        
        # Create the layout
        layout = QVBoxLayout()
        
        # Create the stacked widget
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)
        
        # Create the first tab widget
        tab1 = QTabWidget()
        tab1.addTab(QLabel("Tab 1 - Page 1"), "Page 1")
        tab1.addTab(QLabel("Tab 1 - Page 2"), "Page 2")
        
        # Create the second tab widget
        tab2 = QTabWidget()
        tab2.addTab(QLabel("Tab 2 - Page 1"), "Page 1")
        tab2.addTab(QLabel("Tab 2 - Page 2"), "Page 2")
        
        # Add the tab widgets to the stacked widget
        self.stacked_widget.addWidget(tab1)
        self.stacked_widget.addWidget(tab2)
        
        # Create buttons to change the stacked widget
        btn1 = QPushButton("Tab 1")
        btn1.clicked.connect(lambda: self.change_stacked_widget(0))
        layout.addWidget(btn1)
        
        btn2 = QPushButton("Tab 2")
        btn2.clicked.connect(lambda: self.change_stacked_widget(1))
        layout.addWidget(btn2)
        
        # Set the layout
        self.setLayout(layout)
    
    def change_stacked_widget(self, index):
        animation = QPropertyAnimation(self.stacked_widget, b"maximumWidth")
        animation.setDuration(1000)
        animation.setStartValue(0)
        animation.setEndValue(self.width())
        animation.start()
        self.stacked_widget.setCurrentIndex(index)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = SampleWindow()
    win.show()
    sys.exit(app.exec_())

    # https://stackoverflow.com/questions/60476632/qtabwidget-access-actual-tab-not-the-content-widget
    # https://stackoverflow.com/questions/6952852/qpropertyanimation-doesnt-work-with-a-child-widget
