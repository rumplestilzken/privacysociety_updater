import threading
import PyQt5.QtWidgets

progressbar_value = 0


def applyProgress(value):
    global progressbar_value
    progressbar_value += value


def process_progressbar(progressbar):
    global progressbar_value
    while True:
        progressbar.setValue(progressbar_value)


def start_progressbar(progressbar):
    x = threading.Thread(target=process_progressbar, args=progressbar, daemon=True)
    x.start()
