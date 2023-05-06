from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QShortcut
from PyQt5.QtGui import QKeySequence
import sys


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the layout
        layout = QVBoxLayout()
        label = QLabel("Press 'Ctrl+X' or 'Ctrl+Y' to trigger a method")
        layout.addWidget(label)
        self.setLayout(layout)

        # Create the shortcuts
        shortcut_x = QShortcut(QKeySequence("Ctrl+X"), self)
        shortcut_y = QShortcut(QKeySequence("Ctrl+Y"), self)

        # Connect the shortcuts to methods
        shortcut_x.activated.connect(self.method_x)
        shortcut_y.activated.connect(self.method_y)

    def method_x(self):
        print("Method X triggered")

    def method_y(self):
        print("Method Y triggered")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec_())
