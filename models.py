class HocSinh:
    def __init__(self, ma_hs, ten_hs, ma_lop, so_buoi_hoc=0, sdt=""):
        self.ma_hs = ma_hs
        self.ten_hs = ten_hs
        self.ma_lop = ma_lop
        self.so_buoi_hoc = so_buoi_hoc
        self.sdt = sdt
        self.diem_danh = {}
class LopHoc:
    def __init__(self, ma_lop, ten_lop):
        self.ma_lop = ma_lop
        self.ten_lop = ten_lop

    def __str__(self):
        return f"Lớp: {self.ten_lop} (Mã: {self.ma_lop})"