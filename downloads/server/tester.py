import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel

app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Vertical Box Layout Example")

# Create a vertical box layout
vbox = QVBoxLayout()

# Create a label widget
label = QLabel("This is a label in a vertical box layout")

# Add the label to the layout
vbox.addWidget(label)

# Set the layout to the main window
window.setLayout(vbox)

# Show the main window
window.show()

sys.exit(app.exec_())
