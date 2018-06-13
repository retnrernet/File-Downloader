from PyQt5.QtCore import *
import urllib.request


class Download_Thread(QThread):

    changedValue = pyqtSignal(int)

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def calculateProgress(self, blocks_count, block_size, total_size):
        if total_size == 0:
            pass
        size = (blocks_count+1) * block_size
        self.percent_size = size * 100 / total_size
        self.changedValue.emit(self.percent_size)
        if size < total_size:
            self.percent_size = size * 100 / total_size
        else:
            self.percent_size = 100


    def download(self, url, save_location):

        try:
            urllib.request.urlretrieve(url, save_location, self.calculateProgress)

        except:
            print("Error")

    def run(self):
        pass

    def on_changed_value(self, value):
        self.changedValue.emit(value)



