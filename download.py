from PyQt5.QtCore import *
import urllib.request
import time

class Download_Thread(QThread):

    changedValue = pyqtSignal(int)
    downloadError = pyqtSignal()
    percent = 0

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def calculateProgress(self, blocks_count, block_size, total_size):
        if total_size == 0:
            pass
        size = (blocks_count+1) * block_size
        self.percent = size * 100 / total_size
        self.changedValue.emit(self.percent)
        #print("fom download")

    def download(self, url, save_location):
        #print(url + ' ' + save_location + " from download f")
        try:
            urllib.request.urlretrieve(url, save_location, self.calculateProgress)

        except:
            self.downloadError.emit()
            print("Error")

    def run(self):
        pass

