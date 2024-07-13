import sys
import datetime
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                               QPushButton, QVBoxLayout, QHBoxLayout,
                               QComboBox, QCheckBox, QMessageBox,
                               QListWidget, QDialog, QTableWidget, QTableWidgetItem, QSpinBox,
                               QTabWidget, QListWidgetItem, QMainWindow, QDateEdit, QStyle, QFrame, QScrollArea,QFormLayout)
from PySide6.QtGui import QFont, QIcon, QColor, QPalette , QGuiApplication
from PySide6.QtCore import Qt, QDate 
import copy
from file_manager import doc_diem_danh
from models import HocSinh, LopHoc
from file_manager import (doc_danh_sach_lop_hoc, luu_danh_sach_lop_hoc,
                          luu_diem_danh, doc_thoi_khoa_bieu, luu_thoi_khoa_bieu,
                          doc_danh_sach_hoc_sinh, luu_danh_sach_hoc_sinh, doc_diem_danh)
from xu_ly import xuat_diem_danh_excel

# Định nghĩa stylesheet
# Apple-inspired stylesheet
STYLESHEET = """
QWidget {
    background-color: #ffffff;
    color: #000000;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica', 'Arial', sans-serif;
}
QPushButton {
    background-color: #007AFF;
    color: white;
    border: none;
    padding: 10px 20px;
    font-size: 14px;
    border-radius: 10px;
}
QPushButton:hover {
    background-color: #0056b3;
}
QPushButton:pressed {
    background-color: #003d80;
}
QComboBox {
    border: 1px solid #cccccc;
    border-radius: 10px;
    padding: 5px 10px;
    min-width: 6em;
}
QComboBox::drop-down {
    border: none;
}
QComboBox::down-arrow {
    image: url(down_arrow.png);
    width: 12px;
    height: 12px;
}
QListWidget, QTableWidget {
    border: 1px solid #cccccc;
    border-radius: 10px;
}
QTabWidget::pane {
    border: none;
}
QTabBar::tab {
    background: #f0f0f0;
    border: none;
    padding: 8px 16px;
    margin-right: 2px;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
}
QTabBar::tab:selected {
    background: #ffffff;
    border-bottom: 2px solid #007AFF;
}
QLineEdit {
    border: 1px solid #cccccc;
    border-radius: 10px;
    padding: 5px 10px;
}
"""
class AppleStyleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(STYLESHEET)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setModal(True)

    def create_button(self, text, function):
        button = QPushButton(text)
        button.clicked.connect(function)
        return button
    
class ThemSuaHocVienDialog(QDialog):
    def __init__(self, ma_lop, danh_sach_hs, main_window, hoc_sinh_hien_tai=None):
        super().__init__(main_window)
        self.ma_lop = ma_lop
        self.danh_sach_hs = danh_sach_hs
        self.main_window = main_window
        self.hoc_sinh_hien_tai = hoc_sinh_hien_tai

        self.setWindowTitle(f"{'Sửa' if hoc_sinh_hien_tai else 'Thêm'} học viên lớp {ma_lop}")
        self.init_ui()
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)

        fields = [
            ("Mã học sinh:", QLineEdit),
            ("Tên học sinh:", QLineEdit),
            ("Số điện thoại:", QLineEdit)
        ]  # Đã xóa "Số buổi học:"

        for label_text, widget_type in fields:
            field_layout = QHBoxLayout()
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 16px;")
            widget = widget_type()
            widget.setStyleSheet("font-size: 16px;")
            field_layout.addWidget(label)
            field_layout.addWidget(widget)
            form_layout.addLayout(field_layout)

            setattr(self, f"edit_{label_text.lower().replace(' ', '_').replace(':', '')}", widget)

        if self.hoc_sinh_hien_tai:
            self.edit_mã_học_sinh.setText(self.hoc_sinh_hien_tai.ma_hs)
            self.edit_tên_học_sinh.setText(self.hoc_sinh_hien_tai.ten_hs)
            self.edit_số_điện_thoại.setText(self.hoc_sinh_hien_tai.sdt)
        else:
            self.edit_mã_học_sinh.setText(self.tao_ma_hs_moi())
            self.edit_mã_học_sinh.setReadOnly(True)

        layout.addLayout(form_layout)

        button_luu = QPushButton("Lưu" if self.hoc_sinh_hien_tai else "Thêm")
        button_luu.clicked.connect(self.luu_hoc_sinh)
        layout.addWidget(button_luu)
    def create_button(self, text, function):
        button = QPushButton(text)
        button.clicked.connect(function)
        return button
    def tao_ma_hs_moi(self):
        ma_hs_hien_tai = [hs.ma_hs for hs in self.danh_sach_hs.values() if hs.ma_hs.startswith(self.ma_lop)]
        if not ma_hs_hien_tai:
            return f"{self.ma_lop}001"
        so_thu_tu = max(int(ma_hs[-3:]) for ma_hs in ma_hs_hien_tai) + 1
        return f"{self.ma_lop}{so_thu_tu:03d}"
    def luu_hoc_sinh(self):
        ma_hs = self.edit_mã_học_sinh.text()
        ten_hs = self.edit_tên_học_sinh.text()
        sdt = self.edit_số_điện_thoại.text()

        if not ma_hs or not ten_hs:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin học sinh!")
            return

        hoc_sinh = HocSinh(ma_hs, ten_hs, self.ma_lop, sdt=sdt)
        self.danh_sach_hs[ma_hs] = hoc_sinh
        luu_danh_sach_hoc_sinh(self.danh_sach_hs)
        self.main_window.cap_nhat_danh_sach_hs()
        self.close()

class ThemLopHocDialog(AppleStyleDialog):
    def __init__(self, danh_sach_lop, main_window):
        super().__init__()
        self.danh_sach_lop = danh_sach_lop
        self.main_window = main_window
        self.setWindowTitle("Thêm Lớp Học")
        self.init_ui()

    def tao_ma_lop_moi(self):
        ma_lop_hien_tai = [lop.ma_lop for lop in self.danh_sach_lop.values()]
        if not ma_lop_hien_tai:
            return "L001"
        so_thu_tu = max(int(ma_lop[1:]) for ma_lop in ma_lop_hien_tai) + 1
        return f"L{so_thu_tu:03d}"

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        self.edit_ma_lop = QLineEdit(self.tao_ma_lop_moi())
        self.edit_ma_lop.setReadOnly(True)
        self.edit_ten_lop = QLineEdit()

        form_layout.addRow("Mã lớp học:", self.edit_ma_lop)
        form_layout.addRow("Tên lớp học:", self.edit_ten_lop)

        layout.addLayout(form_layout)

        self.button_them = self.create_button("Thêm", self.them_lop_hoc)
        layout.addWidget(self.button_them)

    def them_lop_hoc(self):
        ma_lop_moi = self.edit_ma_lop.text()
        ten_lop_moi = self.edit_ten_lop.text()
        if ten_lop_moi:
            lop_hoc = LopHoc(ma_lop_moi, ten_lop_moi)
            self.danh_sach_lop[ma_lop_moi] = lop_hoc
            luu_danh_sach_lop_hoc(self.danh_sach_lop)
            self.main_window.cap_nhat_danh_sach_lop_hoc()
            QMessageBox.information(self, "Thông báo", f"Đã thêm lớp học {ten_lop_moi}!")
            self.close()
        else:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tên lớp học!")
class XoaHocVienDialog(QDialog):
    def __init__(self, ma_lop, danh_sach_hs, main_window):
        super().__init__()
        self.ma_lop = ma_lop
        self.danh_sach_hs = danh_sach_hs
        self.main_window = main_window
        self.setWindowTitle(f"Xóa học viên khỏi lớp {ma_lop}")
        self.init_ui()

    def init_ui(self):
        self.label_chon_hv = QLabel("Chọn học viên:")
        self.list_hoc_vien = QListWidget(self)

        # Hiển thị danh sách học sinh
        for hoc_sinh in self.danh_sach_hs.values():
            if hoc_sinh.ma_lop == self.ma_lop:
                self.list_hoc_vien.addItem(f"{hoc_sinh.ten_hs} ({hoc_sinh.ma_hs})")

        self.button_xoa = QPushButton("Xóa")
        self.button_xoa.clicked.connect(self.xoa_hoc_vien)
        vbox = QVBoxLayout()
        vbox.addWidget(self.label_chon_hv)
        vbox.addWidget(self.list_hoc_vien)
        vbox.addWidget(self.button_xoa)

        self.setLayout(vbox)

    def xoa_hoc_vien(self):
        selected_item = self.list_hoc_vien.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn học viên để xóa!")
            return

        ten_hv_chon = selected_item.text()
        ma_hs_chon = ten_hv_chon.split("(")[1].split(")")[0]

        if ma_hs_chon in self.danh_sach_hs:
            del self.danh_sach_hs[ma_hs_chon]
            luu_danh_sach_hoc_sinh(self.danh_sach_hs)
            self.main_window.cap_nhat_danh_sach_hs()
            self.list_hoc_vien.takeItem(self.list_hoc_vien.row(selected_item))
            QMessageBox.information(self, "Thông báo", f"Đã xóa học viên {ten_hv_chon} khỏi lớp {self.ma_lop}!")
        else:
            QMessageBox.warning(self, "Lỗi", f"Không tìm thấy học viên có mã {ma_hs_chon}")

class DiemDanhDialog(QDialog):
    def __init__(self, ma_lop, danh_sach_hs):
        super().__init__()
        self.ma_lop = ma_lop
        self.danh_sach_hs = danh_sach_hs
        self.setWindowTitle(f"Điểm danh lớp {ma_lop}")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        date_layout = QHBoxLayout()
        date_label = QLabel("Ngày điểm danh:")
        date_label.setStyleSheet("font-size: 16px;")
        self.date_edit = QDateEdit()
        self.date_edit.setStyleSheet("font-size: 16px;")
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_edit)
        layout.addLayout(date_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        self.checkboxes = {}
        for hoc_sinh in self.danh_sach_hs.values():
            if hoc_sinh.ma_lop == self.ma_lop:
                checkbox = QCheckBox(hoc_sinh.ten_hs)
                checkbox.setStyleSheet("font-size: 16px;")
                self.checkboxes[hoc_sinh.ma_hs] = checkbox
                scroll_layout.addWidget(checkbox)

        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)

        self.button_luu_diem_danh = self.create_button("Lưu điểm danh", self.luu_diem_danh)
        layout.addWidget(self.button_luu_diem_danh)

    def luu_diem_danh(self):
        ngay = self.date_edit.date().toString(Qt.ISODate)
        diem_danh = {}
        for ma_hs, checkbox in self.checkboxes.items():
            diem_danh[ma_hs] = "Có mặt" if checkbox.isChecked() else "Vắng mặt"
        
        luu_diem_danh(self.ma_lop, diem_danh, ngay)
        QMessageBox.information(self, "Thông báo", f"Đã lưu điểm danh ngày {ngay}!")

    def create_button(self, text, function):
        button = QPushButton(text)
        button.clicked.connect(function)
        return button
class ThoiKhoaBieuDialog(QDialog):
    def __init__(self, ma_lop):
        super().__init__()
        self.ma_lop = ma_lop
        self.setWindowTitle(f"Thời Khóa Biểu Lớp {ma_lop}")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        self.table_tkb = QTableWidget()
        self.table_tkb.setStyleSheet("font-size: 14px;")
        self.table_tkb.setRowCount(6)  # Thứ 2 đến thứ 7
        self.table_tkb.setColumnCount(10)  # 10 khung giờ học

        # Đặt nhãn cho hàng và cột
        self.table_tkb.setVerticalHeaderLabels(["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7"])
        khung_gio = ["8:00-9:00", "9:00-10:00", "10:00-11:00", "14:00-15:00", "15:00-16:00", 
                     "16:00-17:00", "17:00-18:00", "18:00-19:00", "19:00-20:00", "20:00-21:00"]
        self.table_tkb.setHorizontalHeaderLabels(khung_gio)

        layout.addWidget(self.table_tkb)

        self.button_luu_tkb = self.create_button("Lưu thời khóa biểu", self.luu_thoi_khoa_bieu)
        layout.addWidget(self.button_luu_tkb)

        # Đọc và hiển thị thời khóa biểu từ file (nếu có)
        self.hien_thi_thoi_khoa_bieu()
    def create_button(self, text, function):
        button = QPushButton(text)
        button.clicked.connect(function)
        return button
    def luu_thoi_khoa_bieu(self):
        tkb = {}
        for row in range(self.table_tkb.rowCount()):
            thu = row + 2  # Thứ 2 bắt đầu từ row 0
            tkb[thu] = {}
            for col in range(self.table_tkb.columnCount()):
                item = self.table_tkb.item(row, col)
                if item and item.text():
                    tkb[thu][col] = item.text()

        luu_thoi_khoa_bieu(self.ma_lop, tkb)
        QMessageBox.information(self, "Thông báo", f"Đã lưu thời khóa biểu cho lớp {self.ma_lop}!")

    def hien_thi_thoi_khoa_bieu(self):
        tkb = doc_thoi_khoa_bieu(self.ma_lop)
        for thu in tkb:
            row = int(thu) - 2  # Thứ 2 bắt đầu từ row 0
            for khung_gio, mon_hoc in tkb[thu].items():
                col = int(khung_gio)
                item = QTableWidgetItem(mon_hoc)
                self.table_tkb.setItem(row, col, item)

class QuanLyHocVienWidget(QWidget):
    def __init__(self, danh_sach_hs, ma_lop, main_window):
        super().__init__()
        self.danh_sach_hs = danh_sach_hs
        self.ma_lop = ma_lop
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        self.label_lop_hoc = QLabel(f"Quản lý học viên lớp {self.ma_lop}")
        self.label_lop_hoc.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(self.label_lop_hoc)

        # Thêm layout cho các nút chức năng
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        buttons = [
            ("Thêm học viên", self.mo_them_hoc_vien),
            ("Sửa học viên", self.mo_sua_hoc_vien),
            ("Xóa học viên", self.mo_xoa_hoc_vien),
        ]
        
        for text, func in buttons:
            button = QPushButton(text)
            button.setStyleSheet("font-size: 14px;")
            button.clicked.connect(func)
            button_layout.addWidget(button)

        layout.addLayout(button_layout)

        # Thêm widget chọn tháng và năm
        date_layout = QHBoxLayout()
        self.month_combo = QComboBox()
        self.month_combo.addItems([str(i) for i in range(1, 13)])
        self.month_combo.setCurrentText(str(datetime.datetime.now().month))
        self.year_spin = QSpinBox()
        self.year_spin.setRange(2000, 2100)
        self.year_spin.setValue(datetime.datetime.now().year)
        date_layout.addWidget(QLabel("Tháng:"))
        date_layout.addWidget(self.month_combo)
        date_layout.addWidget(QLabel("Năm:"))
        date_layout.addWidget(self.year_spin)
        date_layout.addStretch()

        export_button = QPushButton("Xuất phiếu điểm danh")
        export_button.clicked.connect(self.xuat_phieu_diem_danh)
        date_layout.addWidget(export_button)

        layout.addLayout(date_layout)

        self.list_widget = QListWidget(self)
        self.list_widget.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.list_widget)

        self.cap_nhat_danh_sach_hs()

    

    def mo_them_hoc_vien(self):
        dialog = ThemSuaHocVienDialog(self.ma_lop, self.danh_sach_hs, self.main_window)
        dialog.exec()

    def mo_sua_hoc_vien(self):
        selected_item = self.list_widget.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn học viên để sửa!")
            return

        ten_hs_chon = selected_item.text()
        ma_hs_chon = ten_hs_chon.split("(")[1].split(")")[0]

        hoc_sinh_hien_tai = self.danh_sach_hs.get(ma_hs_chon)
        if hoc_sinh_hien_tai:
            dialog = ThemSuaHocVienDialog(self.ma_lop, self.danh_sach_hs, self.main_window, hoc_sinh_hien_tai)
            dialog.exec()
            self.cap_nhat_danh_sach_hs()
        else:
            QMessageBox.warning(self, "Lỗi", f"Không tìm thấy học viên có mã {ma_hs_chon}")

    def mo_xoa_hoc_vien(self):
        XoaHocVienDialog(self.ma_lop, self.danh_sach_hs, self.main_window).exec()

    def cap_nhat_danh_sach_hs(self):
        self.list_widget.clear()
        for hoc_sinh in self.danh_sach_hs.values():
            if hoc_sinh.ma_lop == self.ma_lop:
                self.list_widget.addItem(f"{hoc_sinh.ten_hs} ({hoc_sinh.ma_hs})")


    def cap_nhat_ma_lop(self, ma_lop_moi):
        self.ma_lop = ma_lop_moi
        self.label_lop_hoc.setText(f"Quản lý học viên lớp {self.ma_lop}")
        self.cap_nhat_danh_sach_hs()

    def mo_diem_danh(self):
        dialog = DiemDanhDialog(self.ma_lop, self.danh_sach_hs)
        dialog.exec()

    def mo_thoi_khoa_bieu(self):
        dialog = ThoiKhoaBieuDialog(self.ma_lop)
        dialog.exec()
    def xuat_phieu_diem_danh(self):
        thang = int(self.month_combo.currentText())
        nam = self.year_spin.value()
        
        ma_lop = self.ma_lop
        ten_lop = self.main_window.danh_sach_lop[ma_lop].ten_lop
        
        if not ma_lop:
            QMessageBox.warning(self, "Lỗi", "Không thể xác định lớp để xuất phiếu điểm danh.")
            return
        
        # Đọc dữ liệu điểm danh
        diem_danh_data = doc_diem_danh(ma_lop, thang, nam)
        
        # Lọc danh sách học sinh của lớp được chọn
        danh_sach_hs_lop = [hs for hs in self.danh_sach_hs.values() if isinstance(hs, HocSinh) and hs.ma_lop == ma_lop]
        
        if not danh_sach_hs_lop:
            QMessageBox.warning(self, "Lỗi", f"Lớp {ten_lop} không có học sinh nào.")
            return
        
        # Cập nhật dữ liệu điểm danh cho từng học sinh
        for hs in danh_sach_hs_lop:
            hs.diem_danh = diem_danh_data.get(hs.ma_hs, {})
        
        # Gọi hàm xuất điểm danh Excel
        xuat_diem_danh_excel(ma_lop, ten_lop, danh_sach_hs_lop, thang, nam)
        QMessageBox.information(self, "Thông báo", f"Đã xuất phiếu điểm danh lớp {ten_lop} tháng {thang}/{nam}")
class QuanLyLopHocWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản Lý Lớp Học")
        self.setStyleSheet(STYLESHEET)
        self.danh_sach_lop = doc_danh_sach_lop_hoc()
        self.danh_sach_hs = doc_danh_sach_hoc_sinh()
        self.init_ui()
        self.center_on_screen()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()
        header_label = QLabel("Quản Lý Lớp Học")
        header_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        # Class selection and management
        class_layout = QHBoxLayout()
        class_layout.setSpacing(10)

        class_selection_layout = QVBoxLayout()
        class_selection_layout.setSpacing(5)
        
        class_label = QLabel("Chọn lớp học:")
        class_label.setStyleSheet("font-size: 16px;")
        class_selection_layout.addWidget(class_label)

        self.combo_lop_hoc = QComboBox()
        self.combo_lop_hoc.setStyleSheet("font-size: 16px;")
        self.cap_nhat_danh_sach_lop_hoc()
        class_selection_layout.addWidget(self.combo_lop_hoc)

        class_layout.addLayout(class_selection_layout)

        class_buttons_layout = QVBoxLayout()
        class_buttons_layout.setSpacing(10)

        self.button_them_lop = QPushButton("Thêm lớp học")
        self.button_them_lop.clicked.connect(self.mo_them_lop_hoc)
        class_buttons_layout.addWidget(self.button_them_lop)

        self.button_xoa_lop = QPushButton("Xóa lớp học")
        self.button_xoa_lop.clicked.connect(self.xoa_lop_hoc)
        class_buttons_layout.addWidget(self.button_xoa_lop)

        class_layout.addLayout(class_buttons_layout)
        class_layout.addStretch()

        main_layout.addLayout(class_layout)

        # Main content
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("QTabBar::tab { height: 30px; }")
        main_layout.addWidget(self.tab_widget)

        self.combo_lop_hoc.currentTextChanged.connect(self.thay_doi_lop_hoc_chon)

        ma_lop_dau_tien = next(iter(self.danh_sach_lop), None)
        if ma_lop_dau_tien:
            self.quan_ly_hoc_vien_widget = QuanLyHocVienWidget(
                copy.deepcopy(self.danh_sach_hs), ma_lop_dau_tien, self)
            self.tab_widget.addTab(self.quan_ly_hoc_vien_widget, "Quản lý học viên")

            # Thêm tab Thời khóa biểu
            self.thoi_khoa_bieu_widget = ThoiKhoaBieuWidget(ma_lop_dau_tien)
            self.tab_widget.addTab(self.thoi_khoa_bieu_widget, "Thời khóa biểu")

            # Thêm tab Điểm danh
            self.diem_danh_widget = DiemDanhWidget(ma_lop_dau_tien, self.danh_sach_hs)
            self.tab_widget.addTab(self.diem_danh_widget, "Điểm danh")

    def mo_diem_danh(self):
        ten_lop = self.main_window.combo_lop_hoc.currentText()
        if not ten_lop:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn lớp học!")
            return
        dialog = DiemDanhDialog(ten_lop, self.main_window.danh_sach_hs)
        dialog.exec()

    def mo_thoi_khoa_bieu(self):
        dialog = ThoiKhoaBieuDialog(self.danh_sach_lop)
        dialog.exec()
class ThoiKhoaBieuWidget(QWidget):
    def __init__(self, ma_lop):
        super().__init__()
        self.ma_lop = ma_lop
        self.init_ui()
        self.load_thoi_khoa_bieu()  # Thêm dòng này

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Tiêu đề
        self.label = QLabel(f"Thời khóa biểu lớp {self.ma_lop}")
        self.label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.label)

        # Bảng thời khóa biểu
        self.table = QTableWidget(7, 10)  # 6 hàng (Thứ 2 - Thứ 7), 10 cột (Tiết 1 - Tiết 8)
        khung_gio = ["8:00-9:00", "9:00-10:00", "10:00-11:00", "14:00-15:00", "15:00-16:00", 
                     "16:00-17:00", "17:00-18:00", "18:00-19:00", "19:00-20:00", "20:00-21:00"]
        self.table.setHorizontalHeaderLabels([khung_gio])
        self.table.setVerticalHeaderLabels(["Thứ " + str(i) for i in range(2, 9)])
        layout.addWidget(self.table)

        # Nút lưu thời khóa biểu
        self.button_save = QPushButton("Lưu thời khóa biểu")
        self.button_save.clicked.connect(self.luu_thoi_khoa_bieu)
        layout.addWidget(self.button_save)

        self.load_thoi_khoa_bieu()

    def load_thoi_khoa_bieu(self):
        tkb = doc_thoi_khoa_bieu(self.ma_lop)
        for thu in tkb:
            for tiet, mon_hoc in tkb[thu].items():
                self.table.setItem(int(thu) - 2, int(tiet) - 1, QTableWidgetItem(mon_hoc))

    def luu_thoi_khoa_bieu(self):
        tkb = {}
        for row in range(6):
            tkb[str(row + 2)] = {}
            for col in range(8):
                item = self.table.item(row, col)
                if item and item.text():
                    tkb[str(row + 2)][str(col + 1)] = item.text()
        
        luu_thoi_khoa_bieu(self.ma_lop, tkb)
        QMessageBox.information(self, "Thông báo", "Đã lưu thời khóa biểu thành công!")

    def cap_nhat_ma_lop(self, ma_lop_moi):
        self.ma_lop = ma_lop_moi
        self.label.setText(f"Thời khóa biểu lớp {self.ma_lop}")
        self.load_thoi_khoa_bieu()

class DiemDanhWidget(QWidget):
    def __init__(self, ma_lop, danh_sach_hs):
        super().__init__()
        self.ma_lop = ma_lop
        self.danh_sach_hs = danh_sach_hs
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Tiêu đề
        self.label = QLabel(f"Điểm danh lớp {self.ma_lop}")
        self.label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.label)

        # Chọn ngày
        date_layout = QHBoxLayout()
        date_label = QLabel("Chọn ngày:")
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_edit)
        layout.addLayout(date_layout)

        # Danh sách học sinh để điểm danh
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        # Nút lưu điểm danh
        self.button_save = QPushButton("Lưu điểm danh")
        self.button_save.clicked.connect(self.luu_diem_danh)
        layout.addWidget(self.button_save)

        self.load_danh_sach_hoc_sinh()

    def load_danh_sach_hoc_sinh(self):
        self.list_widget.clear()
        for hs in self.danh_sach_hs.values():
            if hs.ma_lop == self.ma_lop:
                item = QListWidgetItem(f"{hs.ten_hs} ({hs.ma_hs})")
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(Qt.Unchecked)
                self.list_widget.addItem(item)

    def luu_diem_danh(self):
        ngay = self.date_edit.date().toString(Qt.ISODate)
        diem_danh = {}
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            ma_hs = item.text().split('(')[1].split(')')[0]
            diem_danh[ma_hs] = "Có mặt" if item.checkState() == Qt.Checked else "Vắng mặt"
        
        luu_diem_danh(self.ma_lop, diem_danh, ngay)
        QMessageBox.information(self, "Thông báo", f"Đã lưu điểm danh ngày {ngay} thành công!")

    def cap_nhat_ma_lop(self, ma_lop_moi):
        self.ma_lop = ma_lop_moi
        self.label.setText(f"Điểm danh lớp {self.ma_lop}")
        self.load_danh_sach_hoc_sinh()
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản Lý Lớp Học")
        self.setStyleSheet(STYLESHEET)
        self.danh_sach_lop = doc_danh_sach_lop_hoc()
        self.danh_sach_hs = doc_danh_sach_hoc_sinh()
        self.init_ui()
        self.center_on_screen()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()
        header_label = QLabel("Quản Lý Lớp Học")
        header_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        # Class selection and management
        class_layout = QHBoxLayout()
        class_layout.setSpacing(10)

        class_selection_layout = QVBoxLayout()
        class_selection_layout.setSpacing(5)
        
        class_label = QLabel("Chọn lớp học:")
        class_label.setStyleSheet("font-size: 16px;")
        class_selection_layout.addWidget(class_label)

        self.combo_lop_hoc = QComboBox()
        self.combo_lop_hoc.setStyleSheet("font-size: 16px;")
        self.cap_nhat_danh_sach_lop_hoc()
        class_selection_layout.addWidget(self.combo_lop_hoc)

        class_layout.addLayout(class_selection_layout)

        class_buttons_layout = QVBoxLayout()
        class_buttons_layout.setSpacing(10)

        self.button_them_lop = QPushButton("Thêm lớp học")
        self.button_them_lop.clicked.connect(self.mo_them_lop_hoc)
        class_buttons_layout.addWidget(self.button_them_lop)

        self.button_xoa_lop = QPushButton("Xóa lớp học")
        self.button_xoa_lop.clicked.connect(self.xoa_lop_hoc)
        class_buttons_layout.addWidget(self.button_xoa_lop)

        class_layout.addLayout(class_buttons_layout)
        class_layout.addStretch()

        main_layout.addLayout(class_layout)

        # Main content
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("QTabBar::tab { height: 30px; }")
        main_layout.addWidget(self.tab_widget)

        self.combo_lop_hoc.currentTextChanged.connect(self.thay_doi_lop_hoc_chon)

        ma_lop_dau_tien = next(iter(self.danh_sach_lop), None)
        if ma_lop_dau_tien:
            self.quan_ly_hoc_vien_widget = QuanLyHocVienWidget(
                copy.deepcopy(self.danh_sach_hs), ma_lop_dau_tien, self)
            self.tab_widget.addTab(self.quan_ly_hoc_vien_widget, "Quản lý học viên")

            self.thoi_khoa_bieu_widget = ThoiKhoaBieuWidget(ma_lop_dau_tien)
            self.tab_widget.addTab(self.thoi_khoa_bieu_widget, "Thời khóa biểu")

            self.diem_danh_widget = DiemDanhWidget(ma_lop_dau_tien, self.danh_sach_hs)
            self.tab_widget.addTab(self.diem_danh_widget, "Điểm danh")

    def center_on_screen(self):
        screen = QGuiApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, 
                  (screen.height() - size.height()) // 2)

    def cap_nhat_danh_sach_lop_hoc(self):
        self.combo_lop_hoc.clear()
        danh_sach_lop_moi = doc_danh_sach_lop_hoc()
        self.danh_sach_lop = danh_sach_lop_moi
        for ma_lop, lop_hoc in self.danh_sach_lop.items():
            self.combo_lop_hoc.addItem(lop_hoc.ten_lop, ma_lop)

    def thay_doi_lop_hoc_chon(self):
        ma_lop_moi = self.combo_lop_hoc.currentData()
        if hasattr(self, 'quan_ly_hoc_vien_widget'):
            self.quan_ly_hoc_vien_widget.cap_nhat_ma_lop(ma_lop_moi)
        if hasattr(self, 'thoi_khoa_bieu_widget'):
            self.thoi_khoa_bieu_widget.cap_nhat_ma_lop(ma_lop_moi)
            self.thoi_khoa_bieu_widget.load_thoi_khoa_bieu()  # Thêm dòng này
        if hasattr(self, 'diem_danh_widget'):
            self.diem_danh_widget.cap_nhat_ma_lop(ma_lop_moi)

    def mo_them_lop_hoc(self):
        dialog = ThemLopHocDialog(self.danh_sach_lop, self)
        dialog.exec()

    def cap_nhat_danh_sach_hs(self):
        self.danh_sach_hs = doc_danh_sach_hoc_sinh()
        if hasattr(self, 'quan_ly_hoc_vien_widget'):
            self.quan_ly_hoc_vien_widget.danh_sach_hs = copy.deepcopy(self.danh_sach_hs)
            self.quan_ly_hoc_vien_widget.cap_nhat_danh_sach_hs()
    def xoa_lop_hoc(self):
        ma_lop = self.combo_lop_hoc.currentData()
        ten_lop = self.combo_lop_hoc.currentText()
        if not ma_lop:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn lớp học để xóa!")
            return

        reply = QMessageBox.question(self, 'Xác nhận xóa', f"Bạn có chắc chắn muốn xóa lớp {ten_lop}?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Xóa lớp học khỏi danh sách
            del self.danh_sach_lop[ma_lop]
            
            # Xóa tất cả học sinh thuộc lớp này
            self.danh_sach_hs = {ma_hs: hs for ma_hs, hs in self.danh_sach_hs.items() if hs.ma_lop != ma_lop}
            
            # Lưu các thay đổi
            luu_danh_sach_lop_hoc(self.danh_sach_lop)
            luu_danh_sach_hoc_sinh(self.danh_sach_hs)
            
            # Cập nhật giao diện
            self.cap_nhat_danh_sach_lop_hoc()
            self.cap_nhat_danh_sach_hs()
            
            QMessageBox.information(self, "Thông báo", f"Đã xóa lớp {ten_lop} và tất cả học sinh thuộc lớp!")
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Xác nhận thoát', 
                                    "Bạn có chắc chắn muốn thoát chương trình?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()