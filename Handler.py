from PyQt5.QtCore import *
import urllib.request
import time
import download


class Handler_Thread(QThread):

    #changedValue = pyqtSignal(float)
    error = pyqtSignal()
    progressSignal = pyqtSignal(int)
    progressValue = 0
    downloadThread = download.Download_Thread()
    timer = QTimer()


    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        #self.wait()
        pass


    def make_connection(self):
        self.downloadThread.changedValue.connect(self.update_progressBar) # was update_progressBar
        self.downloadThread.downloadError.connect(self.report_error)

    def run(self):
        self.downloadThread.start()
        self.make_connection()


    def start_download(self, url, save_location):
        self.downloadThread.download(url, save_location)



        #print(url + ' ' + save_location)

    def send_progress(self):
        #print('progSending')
        #print(self.progressValue)
        try:
            self.progressSignal.emit(self.progressValue)
        except:
            print('sendError')

    @pyqtSlot(int)
    def update_progressBar(self, val):
        #print("from-handler update")
        #self.timer.timeout.connect(self.send_progress)
        #self.timer.start(1000)
        self.progressValue = val
        if self.progressValue > 100:
            self.downloadThread.exit()
        time.sleep(1)
        self.send_progress()

    @pyqtSlot()
    def report_error(self):
        self.error.emit()




