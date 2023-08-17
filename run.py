#!/usr/bin/env python3
import os

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import threading

from flash import process_flash


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.form_widget = FormWidget(self)
        self.setCentralWidget(self.form_widget)

        self.setWindowIcon(QIcon('resources/icon.png'))
        # set the title
        self.setWindowTitle("PrivacySociety GSI Updater")

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

        self.variant_text_edit = QLabel("Variant")
        self.layout.addWidget(self.variant_text_edit, 1, 0, Qt.AlignmentFlag.AlignLeft)

        self.gsi_variant = QComboBox()
        # self.gsi_variant.setEnabled(False)
        self.gsi_variant.setFixedWidth(300)
        self.gsi_variant.setFixedHeight(20)
        # self.gsi_variant.setVisible(False)
        self.gsi_variant.addItem("Titan Pocket")
        self.gsi_variant.addItem("Jelly 2E")
        # self.gsi_variant.addItem("Atom L")
        self.gsi_variant.addItem("Pixel 5a")
        self.layout.addWidget(self.gsi_variant, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(300)
        self.layout.addWidget(self.progress_bar, 2, 0, 1, 2, Qt.AlignmentFlag.AlignLeft)

        self.button1 = QPushButton("Flash")
        self.layout.addWidget(self.button1, 2, 1, Qt.AlignmentFlag.AlignRight)

        self.setLayout(self.layout)


app = QApplication(sys.argv)
window = Window()


def flash_click():
    # window.form_widget.setEnabled(False)
    # ui.start_progressbar(window.form_widget.progress_bar)
    # flash.process_progressbar(window.form_widget.progress_bar)
    url = window.form_widget.url_text_edit.toPlainText()
    variant = window.form_widget.gsi_variant.currentText()
    process_flash(url, variant, window.form_widget.progress_bar)
    # window.form_widget.gsi_variant.setVisible(True)
    # window.form_widget.setEnabled(True)
    # msg = QMessageBox()
    # msg.setWindowTitle("Flash Complete.")
    # msg.setText("Flashing has completed. Your phone is rebooting into PrivacySociety GSI.")
    # msg.exec_()


def flash_click_event():
    # ui.start_progressbar(window.form_widget.progress_bar)
    window.form_widget.setEnabled(False)
    window.form_widget.progress_bar.setValue(0)
    x = threading.Thread(target=flash_click)
    x.start()
    while x.is_alive():
        # window.form_widget.setEnabled(False)
        ""  # Do Nothing
    window.form_widget.progress_bar.setValue(100)
    window.form_widget.setEnabled(True)


def main():
    window.form_widget.button1.clicked.connect(lambda: flash_click_event())

    sys.exit(app.exec())
    return


if __name__ == '__main__':
    main()
