from PyQt6 import QtWidgets, QtGui
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QByteArray
import sys, MySQLdb as mdb
from Radio import *

conn = mdb.connect("localhost", "root", "", "pixmap")

def get_data():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books;")
    res = cursor.fetchall()
    return res

class MainWin(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Radio")
        layout = QtWidgets.QVBoxLayout(self)
        self.setStyleSheet("background: #a6a6a6")
        res_data = get_data()

        for i in res_data:
            img = i[3]
            qimage = QImage.fromData(QByteArray(img))
            qpixmap = QPixmap.fromImage(qimage)
            file_path = f"save_img/{i[1]}.jpg"
            qpixmap.save(file_path, "JPG")

            rad = QtWidgets.QRadioButton(f"{i[1]}", self)
            rad.setObjectName(f"{i[0]}")
            rad.setStyleSheet(
                f"QRadioButton::indicator {{width: 40px; height: 40px}}"
                f" QRadioButton::indicator::unchecked"
                f" {{image: url('save_img/{i[1]}.jpg');}} QRadioButton::indicator::checked "
                f"{{image: url('img_check/check.png');}}"
            )
            layout.addWidget(rad)
            rad.toggled.connect(self.on_toggled)
        btn = QtWidgets.QPushButton("Записать", self)
        layout.addWidget(btn)
        btn.clicked.connect(self.on_clicked)
        self.check = False

    def on_toggled(self, checked):
        radio = self.sender()
        if checked:
            self.selected_radio = radio
            self.check = True

    def on_clicked(self):
        if self.check:
            cur = conn.cursor()
            cur.execute(f"CALL `rate`({self.selected_radio.objectName()});")
            cur.close()
            conn.commit()
            print("Selected Radio: ", self.selected_radio.objectName(), self.selected_radio.text())
        else:
            print("No radio selected")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWin()
    win.show()
    sys.exit(app.exec())