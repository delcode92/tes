from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QSizePolicy

app = QApplication([])

layout = QVBoxLayout()
layout.setContentsMargins(0,0,0,0)
layout.setSpacing(0)

label1 = QLabel("Label 1")
label1.setStyleSheet("background:red;")
label1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
layout.addWidget(label1)

label2 = QLabel("Label 2")
label2.setStyleSheet("background:green;")
label2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
layout.addWidget(label2)

label3 = QLabel("Label 3")
label3.setStyleSheet("background:blue;")
label3.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
layout.addWidget(label3)

# Create a parent widget to hold the layout
parent_widget = QWidget()
parent_widget.setLayout(layout)
parent_widget.show()

app.exec_()
