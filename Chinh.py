import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, Toplevel
import seaborn as sns
import matplotlib.pyplot as plt
from plot_utils import industry_highest_revenue, highest_profit_month, favorite_runtime, show_genre_data, calculate_profit, show_top, show_genre_data, show_genres_data

df = None
current_page = 0
rows_per_page = 1000  

def select_file():
    global df, current_page
    file_path = filedialog.askopenfilename(
        title="Chọn file CSV",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    if file_path:
        try:
            df = pd.read_csv(file_path)
            df["profit"] = df["revenue_adj"] - df["budget_adj"]
            df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
            current_page = 0  # Đặt lại trang hiện tại sau khi chọn file mới
            update_table()  # Cập nhật dữ liệu vào bảng
            update_pagination()  # Cập nhật các nút phân trang
            messagebox.showinfo("Thông báo", "Đã tải file CSV thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc file CSV: {e}")

def update_table():
    if df is None:
        messagebox.showerror("Lỗi", "Chưa có dữ liệu để hiển thị!")
        return
    
    # Xóa dữ liệu cũ trong bảng
    for row in tree.get_children():
        tree.delete(row)
    
    # Xác định phạm vi dòng cho trang hiện tại
    start_row = current_page * rows_per_page
    end_row = start_row + rows_per_page
    
    # Thêm dữ liệu từ DataFrame vào bảng cho trang hiện tại
    for _, row in df.iloc[start_row:end_row].iterrows():
        tree.insert("", "end", values=list(row))

# Hàm cập nhật các nút phân trang
def update_pagination():
    # Xóa các nút phân trang cũ
    for widget in pagination_frame.winfo_children():
        widget.destroy()

    # Tính tổng số trang
    total_pages = (len(df) // rows_per_page) + (1 if len(df) % rows_per_page != 0 else 0)
    
    # Giới hạn hiển thị tối đa 10 trang
    displayed_pages = min(total_pages, 10)
    
    for i in range(displayed_pages):
        page_button = tk.Button(
            pagination_frame, 
            text=f"Site {i+1}", 
            command=lambda page=i: change_page(page), 
            font=("Pacifico", 12), 
            width=10
        )
        page_button.pack(side="left", padx=5)

# Hàm thay đổi trang
def change_page(page):
    global current_page
    current_page = page
    update_table()  # Cập nhật lại bảng dữ liệu cho trang mới
    update_pagination()  # Cập nhật lại các nút phân trang

# Giao diện chính
root = tk.Tk()
root.title("Phân tích dữ liệu phim")
root.geometry("2900x1600")
root.config(bg="#f0f0f0")

# Cấu hình style Treeview
style = ttk.Style()
style.configure("Treeview", rowheight=40)  # Tăng chiều cao mỗi dòng

# Tạo khung chứa bảng và nút
frame_left = tk.Frame(root, width=700, height=900, bg="#C1CDCD")
frame_left.pack(side="left", fill="y", padx=10, pady=10)

frame_right = tk.Frame(root, width=200, height=900, bg="white")
frame_right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# Tiêu đề
tk.Label(frame_left, text="  PHÂN TÍCH DỮ LIỆU PHIM  ", font=("Pacifico", 17, "bold"), bg="#CDCDB4", bd=4, relief="raised").pack(pady=10)

# Nút chọn file
tk.Button(frame_left, text="Chọn file CSV", command=select_file, font=("Pacifico", 15), bg="#669999", borderwidth=2, relief="raised").pack(pady=10)

# Các nút chức năng
buttons = [
    ("Tính lợi nhuận của bộ phim", lambda: calculate_profit(root, df)),                 #Done
    ("Ngành công nghiệp đạt doanh thu cao nhất", lambda: industry_highest_revenue(df)), #Done
    ("Tháng nào lợi nhuận cao nhất", lambda: highest_profit_month(df)),                 #Done
    ("Thời lượng phim được yêu thích nhất", lambda: favorite_runtime(df)),              #Done

    ("Top 10 bộ phim có doanh thu cao nhất", lambda: show_top(df, "original_title", "revenue_adj", "Top 10 bộ phim có doanh thu cao nhất")),       #Done
    ("Top 10 bộ phim có ngân sách cao nhất", lambda: show_top(df, "original_title", "budget_adj", "Top 10 bộ phim có ngân sách cao nhất")), #Done
    ("Top 10 bộ phim nổi tiếng nhất", lambda: show_top(df, "original_title", "popularity", "Top 10 bộ phim nổi tiếng nhất")),               #Done

    ("Số lượng phim sản xuất theo thể loại", lambda: show_genres_data(df)),   #Done
    ("Thể loại lợi thế về tổng thể", lambda: show_genre_data(df, 'profit', "Thể loại lợi thế về lợi nhuận")),          #Done
    ("Thể loại phổ biến tổng thể", lambda: show_genre_data(df, 'popularity', "Thể loại phổ biến về tổng thể ")),       #Done
]

for text, command in buttons:
    tk.Button(
        frame_left, 
        text=text, 
        command=command, 
        font=("Pacifico", 12),  
        width= 40, 
        bg="#9999CC", 
        borderwidth=2, 
        relief="raised"
    ).pack(pady=7)


# Tạo phong cách cho thanh cuộn
style = ttk.Style()
style.theme_use('default')  # Sử dụng theme mặc định để tùy chỉnh
style.configure(
    "Vertical.TScrollbar",
    gripcount=0,
    background="#669999",  # Màu nền của thanh trượt
    troughcolor="#D3D3D3", # Màu nền của rãnh
    bordercolor="#AAAAAA", # Màu viền
    arrowcolor="white"     # Màu mũi tên
)
style.configure(
    "Horizontal.TScrollbar",
    gripcount=0,
    background="#669999",  # Màu nền của thanh trượt
    troughcolor="#D3D3D3", # Màu nền của rãnh
    bordercolor="#AAAAAA", # Màu viền
    arrowcolor="white"     # Màu mũi tên
)

# Tạo bảng Treeview trong frame_right
columns = ["id", "popularity", "original_title", "cast", "director", "runtime", 
          "genres", "production_companies", "release_date", "vote_count", "vote_average",
          "release_year", "budget_adj", "revenue_adj", "profit"]
tree = ttk.Treeview(frame_right, columns=columns, show="headings", height=25)

# Cấu hình cột
for col in columns:
    tree.heading(col, text=col, anchor="center")
    if col == 'genres':
        tree.column(col, anchor="center", width=800)
    elif col == 'cast' or col == 'production_companies':
        tree.column(col, anchor="center", width=1200)
    else:
        tree.column(col, anchor="center", width=300)

# Tạo thanh cuộn dọc và ngang với phong cách
scrollbar_y = ttk.Scrollbar(frame_right, orient="vertical", command=tree.yview, style="Vertical.TScrollbar")
scrollbar_x = ttk.Scrollbar(frame_right, orient="horizontal", command=tree.xview, style="Horizontal.TScrollbar")

# Cấu hình thanh cuộn cho Treeview
tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

# Hiển thị thanh cuộn
scrollbar_y.pack(side="right", fill="y")
scrollbar_x.pack(side="bottom", fill="x")

tree.pack(fill="both", expand=True, padx=10, pady=10)

# Tạo khung phân trang bên dưới bảng
pagination_frame = tk.Frame(frame_right, bg="white")
pagination_frame.pack(side="bottom", fill="x", pady=10)

# Chạy ứng dụng
root.mainloop()
