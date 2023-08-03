#!/usr/bin/env python3

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.form_widget = FormWidget(self)
        self.setCentralWidget(self.form_widget)

        self.setWindowIcon(QIcon('resources/icon.png'))
        # set the title
        self.setWindowTitle("PrivacySociety GSI Updater")

        # setting  the geometry of window
        # self.setGeometry(0, 0, 400, 300)

        # show all the widgets
        self.show()


class FormWidget(QWidget):

    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)
        self.layout = QGridLayout(self)

        self.url_text = QLabel("Update URL:")
        self.layout.addWidget(self.url_text, 0, 0, Qt.AlignmentFlag.AlignLeft)

        self.url_text_edit = QTextEdit("https://ota.privacysociety.org/ota.json")
        self.url_text_edit.setEnabled(False)
        self.url_text_edit.setFixedWidth(300)
        self.url_text_edit.setFixedHeight(20)
        self.layout.addWidget(self.url_text_edit, 0, 1, Qt.AlignmentFlag.AlignRight)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(300)
        self.layout.addWidget(self.progress_bar, 1, 0, 1, 2, Qt.AlignmentFlag.AlignLeft)

        # verticalSpacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # self.layout.addItem(verticalSpacer, 6, 0, Qt.AlignTop)

        self.button1 = QPushButton("Flash")
        self.layout.addWidget(self.button1, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.setLayout(self.layout)


def main():
    app = QApplication(sys.argv)
    window = Window()

    sys.exit(app.exec())
    return


if __name__ == '__main__':
    main()
