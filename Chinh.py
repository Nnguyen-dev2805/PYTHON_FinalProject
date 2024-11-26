import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, Toplevel

from plot_utils import (
    industry_highest_revenue,
    highest_profit_month,
    favorite_runtime,
    show_genre_data,
    calculate_profit,
    show_top,
    show_genres_data,
)

df = None
original_df = None 
current_page = 0
rows_per_page = 300

def select_file():
    global df, original_df, current_page, tree
    file_path = filedialog.askopenfilename(
        title="Chọn file CSV",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
    )
    if file_path:
        try:
            df = pd.read_csv(file_path)
            original_df = df.copy()  # Lưu dữ liệu gốc
            df["profit"] = df["revenue_adj"] - df["budget_adj"]
            df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
            current_page = 0  # Reset trang hiện tại
            create_treeview(df)  # Tạo bảng dữ liệu Treeview
            update_table()  # Hiển thị dữ liệu lên Treeview
            update_pagination()  # Tạo nút phân trang
            update_filter_columns()  # Cập nhật danh sách cột lọc
            messagebox.showinfo("Thông báo", "Đã tải file CSV thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc file CSV: {e}")


def create_treeview(dataframe):
    global tree

    # Xóa Treeview cũ (nếu có)
    for widget in frame_right.winfo_children():
        if isinstance(widget, ttk.Treeview) or isinstance(widget, ttk.Scrollbar):
            widget.destroy()

    # Tạo Treeview hiển thị dữ liệu
    columns = list(dataframe.columns)
    tree = ttk.Treeview(frame_right, columns=columns, show="headings", height=25)

    # Đặt cấu hình cột
    for col in columns:
        tree.heading(col, text=col, anchor="center")
        if col == 'cast':
            tree.column(col, anchor="center", width=1400)    
        elif col == 'director':
            tree.column(col, anchor="center", width=600)
        elif col == 'production_companies':
            tree.column(col, anchor="center", width=1600)
        elif col == 'genres':
            tree.column(col, anchor="center", width=700)
        else:
            tree.column(col, anchor="center", width=350)

    # Tạo thanh cuộn dọc và ngang
    scrollbar_y = ttk.Scrollbar(frame_right, orient="vertical", command=tree.yview)
    scrollbar_x = ttk.Scrollbar(frame_right, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x.pack(side="bottom", fill="x")

    tree.pack(fill="both", expand=True, padx=10, pady=10)


def update_table():
    if df is None:
        messagebox.showerror("Lỗi", "Chưa có dữ liệu để hiển thị!")
        return

    # Xóa dữ liệu cũ
    for row in tree.get_children():
        tree.delete(row)

    # Hiển thị dữ liệu theo trang
    start_row = current_page * rows_per_page
    end_row = start_row + rows_per_page
    for _, row in df.iloc[start_row:end_row].iterrows():
        tree.insert("", "end", values=list(row))


def update_pagination():
    # Xóa nút phân trang cũ
    for widget in pagination_frame.winfo_children():
        widget.destroy()

    # Tổng số trang
    total_pages = (len(df) // rows_per_page) + (1 if len(df) % rows_per_page != 0 else 0)

    # Tạo các nút phân trang
    for i in range(total_pages):
        page_button = tk.Button(
            pagination_frame,
            text=f"Trang {i+1}",
            command=lambda page=i: change_page(page),
            font=("Pacifico", 8),
            width=10,
        )
        page_button.pack(side="left", padx=5)


def change_page(page):
    global current_page
    current_page = page
    update_table()
    update_pagination()


def reset_data():
    global df
    if original_df is not None:
        df = original_df.copy()
        create_treeview(df)
        update_table()
        update_pagination()
        update_filter_columns()
        messagebox.showinfo("Thông báo", "Đã khôi phục dữ liệu gốc!")
    else:
        messagebox.showerror("Lỗi", "Không có dữ liệu gốc để khôi phục!")

def type_conversion(value, column_series):
    # Xác định kiểu dữ liệu của cột
    if column_series.dtype == 'int64':
        return int(value)
    elif column_series.dtype == 'float64':
        return float(value)
    elif column_series.dtype == 'object':
        return str(value)
    else:
        return value


def filter_data():
    global df
    if df is None:
        messagebox.showerror("Lỗi", "Chưa có dữ liệu để lọc!")
        return

    column = filter_column_var.get()
    condition = filter_condition_var.get()
    value = filter_value_entry.get()

    if not column or column not in df.columns:
        messagebox.showerror("Lỗi", "Vui lòng chọn một cột hợp lệ!")
        return

    try:
        filtered_df = df.copy()
        if condition == "=":
            filtered_df = filtered_df[filtered_df[column] == type_conversion(value, df[column])]
        elif condition == "!=":
            filtered_df = filtered_df[filtered_df[column] != type_conversion(value, df[column])]
        elif condition == ">":
            filtered_df = filtered_df[filtered_df[column].astype(float) > float(value)]
        elif condition == "<":
            filtered_df = filtered_df[filtered_df[column].astype(float) < float(value)]
        elif condition == "contains":
            filtered_df = filtered_df[filtered_df[column].astype(str).str.contains(value, na=False)]

        df = filtered_df
        create_treeview(df)
        update_table()
        update_pagination()
        messagebox.showinfo("Thông báo", "Lọc dữ liệu thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lọc dữ liệu không thành công: {e}")



def update_filter_columns():
    if df is not None:
        # Giới hạn cột chỉ hiển thị các cột được chỉ định
        allowed_columns = ["runtime", "popularity", "vote_count", "vote_average", "release_year", "profit", "revenue_adj", "budget_adj", "director"]
        available_columns = [col for col in df.columns if col in allowed_columns]
        filter_column_menu["values"] = available_columns



# Giao diện chính
root = tk.Tk()
root.title("   Phân tích dữ liệu phim   ")
root.geometry("3200x1700")
root.config(bg="#f0f0f0")

style = ttk.Style()
style.configure("Treeview", rowheight=40)  # Tăng chiều cao mỗi dòng

# Giao diện lọc dữ liệu
filter_frame = tk.Frame(root, bg="#C1CDCD")
filter_frame.pack(fill="x", pady=10)

tk.Label(filter_frame, text="Cột:", font=("Pacifico", 12), bg="#C1CDCD").grid(row=0, column=0, padx=5, pady=5)
filter_column_var = tk.StringVar()
filter_column_menu = ttk.Combobox(filter_frame, textvariable=filter_column_var, font=("Pacifico", 12))
filter_column_menu.grid(row=0, column=1, padx=5, pady=5)

tk.Label(filter_frame, text="Điều kiện:", font=("Pacifico", 12), bg="#C1CDCD").grid(row=0, column=2, padx=5, pady=5)
filter_condition_var = tk.StringVar()
filter_condition_menu = ttk.Combobox(filter_frame, textvariable=filter_condition_var, font=("Pacifico", 12))
filter_condition_menu["values"] = ["=", "!=", ">", "<", "contains"]
filter_condition_menu.grid(row=0, column=3, padx=5, pady=5)

tk.Label(filter_frame, text="Giá trị:", font=("Pacifico", 12), bg="#C1CDCD").grid(row=0, column=4, padx=5, pady=5)
filter_value_entry = tk.Entry(filter_frame, font=("Pacifico", 12))
filter_value_entry.grid(row=0, column=5, padx=5, pady=5)

tk.Button(filter_frame, text="Áp dụng lọc", command=filter_data, font=("Pacifico", 12), bg="#669999", relief="raised").grid(row=0, column=6, padx=10, pady=5)
tk.Button(filter_frame, text="Khôi phục dữ liệu", command=reset_data, font=("Pacifico", 12), bg="#CC6666", relief="raised").grid(row=0, column=7, padx=10, pady=5)

# Giao diện bảng và nút
frame_left = tk.Frame(root, width=300, bg="#C1CDCD")
frame_left.pack(side="left", fill="y", padx=10, pady=10)

frame_right = tk.Frame(root, width=300, bg="white")
frame_right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

tk.Label(frame_left, text="   Phân tích dữ liệu phim   ", font=("Pacifico", 17, "bold"), bg="#CDCDB4", relief="raised").pack(pady=10)
tk.Button(frame_left, text="Chọn file CSV", command=select_file, font=("Pacifico", 15), bg="#669999").pack(pady=10)

pagination_frame = tk.Frame(frame_right, bg="white")
pagination_frame.pack(side="bottom", fill="x", pady=10)


def delete_selected_row():
    global df
    if df is None:
        messagebox.showerror("Thông báo", "Chưa có dữ liệu để xóa!")
        return
    
    selected_item = tree.selection()  # Lấy dòng được chọn
    if selected_item:  # Kiểm tra có dòng nào được chọn không
        try:
            # Xóa dòng từ DataFrame
            row_index = tree.index(selected_item[0])  # Tìm chỉ số của dòng được chọn trong Treeview
            # global df
            df = df.drop(df.index[current_page * rows_per_page + row_index])  # Tính chỉ số trong DataFrame và xóa
            df.reset_index(drop=True, inplace=True)  # Đặt lại chỉ số của DataFrame
            
            # Xóa dòng từ Treeview
            tree.delete(selected_item[0])
            messagebox.showinfo("Thông báo", "Đã xóa dòng dữ liệu thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa dòng dữ liệu: {e}")
    else:
        messagebox.showwarning("Chú ý", "Vui lòng chọn dòng dữ liệu để xóa!")


def edit_selected_row():
    global df
    if df is None:
        messagebox.showerror("Thông báo", "Chưa có dữ liệu để xóa!")
        return
    
    selected_item = tree.selection()  # Lấy dòng được chọn
    if selected_item:
        # Mở cửa sổ mới để nhập dữ liệu
        edit_window = Toplevel(root)
        edit_window.title("Chỉnh sửa dữ liệu")
        edit_window.geometry("700x700")

        # Lấy thông tin dòng hiện tại
        row_index = tree.index(selected_item[0])
        current_values = df.iloc[current_page * rows_per_page + row_index]
        
        # Tạo nhãn và trường nhập cho mỗi cột
        entries = {}
        for i, col in enumerate(df.columns):
            tk.Label(edit_window, text=col).grid(row=i, column=0)
            entry = tk.Entry(edit_window)
            entry.grid(row=i, column=1)
            entry.insert(0, str(current_values[col]))
            entries[col] = entry

        # Hàm để cập nhật dữ liệu
        def update_data():
            try:
                # Cập nhật DataFrame
                for col, entry in entries.items():
                    df.at[current_page * rows_per_page + row_index, col] = entry.get()

                # Cập nhật Treeview
                tree.item(selected_item[0], values=[entry.get() for entry in entries.values()])
                messagebox.showinfo("Thông báo", "Dữ liệu đã được cập nhật thành công!")
                edit_window.destroy()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật dữ liệu: {e}")

        # Nút cập nhật
        tk.Button(edit_window, text="Cập nhật", command=update_data).grid(row=len(df.columns), column=1)

    else:
        messagebox.showwarning("Chú ý", "Vui lòng chọn dòng dữ liệu để chỉnh sửa!")



# Các nút chức năng
buttons = [
    ("Tính lợi nhuận của bộ phim", lambda: calculate_profit(root, df)),                 # Done
    ("Ngành công nghiệp phim đạt doanh thu cao nhất", lambda: industry_highest_revenue(df)), # Done
    ("Tháng có lợi nhuận cao nhất", lambda: highest_profit_month(df)),                 # Done
    ("Thời lượng phim được yêu thích nhất", lambda: favorite_runtime(df)),              # Done
    ("Top 10 bộ phim có doanh thu cao nhất", lambda: show_top(df, "original_title", "revenue_adj", "Top 10 bộ phim có doanh thu cao nhất")), # Done
    ("Top 10 bộ phim có ngân sách cao nhất", lambda: show_top(df, "original_title", "budget_adj", "Top 10 bộ phim có ngân sách cao nhất")), # Done
    ("Top 10 bộ phim nổi tiếng nhất", lambda: show_top(df, "original_title", "popularity", "Top 10 bộ phim nổi tiếng nhất")), # Done
    ("Số lượng phim sản xuất theo thể loại", lambda: show_genres_data(df)), # Done
    ("Thể loại lợi thế về tổng thể", lambda: show_genre_data(df, 'profit', "Thể loại lợi thế về lợi nhuận")), # Done
    ("Thể loại phổ biến tổng thể", lambda: show_genre_data(df, 'popularity', "Thể loại phổ biến về tổng thể")), # Done
]

tk.Button(frame_left, text="Xóa dòng dữ liệu", command=delete_selected_row, font=("Pacifico", 15), bg="#CC6666", borderwidth=2, relief="raised").pack(pady=10)
tk.Button(frame_left, text="Chỉnh sửa dữ liệu", command=edit_selected_row, font=("Pacifico", 15), bg="#CC9966", borderwidth=2, relief="raised").pack(pady=10)

for text, command in buttons:
    tk.Button(
        frame_left, 
        text=text, 
        command=command, 
        font=("Pacifico", 12),  
        width=40, 
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
    arrowcolor="black",     # Màu mũi tên
    arrowsize = 30
)

style.configure(
    "Horizontal.TScrollbar",
    gripcount=0,
    background="#669999",  # Màu nền của thanh trượt
    troughcolor="#D3D3D3", # Màu nền của rãnh
    bordercolor="#AAAAAA", # Màu viền
    arrowcolor="black",     # Màu mũi tên
    arrowsize = 30
)

# Tạo khung phân trang bên dưới bảng
pagination_frame = tk.Frame(frame_right, bg="white")
pagination_frame.pack(side="bottom", fill="x", pady=10)

root.mainloop()
