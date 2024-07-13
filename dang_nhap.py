from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt

class DangNhapDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Đăng nhập")
        self.setModal(True)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        self.username_label = QLabel("Tên đăng nhập:")
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.password_label = QLabel("Mật khẩu:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Đăng nhập")
        self.login_button.clicked.connect(self.xac_thuc_dang_nhap)
        layout.addWidget(self.login_button)

    def xac_thuc_dang_nhap(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Đây chỉ là ví dụ đơn giản, bạn nên sử dụng phương pháp bảo mật hơn trong thực tế
        if username == "admin" and password == "123456":
            self.accept()
        else:
            QMessageBox.warning(self, "Lỗi đăng nhập", "Tên đăng nhập hoặc mật khẩu không đúng!")