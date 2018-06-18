from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
import sys
from os import path
import clipboard
import Handler



FORM_CLASS,_ = loadUiType(path.join(path.dirname(__file__), "main.ui"))

class MainApp(QMainWindow, FORM_CLASS):

    progress_value = 0
    def __init__(self, parent= None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setup_Ui()
        self.init_Buttons()
        self.handler_thread = Handler.Handler_Thread()
        self.make_connection()

    def setup_Ui(self):
        self.setWindowTitle("File Downloader")
        self.setFixedSize(650,260)
        self.progressBar.setProperty("value", 0)
        self.url_text.setText("")
        self.save_text.setText("")


    def init_Buttons(self):
        self.downloadButton.clicked.connect(self.download)
        self.pasteButton.clicked.connect(self.paste_url)
        self.browseButton.clicked.connect(self.browse)

    def make_connection(self):
        self.handler_thread.progressSignal.connect(self.update_progressBar)
        self.handler_thread.error.connect(self.download_error)

    def paste_url(self):
        text = clipboard.paste()
        self.url_text.setText(text)

    def download(self):
        url = self.url_text.text()
        save_location = self.save_text.text()
        if url == "":
            QMessageBox.warning(self, "No URL!", "You must specify URL to download your file")

        elif "http" not in url:
            QMessageBox.warning(self, "Wrong URL!", "This is not a proper URL")
        else:
            if save_location == "":
                l = url.split('/')
                i = len(l) - 1
                save_location = l[i]
                self.save_text.setText(save_location)
            self.handler_thread.start()
            self.handler_thread.start_download(url, save_location)


    def browse(self):
        save_location = QFileDialog.getSaveFileName(self, caption = "Save As", directory=".", filter = "All files (*.*)")
        save_location = save_location[0]
        save_location = save_location[2:]
        self.save_text.setText(save_location)


    @pyqtSlot(int)
    def update_progressBar(self, val):
        #print("prog-main-here")
        #self.progress_value = self.handler_thread.progressValue
        #self.init_Buttons()
        self.progress_value = val
        print(self.progress_value)
        self.progressBar.setProperty("value", self.progress_value)
        if self.progress_value > 100:
            self.handler_thread.exit()
            self.progressBar.setProperty("value", 100)
            QMessageBox.information(self, "Download Completed", "Your file has been downloaded successfully",QMessageBox.Ok)
            self.url_text.setText("")
            self.save_text.setText("")
            self.progressBar.setProperty("value", 0)

    @pyqtSlot()
    def download_error(self):
        QMessageBox.warning(self, "Error", "Sorry! Cannot Download your file. Check your internet connection.", QMessageBox.Ok)

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

# my idea another thread that takes value through signals from calcprogress and that thread signals it into GUI but every certain time
"""
        if val < 100:
            self.progressBar.setProperty("value", val)
        else:
            val = 100
            self.progressBar.setProperty("value", val)
            QMessageBox.information(self, "Download Completed", "Your file has been downloaded successfully", QMessageBox.Ok)
            self.url_text.setText("")
            self.save_text.setText("")
            self.progressBar.setProperty("value", 0)
            self.downloadThread.exit()
            
            
            
            
             def kill_thread(self):
        QMessageBox.information(self, "Download Completed", "Your file has been downloaded successfully", QMessageBox.Ok)
        self.url_text.setText("")
        self.save_text.setText("")
        self.progressBar.setProperty("value", 0)
        self.downloadThread.exit()
        self.running.clear()
        #self.progress_thread.join()
        
        
        
"""