from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
import sys
from os import path
import download
import clipboard
import main
import download


class Progress_Bar(QObject, MainApp):

    def __init__(self):
        self.progressBar.setProperty("value", 0)
        self.downloadThread.changedValue.connect(self.update_progressBar)

    @pyqtSlot(int)
    def update_progressBar(self, val):
        self.progressBar.setProperty("value", val)
        if val > 100:
            val = 100
            self.progressBar.setProperty("value", val)
            QMessageBox.information(self, "Download Completed", "Your file has been downloaded successfully",
                                    QMessageBox.Ok)
            self.url_text.setText("")
            self.save_text.setText("")
            self.progressBar.setProperty("value", 0)
            self.downloadThread.exit()



######################################################################################3


#def handle_ProgressBar(self):
     #   self.progress = Progress_Bar()
      #  self.progress_thread = QThread()

        #self.progress.newParams.connect(self.changeTextEdit)
#        self.progress.moveToThread(self.progress_thread)
 #       self.progress_thread.start()