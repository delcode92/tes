from PyQt5.QtGui import QPalette, QColor, QBrush
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtPrintSupport import QPrinter, QPrintPreviewDialog
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys

class PdfPreview(QWebEngineView):
    def __init__(self, parent=None):
        super(PdfPreview, self).__init__(parent)
        self.loadFinished.connect(self.handle_load_finished)

    def handle_load_finished(self):
        self.page().runJavaScript("document.body.style.zoom = '125%'")

class PreviewDialog(QPrintPreviewDialog):
    def __init__(self, printer, parent=None):
        super(PreviewDialog, self).__init__(printer, parent)
        self.pdf_preview = PdfPreview()
        self.layout().addWidget(self.pdf_preview)
        self.setWindowTitle('PDF Preview')

    def paintRequested(self, printer):
        self.pdf_preview.setUrl(QUrl.fromLocalFile(self.printer().outputFileName()))
        super(PreviewDialog, self).paintRequested(printer)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    printer = QPrinter()
    preview = PreviewDialog(printer)
    # Load your pdf file here
    preview.pdf_preview.load(QUrl.fromLocalFile('example.pdf'))
    preview.exec_()
