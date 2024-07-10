import sys
import datetime
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                               QPushButton, QVBoxLayout, QHBoxLayout,
                               QComboBox, QCheckBox, QMessageBox,
                               QListWidget, QDialog, QTableWidget, QTableWidgetItem, QSpinBox,
                               QTabWidget, QListWidgetItem,QMainWindow)
from PySide6.QtGui import QFont
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt
import copy
from file_manager import doc_diem_danh
from models import HocSinh, LopHoc
from file_manager import (doc_danh_sach_lop_hoc, luu_danh_sach_lop_hoc,
                          luu_diem_danh, doc_thoi_khoa_bieu, luu_thoi_khoa_bieu,
                          doc_danh_sach_hoc_sinh, luu_danh_sach_hoc_sinh, doc_diem_danh)
from xu_ly import xuat_diem_danh_excel
class ThemSuaHocVienDialog(QDialog):
    def __init__(self, ma_lop, danh_sach_hs, main_window, hoc_sinh_hien_tai=None):
        super().__init__()
        self.ma_lop = ma_lop
        self.danh_sach_hs = danh_sach_hs
        self.main_window = main_window
        self.hoc_sinh_hien_tai = hoc_sinh_hien_tai

        self.setWindowTitle(f"{'Sửa' if hoc_sinh_hien_tai else 'Thêm'} học viên lớp {ma_lop}")
        self.init_ui()

    def init_ui(self):
        self.label_ma_hs = QLabel("Mã học sinh:")
        self.edit_ma_hs = QLineEdit()
        self.label_ten_hs = QLabel("Tên học sinh:")
        self.edit_ten_hs = QLineEdit()
        self.label_so_buoi_hoc = QLabel("Số buổi học:")
        self.spin_so_buoi_hoc = QSpinBox()
        self.spin_so_buoi_hoc.setMinimum(0)
        self.spin_so_buoi_hoc.setMaximum(31)
        self.label_sdt = QLabel("Số điện thoại:")
        self.edit_sdt = QLineEdit()

        if self.hoc_sinh_hien_tai:
            self.edit_ma_hs.setText(self.hoc_sinh_hien_tai.ma_hs)
            self.edit_ten_hs.setText(self.hoc_sinh_hien_tai.ten_hs)
            self.spin_so_buoi_hoc.setValue(self.hoc_sinh_hien_tai.so_buoi_hoc)
            self.edit_sdt.setText(self.hoc_sinh_hien_tai.sdt)

        button_luu = QPushButton("Lưu" if self.hoc_sinh_hien_tai else "Thêm")
        button_luu.clicked.connect(self.luu_hoc_sinh)

        layout = QVBoxLayout()
        layout.addWidget(self.label_ma_hs)
        layout.addWidget(self.edit_ma_hs)
        layout.addWidget(self.label_ten_hs)
        layout.addWidget(self.edit_ten_hs)
        layout.addWidget(self.label_so_buoi_hoc)
        layout.addWidget(self.spin_so_buoi_hoc)
        layout.addWidget(self.label_sdt)
        layout.addWidget(self.edit_sdt)
        layout.addWidget(button_luu)
        self.setLayout(layout)

    def luu_hoc_sinh(self):
        ma_hs = self.edit_ma_hs.text()
        ten_hs = self.edit_ten_hs.text()
        so_buoi_hoc = self.spin_so_buoi_hoc.value()
        sdt = self.edit_sdt.text()

        if not ma_hs or not ten_hs:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin học sinh!")
            return

        hoc_sinh = HocSinh(ma_hs, ten_hs, self.ma_lop, so_buoi_hoc, sdt)
        self.danh_sach_hs[ma_hs] = hoc_sinh
        luu_danh_sach_hoc_sinh(self.danh_sach_hs)
        self.main_window.cap_nhat_danh_sach_hs()
        self.close()


class ThemLopHocDialog(QDialog):
    def __init__(self, danh_sach_lop, main_window):
        super().__init__()
        self.danh_sach_lop = danh_sach_lop
        self.main_window = main_window
        self.setWindowTitle("Thêm Lớp Học")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.label_ma_lop = QLabel("Mã lớp học:")
        self.edit_ma_lop = QLineEdit()
        layout.addWidget(self.label_ma_lop)
        layout.addWidget(self.edit_ma_lop)

        self.label_ten_lop = QLabel("Tên lớp học:")
        self.edit_ten_lop = QLineEdit()
        layout.addWidget(self.label_ten_lop)
        layout.addWidget(self.edit_ten_lop)

        self.button_them = QPushButton("Thêm")
        self.button_them.clicked.connect(self.them_lop_hoc)
        layout.addWidget(self.button_them)

    def them_lop_hoc(self):
        ma_lop_moi = self.edit_ma_lop.text()
        ten_lop_moi = self.edit_ten_lop.text()
        if ma_lop_moi and ten_lop_moi:
            if ma_lop_moi not in self.danh_sach_lop:
                lop_hoc = LopHoc(ma_lop_moi, ten_lop_moi)
                self.danh_sach_lop[ma_lop_moi] = lop_hoc
                luu_danh_sach_lop_hoc(self.danh_sach_lop)
                self.main_window.cap_nhat_danh_sach_lop_hoc()
                QMessageBox.information(self, "Thông báo", f"Đã thêm lớp học {ten_lop_moi}!")
                self.close()
            else:
                QMessageBox.warning(self, "Lỗi", f"Lớp học {ten_lop_moi} đã tồn tại!")
        else:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập mã và tên lớp học!")


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
    def __init__(self, ten_lop, danh_sach_hs):
        super().__init__()
        self.ten_lop = ten_lop
        self.danh_sach_hs = danh_sach_hs
        self.setWindowTitle(f"Điểm danh lớp {ten_lop}")
        self.init_ui()

    def init_ui(self):
        # Lọc danh sách học sinh thuộc lớp hiện tại
        hoc_sinh_lop = [
            hs for hs in self.danh_sach_hs.values() if hs.ma_lop == self.ten_lop]

        if not hoc_sinh_lop:
            QMessageBox.warning(self, "Lỗi", f"Lớp {self.ten_lop} chưa có học viên!")
            return

        self.checkboxes = {}
        vbox = QVBoxLayout()

        for hoc_sinh in hoc_sinh_lop:
            checkbox = QCheckBox(hoc_sinh.ten_hs)
            self.checkboxes[hoc_sinh.ma_hs] = checkbox
            vbox.addWidget(checkbox)

        self.button_luu_diem_danh = QPushButton("Lưu điểm danh")
        self.button_luu_diem_danh.clicked.connect(self.luu_diem_danh)
        vbox.addWidget(self.button_luu_diem_danh)

        self.setLayout(vbox)

    def luu_diem_danh(self):
        diem_danh = {}
        for ma_hs, checkbox in self.checkboxes.items():
            if checkbox.isChecked():
                diem_danh[ma_hs] = "Có mặt"
            else:
                diem_danh[ma_hs] = "Vắng mặt"
        luu_diem_danh(self.ten_lop, diem_danh)
        QMessageBox.information(self, "Thông báo", "Đã lưu điểm danh!")


class ThoiKhoaBieuDialog(QDialog):
    def __init__(self, ma_lop):
        super().__init__()
        self.ma_lop = ma_lop
        self.setWindowTitle(f"Thời Khóa Biểu Lớp {ma_lop}")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.table_tkb = QTableWidget()
        self.table_tkb.setRowCount(6)  # Thứ 2 đến thứ 7
        self.table_tkb.setColumnCount(10)  # 7 khung giờ học

        # Đặt nhãn cho hàng (thứ trong tuần)
        self.table_tkb.setVerticalHeaderLabels(["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7"])

        # Đặt nhãn cho cột (khung giờ học)
        khung_gio = ["8:00-9:00", "9:00-10:00", "10:00-11:00", "14:00-15:00", "15:00-16:00", "16:00-17:00", "17:00-18:00","18:00-19:00","19:00-20:00","20:00-21:00"]
        self.table_tkb.setHorizontalHeaderLabels(khung_gio)

        layout.addWidget(self.table_tkb)

        self.button_luu_tkb = QPushButton("Lưu")
        self.button_luu_tkb.clicked.connect(self.luu_thoi_khoa_bieu)
        layout.addWidget(self.button_luu_tkb)

        # Đọc và hiển thị thời khóa biểu từ file (nếu có)
        self.hien_thi_thoi_khoa_bieu()

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

        self.label_lop_hoc = QLabel(f"Quản lý học viên lớp {self.ma_lop}")
        layout.addWidget(self.label_lop_hoc)

        button_layout = QHBoxLayout()
        self.button_them = QPushButton("Thêm học viên")
        self.button_them.clicked.connect(self.mo_them_hoc_vien)
        self.button_sua = QPushButton("Sửa học viên")
        self.button_sua.clicked.connect(self.mo_sua_hoc_vien)
        self.button_xoa = QPushButton("Xóa học viên")
        self.button_xoa.clicked.connect(self.mo_xoa_hoc_vien)
        self.button_diem_danh = QPushButton("Điểm danh")
        self.button_diem_danh.clicked.connect(self.mo_diem_danh)
        self.button_thoi_khoa_bieu = QPushButton("Thời khóa biểu")
        self.button_thoi_khoa_bieu.clicked.connect(self.mo_thoi_khoa_bieu)
        self.button_xuat_diem_danh = QPushButton("Xuất phiếu điểm danh")
        self.button_xuat_diem_danh.clicked.connect(self.xuat_phieu_diem_danh)

        button_layout.addWidget(self.button_them)
        button_layout.addWidget(self.button_sua)
        button_layout.addWidget(self.button_xoa)
        button_layout.addWidget(self.button_diem_danh)
        button_layout.addWidget(self.button_thoi_khoa_bieu)
        button_layout.addWidget(self.button_xuat_diem_danh)

        layout.addLayout(button_layout)

        self.list_widget = QListWidget(self)
        layout.addWidget(self.list_widget)

        self.cap_nhat_danh_sach_hs()

    def mo_them_hoc_vien(self):
        ThemSuaHocVienDialog(self.ma_lop, self.danh_sach_hs, self.main_window).exec()

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
            self.cap_nhat_danh_sach_hs()  # Cập nhật lại danh sách sau khi sửa
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
        now = datetime.datetime.now()
        thang = now.month
        nam = now.year
        
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
    def __init__(self, danh_sach_lop, main_window):
        super().__init__()
        self.danh_sach_lop = danh_sach_lop
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        self.label_quan_ly_lop = QLabel("Quản lý lớp học")
        self.button_diem_danh = QPushButton("Điểm danh")
        self.button_diem_danh.clicked.connect(self.mo_diem_danh)
        self.button_thoi_khoa_bieu = QPushButton("Thời khóa biểu")
        self.button_thoi_khoa_bieu.clicked.connect(self.mo_thoi_khoa_bieu)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label_quan_ly_lop)
        vbox.addWidget(self.button_diem_danh)
        vbox.addWidget(self.button_thoi_khoa_bieu)
        self.setLayout(vbox)

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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản Lý Lớp Học")
        self.danh_sach_lop = doc_danh_sach_lop_hoc()
        self.danh_sach_hs = doc_danh_sach_hoc_sinh()
        self.init_ui()
        self.center_on_screen()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        top_layout = QHBoxLayout()
        self.combo_lop_hoc = QComboBox()
        self.cap_nhat_danh_sach_lop_hoc()
        top_layout.addWidget(self.combo_lop_hoc)
        
        self.button_them_lop = QPushButton("Thêm lớp học")
        self.button_them_lop.clicked.connect(self.mo_them_lop_hoc)
        top_layout.addWidget(self.button_them_lop)

        main_layout.addLayout(top_layout)

        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        self.combo_lop_hoc.currentTextChanged.connect(self.thay_doi_lop_hoc_chon)

        ma_lop_dau_tien = next(iter(self.danh_sach_lop), None)
        if ma_lop_dau_tien:
            self.quan_ly_hoc_vien_widget = QuanLyHocVienWidget(
                copy.deepcopy(self.danh_sach_hs), ma_lop_dau_tien, self)
            self.tab_widget.addTab(self.quan_ly_hoc_vien_widget, "Quản lý học viên")

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

    def mo_them_lop_hoc(self):
        dialog = ThemLopHocDialog(self.danh_sach_lop, self)
        dialog.exec()

    def cap_nhat_danh_sach_hs(self):
        self.danh_sach_hs = doc_danh_sach_hoc_sinh()
        if hasattr(self, 'quan_ly_hoc_vien_widget'):
            self.quan_ly_hoc_vien_widget.danh_sach_hs = copy.deepcopy(self.danh_sach_hs)
            self.quan_ly_hoc_vien_widget.cap_nhat_danh_sach_hs()