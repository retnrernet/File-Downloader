from PyQt5.QtCore import *
import urllib.request


class Download_Thread(QThread):

    changedValue = pyqtSignal(int)
    downloadError = pyqtSignal()


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


    def download(self, url, save_location):

        try:
            urllib.request.urlretrieve(url, save_location, self.calculateProgress)

        except:
            self.downloadError.emit()
            print("Error")

    def run(self):
        pass

    #def on_changed_value(self, value):
     #   self.changedValue.emit(value)



