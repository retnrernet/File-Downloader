from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
import sys
from os import path
import download
import clipboard
import threading


FORM_CLASS,_ = loadUiType(path.join(path.dirname(__file__), "main.ui"))

class MainApp(QMainWindow, FORM_CLASS):

    progressValue = 0
    step = 0
    download_ended = False
    running = threading.Event()

    def __init__(self, parent= None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.downloadThread = download.Download_Thread()
        self.setup_Ui()
        self.init_Buttons()
        self.running.set()
        # Making the connection
        self.make_connection(self.downloadThread)


    def setup_Ui(self):
        self.setWindowTitle("File Downloader")
        self.setFixedSize(650,260)
        self.progressBar.setProperty("value", 0)
        self.url_text.setText("")
        self.save_text.setText("")

    def init_Buttons(self):
        self.downloadButton.clicked.connect(self.download)
        self.cancelButton.clicked.connect(self.cancel)
        self.pasteButton.clicked.connect(self.paste_url)
        self.browseButton.clicked.connect(self.browse)

    def cancel(self):
        self.downloadThread.exit()

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
            self.downloadThread.start()
            self.downloadThread.download(url, save_location)


    def browse(self):
        save_location = QFileDialog.getSaveFileName(self, caption = "Save As", directory=".", filter = "All files (*.*)")
        save_location = save_location[0]
        save_location = save_location[2:]
        self.save_text.setText(save_location)

    def make_connection(self, threadObj):
        self.downloadThread.changedValue.connect(self.receive_progress)
        self.downloadThread.downloadError.connect(self.download_error)


    @pyqtSlot(float)
    def receive_progress(self, val):
        self.step = val
        print(self.step)
        self.progress_thread = threading.Thread(target=self.update_progressBar, args=(self.running,))
        self.progress_thread.start()

    def update_progressBar(self, running):
        self.progressValue += self.step
        self.progressBar.setProperty("value", self.progressValue * 100)
        if self.progressValue > 1:
            #self.running.clear()
            #self.progress_thread.join()
            self.end_download()


    def end_download(self):
        self.progressBar.setProperty("value", 100)
        QMessageBox.information(self, "Download Completed", "Your file has been downloaded successfully", QMessageBox.Ok)
        self.url_text.setText("")
        self.save_text.setText("")
        self.progressBar.setProperty("value", 0)
        self.downloadThread.exit()

    @pyqtSlot()
    def download_error(self):
        QMessageBox.warning(self, "Error", "Sorry! Cannot Download your file. Check your internet connection.", QMessageBox.Ok)



def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()



    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


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