from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
import sys
from os import path
import download
import clipboard


FORM_CLASS,_ = loadUiType(path.join(path.dirname(__file__), "main.ui"))


class MainApp(QMainWindow, FORM_CLASS):

    def __init__(self, parent= None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.downloadThread = download.Download_Thread()
        self.setup_Ui()
        self.init_Buttons()

        # Making the connection
        self.make_connection(self.downloadThread)




    def setup_Ui(self):
        self.setWindowTitle("Download Manager")
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
        self.downloadThread.start()

        self.downloadThread.download(url, save_location)

    def browse(self):
        save_location = QFileDialog.getSaveFileName(self, caption = "Save As", directory=".", filter = "All files (*.*)")
        save_location = save_location[0]
        save_location = save_location[2:]
        self.save_text.setText(save_location)

    def make_connection(self, threadObj):
        self.downloadThread.changedValue.connect(self.update_progressBar)

    @pyqtSlot(int)
    def update_progressBar(self, val):
        self.progressBar.setProperty("value", val)
        if val > 100:
            val = 100
            self.progressBar.setProperty("value", val)
            QMessageBox.information(self, "Download Completed", "Your file has been downloaded successfully", QMessageBox.Ok)
            self.url_text.setText("")
            self.save_text.setText("")
            self.progressBar.setProperty("value", 0)
            self.downloadThread.exit()



def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

