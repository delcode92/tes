import sys
from PyQt5.QtWidgets import QApplication, QWidget, QRadioButton, QHBoxLayout


class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):
        # Create the radio buttons
        self.rb1 = QRadioButton('Button 1')
        self.rb2 = QRadioButton('Button 2')
        self.rb3 = QRadioButton('Button 3')
        
        # Create a horizontal layout to add the radio buttons
        hbox = QHBoxLayout()
        hbox.addWidget(self.rb1)
        hbox.addWidget(self.rb2)
        hbox.addWidget(self.rb3)
        
        # Set the layout for the window
        self.setLayout(hbox)
        
        # Connect the radio buttons
        # self.rb1.toggled.connect(self.onRadioButtonToggle)
        # self.rb2.toggled.connect(self.onRadioButtonToggle)
        # self.rb3.toggled.connect(self.onRadioButtonToggle)
        
        # Set the window properties
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Radio Buttons')
        self.show()
        
        
    def onRadioButtonToggle(self):
        # Get the radio button that was toggled
        radioButton = self.sender()
        
        # If the radio button is checked, print its text
        if radioButton.isChecked():
            print(radioButton.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
