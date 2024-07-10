from models import HocSinh
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import calendar
import datetime
def clean_filename(filename):
    """Remove invalid characters from filename"""
    return "".join(c for c in filename if c.isalnum() or c in (' ', '_', '-'))

def xuat_diem_danh_excel(ma_lop, ten_lop, danh_sach_diem_danh, thang, nam):
    """Xuất điểm danh của lớp trong tháng sang file Excel."""

    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = f"Diem Danh {clean_filename(ten_lop)} - Thang {thang}-{nam}"

    # Định dạng cho header
    header_font = Font(bold=True)
    header_alignment = Alignment(horizontal='center', vertical='center')
    border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

    # Thêm tiêu đề
    sheet.merge_cells('A1:D1')
    title_cell = sheet['A1']
    title_cell.value = f"PHIẾU ĐIỂM DANH LỚP {ten_lop.upper()} - THÁNG {thang}/{nam}"
    title_cell.font = Font(bold=True, size=14)
    title_cell.alignment = Alignment(horizontal='center', vertical='center')

    # Ghi header
    headers = ["STT", "Họ và tên"]
    for i, header in enumerate(headers, start=1):
        cell = sheet.cell(row=3, column=i, value=header)
        cell.font = header_font
        cell.alignment = header_alignment
        cell.border = border

    # Tìm số ngày trong tháng
    _, days_in_month = calendar.monthrange(nam, thang)

    # Ghi các ngày trong tháng vào header
    for day in range(1, days_in_month + 1):
        cell = sheet.cell(row=3, column=day + 2, value=day)
        cell.font = header_font
        cell.alignment = header_alignment
        cell.border = border

    # Ghi cột tổng số buổi đi học
    total_column = days_in_month + 3
    cell = sheet.cell(row=3, column=total_column, value="Tổng số buổi đi học")
    cell.font = header_font
    cell.alignment = header_alignment
    cell.border = border

    if not danh_sach_diem_danh:
        print("Danh sách điểm danh trống.")
        return

    row = 4
    for hoc_sinh in danh_sach_diem_danh:
        if not isinstance(hoc_sinh, HocSinh):
            print(f"Bỏ qua dữ liệu không hợp lệ: {hoc_sinh}")
            continue
        
        sheet.cell(row=row, column=1, value=row - 3).border = border
        sheet.cell(row=row, column=2, value=hoc_sinh.ten_hs).border = border

        total_days_present = 0
        for day in range(1, days_in_month + 1):
            cell = sheet.cell(row=row, column=day + 2)
            diem_danh_ngay = hoc_sinh.diem_danh.get(str(day), "")
            if isinstance(diem_danh_ngay, str) and diem_danh_ngay.lower() == "có mặt":
                cell.value = "X"
                total_days_present += 1
            cell.alignment = Alignment(horizontal='center')
            cell.border = border

        # Ghi tổng số buổi đi học
        sheet.cell(row=row, column=total_column, value=total_days_present).border = border

        row += 1

    # Tự động điều chỉnh độ rộng cột
    for column_cells in sheet.columns:
        length = max(len(str(cell.value)) for cell in column_cells if not isinstance(cell, openpyxl.cell.MergedCell))
        if length > 0:
            column_letter = openpyxl.utils.get_column_letter(column_cells[0].column)
            adjusted_width = (length + 2)
            sheet.column_dimensions[column_letter].width = adjusted_width

    # Lưu file Excel
    ten_file = f"diem_danh_{clean_filename(ten_lop)}_{thang}_{nam}.xlsx"
    try:
        wb.save(ten_file)
        print(f"Đã xuất điểm danh sang file: {ten_file}")
    except PermissionError:
        print(f"Không có quyền ghi file '{ten_file}'.")
    except Exception as e:
        print(f"Lỗi khi xuất file Excel: {e}")