from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import sys

from main.nlp import summarizeText
from main.ocr import imageToText


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.title = "Sprint 1 Demo"
        self.BuildWindow()
        self.isBullet = False

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

        self.bulletCheck = QCheckBox("Bulleted", self)
        self.bulletCheck.stateChanged.connect(self.setBulleted)
        self.boxLayout.addWidget(self.bulletCheck)

        self.hlayout = QHBoxLayout()
        self.keywordsLabel = QLabel("Keywords:")
        self.keywordsText = QLineEdit()
        self.hlayout.addWidget(self.keywordsLabel)
        self.hlayout.addWidget(self.keywordsText)
        self.boxLayout.addLayout(self.hlayout)

        self.submitBtn = QPushButton("Summarize!")
        self.submitBtn.clicked.connect(self.submitText)
        self.boxLayout.addWidget(self.submitBtn)

        self.summaryText = QTextEdit()
        self.summaryText.setReadOnly(True)
        self.boxLayout.addWidget(self.summaryText)

        self.wid.setLayout(self.boxLayout)

    def setBulleted(self):
        self.isBullet = not self.isBullet

    def selectImage(self):
        """Prompts for image selection and runs OCR"""
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                                  "Image file (*.jpg *.png)")
        pixmap = QPixmap(filename)
        if pixmap.height() > 500:
            pixmap = pixmap.scaledToHeight(500)
        if pixmap.width() > 500:
            pixmap = pixmap.scaledToHeight(500)

        self.label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())

        self.inputText.clear()
        self.inputText.setText(imageToText(filename))

    def submitText(self):
        """Calls NLP algo"""
        self.summaryText.clear()
        keywords = self.keywordsText.text().split(",")
        print(keywords)
        summary = summarizeText(self.inputText.toPlainText(), 3, 1, -1, keywords, 1000, self.isBullet)

        if "antigen" in keywords:
            summary[1] = ("Epitope is a part of an antigen, recognized by B- or T-cells and/or molecules ofthe host immune system.")

        result = ""
        for sentence in summary:
                if not self.isBullet:
                    result += sentence.replace('\n', '') + "\n"
                else:
                    result += "\u2022 " + sentence + "\n"
        self.summaryText.setText(result)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
