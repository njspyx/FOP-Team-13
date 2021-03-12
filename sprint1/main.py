from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import sys

from nlp import summarizeText
from ocr import imageToText


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Sprint 1 Demo")
        self.BuildWindow()

    def BuildWindow(self):
        self.wid = QWidget(self)
        self.setCentralWidget(self.wid)
        self.boxLayout = QVBoxLayout()

        self.imageBtn = QPushButton("Select Image")
        self.imageBtn.clicked.connect(self.selectImage)
        self.boxLayout.addWidget(self.imageBtn)

        self.label = QLabel("")
        self.boxLayout.addWidget(self.label)

        self.inputText = QTextEdit()
        self.boxLayout.addWidget(self.inputText)

        self.submitBtn = QPushButton("Summarize!")
        self.submitBtn.clicked.connect(self.submitText)
        self.boxLayout.addWidget(self.submitBtn)

        self.summaryText = QTextEdit()
        self.summaryText.setReadOnly(True)
        self.boxLayout.addWidget(self.summaryText)

        self.wid.setLayout(self.boxLayout)

    def selectImage(self):
        """Prompts for image selection and runs OCR"""
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                                  "Image file (*.jpg *.png)")
        pixmap = QPixmap(filename)
        if pixmap.height() > 500:
            pixmap = pixmap.scaledToHeight(500)
        if pixmap.width() > 500:
            pixmap = pixmap.scaledToWidth(500)

        self.label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())

        self.inputText.clear()
        self.inputText.setText(imageToText(filename))

    def submitText(self):
        """Calls NLP algo"""
        self.summaryText.clear()
        summary = summarizeText(self.inputText.toPlainText(), 3, 5, -3)
        
        newText = ""
        for sentence in summary:
            newText += sentence + "\n"
        self.summaryText.setText(newText)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
