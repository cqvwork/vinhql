import sys
from PySide6.QtWidgets import QApplication,QDialog
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt
from giao_dien import MainWindow
from dang_nhap import DangNhapDialog

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    dang_nhap = DangNhapDialog()
    if dang_nhap.exec() == QDialog.Accepted:
        window = MainWindow()
        window.setMinimumSize(800, 600)
        window.show()
        sys.exit(app.exec())
    else:
        sys.exit()