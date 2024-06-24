import cv2
from pyzbar.pyzbar import decode
import pandas as pd
import threading
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog

# Các biến toàn cục
cap = cv2.VideoCapture(0)
#excel_data = pd.read_excel('database.xlsx')
excel_data = pd.DataFrame()  # Initialize with an empty DataFrame

def change_database_path():
    global excel_data
    file_path = filedialog.askopenfilename(title="Select Database", filetypes=[("Excel files", "*.xlsx;*.xls")])

    if file_path:
        excel_data = pd.read_excel(file_path)
        print(f"Database changed to: {file_path}")


def set_auto_focus():
    # Kiểm tra xem camera có hỗ trợ auto focus không
    if cap.isOpened() and hasattr(cv2, 'CAP_PROP_AUTOFOCUS'):
        # Bật chế độ tự động lấy nét
        cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
        print("Đã bật chức năng tự động lấy nét (Auto Focus)")

def check_order():
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    barcodes = decode(gray)

    for barcode in barcodes:
        barcode_info = str(barcode.data.decode('utf-8'))  # Chuyển đổi thành chuỗi văn bản

        if barcode_info in excel_data['Mã vận đơn'].values:
            row = excel_data.loc[excel_data['Mã vận đơn'] == barcode_info]
            ten_nguoi_nhan = row['Tên người nhận'].values[0]
            dia_chi = row['Địa chỉ'].values[0]
            san_tmdt = row['Sàn TMĐT'].values[0]
            don_vi_van_chuyen = row['Đơn vị vận chuyển'].values[0]
            mo_ta = row['Mô tả'].values[0]

            label_ten_nguoi_nhan.config(text=f"Tên người nhận: {ten_nguoi_nhan}")
            label_dia_chi.config(text=f"Địa chỉ: {dia_chi}")
            label_san_tmdt.config(text=f"Sàn TMĐT: {san_tmdt}")
            label_don_vi_van_chuyen.config(text=f"Đơn vị vận chuyển: {don_vi_van_chuyen}")
            label_mo_ta.config(text=f"Mô tả: {mo_ta}")

        else:
            print("Không tìm thấy thông tin tương ứng")

    # Cập nhật frame sau khi xử lý mã vạch
    update_frame()

def update_frame():
    _, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)
    img = ImageTk.PhotoImage(image=img)
    panel.config(image=img)
    panel.image = img
    panel.after(10, check_order)  # Lặp lại cập nhật frame

def on_click():
    threading.Thread(target=check_order).start()

# Tạo giao diện
window = tk.Tk()
window.title("QR Scanner")
window.geometry("800x600")

# Hiển thị video
panel = tk.Label(window)
panel.grid(row=0, column=0, rowspan=6)
update_frame()  # Khởi chạy cập nhật frame

# Hiển thị các thông tin
label_ten_nguoi_nhan = tk.Label(window, text="Tên người nhận: ")
label_ten_nguoi_nhan.grid(row=0, column=1)

label_dia_chi = tk.Label(window, text="Địa chỉ: ")
label_dia_chi.grid(row=1, column=1)

label_san_tmdt = tk.Label(window, text="Sàn TMĐT: ")
label_san_tmdt.grid(row=2, column=1)

label_don_vi_van_chuyen = tk.Label(window, text="Đơn vị vận chuyển: ")
label_don_vi_van_chuyen.grid(row=3, column=1)

label_mo_ta = tk.Label(window, text="Mô tả: ")
label_mo_ta.grid(row=4, column=1)

# Tạo button
#button = tk.Button(window, text="Check Đơn", command=on_click)
#button.grid(row=5, column=1)
button_change_database = tk.Button(window, text="Change Database", command=change_database_path)
button_change_database.grid(row=6, column=1)
# Bắt đầu luồng hiển thị camera
threading.Thread(target=set_auto_focus).start()

window.mainloop()
