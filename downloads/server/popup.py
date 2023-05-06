from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QPushButton, QVBoxLayout


class PopupWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Popup Window")
        self.setLayout(QVBoxLayout())
        label = QLabel("This is a popup window")
        self.layout().addWidget(label)


class MainWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setLayout(QVBoxLayout())
        button = QPushButton("Open Popup Window")
        button.clicked.connect(self.show_popup_window)
        self.layout().addWidget(button)

    def show_popup_window(self):
        popup = PopupWindow(self)
        popup.exec_()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
