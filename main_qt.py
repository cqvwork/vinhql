import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt
from giao_dien import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Sử dụng style Fusion cho giao diện nhất quán
    window = MainWindow()
    window.setMinimumSize(800, 600)  # Đặt kích thước tối thiểu cho cửa sổ
    window.show()
    sys.exit(app.exec())