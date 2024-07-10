import os
import datetime
import json
from models import HocSinh, LopHoc

def lay_duong_dan_file(ten_file):
    """Lấy đường dẫn tuyệt đối đến file trong thư mục hiện tại."""
    thu_muc_hien_tai = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(thu_muc_hien_tai, ten_file)

def doc_danh_sach_hoc_sinh(ten_file="hoc_sinh.txt"):
    """Đọc dữ liệu học sinh từ file."""
    danh_sach_hs = {}
    duong_dan_file = lay_duong_dan_file(ten_file)
    try:
        with open(duong_dan_file, "r", encoding='utf-8') as f:
            for line in f:
                ma_hs, ten_hs, ma_lop, so_buoi_hoc, sdt = line.strip().split("|")
                hoc_sinh = HocSinh(ma_hs, ten_hs, ma_lop, int(so_buoi_hoc), sdt)
                danh_sach_hs[ma_hs] = hoc_sinh
    except FileNotFoundError:
        print(f"File '{ten_file}' không tồn tại. Tạo danh sách học sinh mới.")
    except PermissionError:
        print(f"Không có quyền truy cập file '{ten_file}'.")
    except Exception as e:
        print(f"Lỗi khi đọc dữ liệu học sinh: {e}")
    return danh_sach_hs

def doc_danh_sach_lop_hoc(ten_file="lop_hoc.txt"):
    """Đọc dữ liệu lớp học từ file."""
    danh_sach_lop = {}
    duong_dan_file = lay_duong_dan_file(ten_file)
    try:
        with open(duong_dan_file, "r", encoding='utf-8') as f:
            for line in f:
                ma_lop, ten_lop = line.strip().split("|")
                lop_hoc = LopHoc(ma_lop, ten_lop)
                danh_sach_lop[ma_lop] = lop_hoc
    except FileNotFoundError:
        print(f"File '{ten_file}' không tồn tại. Tạo danh sách lớp học mới.")
    except PermissionError:
        print(f"Không có quyền truy cập file '{ten_file}'.")
    except Exception as e:
        print(f"Lỗi khi đọc dữ liệu lớp học: {e}")
    return danh_sach_lop

def luu_danh_sach_hoc_sinh(danh_sach_hs, ten_file="hoc_sinh.txt"):
    """Lưu danh sách học sinh vào file."""
    duong_dan_file = lay_duong_dan_file(ten_file)
    try:
        with open(duong_dan_file, "w", encoding='utf-8') as f:
            for ma_hs, hoc_sinh in danh_sach_hs.items():
                f.write(f"{hoc_sinh.ma_hs}|{hoc_sinh.ten_hs}|{hoc_sinh.ma_lop}|{hoc_sinh.so_buoi_hoc}|{hoc_sinh.sdt}\n")
        print(f"Đã lưu danh sách học sinh vào file '{ten_file}'.")
    except PermissionError:
        print(f"Không có quyền ghi file '{ten_file}'.")
    except Exception as e:
        print(f"Lỗi khi lưu danh sách học sinh: {e}")

def luu_danh_sach_lop_hoc(danh_sach_lop, ten_file="lop_hoc.txt"):
    """Lưu danh sách lớp học vào file."""
    duong_dan_file = lay_duong_dan_file(ten_file)
    try:
        with open(duong_dan_file, "w", encoding='utf-8') as f:
            for ma_lop, lop_hoc in danh_sach_lop.items():
                f.write(f"{lop_hoc.ma_lop}|{lop_hoc.ten_lop}\n")
        print(f"Đã lưu danh sách lớp học vào file '{ten_file}'.")
    except PermissionError:
        print(f"Không có quyền ghi file '{ten_file}'.")
    except Exception as e:
        print(f"Lỗi khi lưu danh sách lớp học: {e}")

def luu_diem_danh(ma_lop, diem_danh):
    """Lưu điểm danh của lớp vào file JSON theo tháng."""
    now = datetime.datetime.now()
    thang = now.month
    nam = now.year
    ten_file = f"diem_danh_{ma_lop}_{thang}_{nam}.json"
    duong_dan_file = lay_duong_dan_file(ten_file)

    try:
        with open(duong_dan_file, "w", encoding='utf-8') as f:
            json.dump(diem_danh, f, ensure_ascii=False, indent=4)
        print(f"Đã lưu điểm danh vào file: {duong_dan_file}")
    except PermissionError:
        print(f"Không có quyền ghi file '{ten_file}'.")
    except Exception as e:
        print(f"Lỗi khi lưu điểm danh: {e}")

def luu_thoi_khoa_bieu(ma_lop, thoi_khoa_bieu, ten_file=None):
    if ten_file is None:
        ten_file = f"thoi_khoa_bieu_{ma_lop}.json"
    duong_dan_file = lay_duong_dan_file(ten_file)
    try:
        with open(duong_dan_file, "w", encoding='utf-8') as f:
            json.dump(thoi_khoa_bieu, f, ensure_ascii=False, indent=4)
        print(f"Đã lưu thời khóa biểu lớp {ma_lop} vào file '{ten_file}'.")
    except PermissionError:
        print(f"Không có quyền ghi file '{ten_file}'.")
    except Exception as e:
        print(f"Lỗi khi lưu thời khóa biểu: {e}")

def doc_thoi_khoa_bieu(ma_lop, ten_file=None):
    if ten_file is None:
        ten_file = f"thoi_khoa_bieu_{ma_lop}.json"
    duong_dan_file = lay_duong_dan_file(ten_file)
    try:
        with open(duong_dan_file, "r", encoding='utf-8') as f:
            tkb = json.load(f)
        return tkb
    except FileNotFoundError:
        print(f"File thời khóa biểu '{ten_file}' không tồn tại. Tạo thời khóa biểu mới.")
        return {}
    except json.JSONDecodeError:
        print(f"Lỗi định dạng JSON trong file '{ten_file}'. Tạo thời khóa biểu mới.")
        return {}
    except Exception as e:
        print(f"Lỗi khi đọc thời khóa biểu: {e}")
        return {}
    
def doc_diem_danh(ma_lop, thang, nam):
    ten_file = f"diem_danh_{ma_lop}_{thang}_{nam}.json"
    duong_dan_file = lay_duong_dan_file(ten_file)
    try:
        with open(duong_dan_file, "r", encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File điểm danh '{ten_file}' không tồn tại.")
        return {}
    except json.JSONDecodeError:
        print(f"Lỗi định dạng JSON trong file '{ten_file}'.")
        return {}
    except Exception as e:
        print(f"Lỗi khi đọc dữ liệu điểm danh: {e}")
        return {}