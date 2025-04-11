import pandas as pd
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import ttk
from tkinter import filedialog, messagebox, Toplevel
from pandastable import Table
import math
from plot_utils import (
    gov_exp_pct_gdp,
    Top_lit_rate_adult_pct,
    Top_gov_exp_by_country,
    Rela_GovExp_LitRate,
    Pie_gov_exp,
    Top_max_Pupil_Teacher_pri,
    Top_min_Pupil_Teacher_pri,
    Pupil_Teacher_pri_sec,
)

df = None
original_df = None 
current_page = 0
rows_per_page = 300

VALID_COUNTRIES = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", 
    "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", 
    "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", 
    "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", 
    "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", 
    "Chad", "Chile", "China", "Colombia", "Comoros", "Congo (Congo-Brazzaville)", "Congo (Democratic Republic of the)", 
    "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czechia (Czech Republic)", "Denmark", "Djibouti", 
    "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", 
    "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France", 
    "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", 
    "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", 
    "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", 
    "Kenya", "Kiribati", "Korea (North)", "Korea (South)", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", 
    "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", 
    "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", 
    "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", 
    "Myanmar (formerly Burma)", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", 
    "Niger", "Nigeria", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea", 
    "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", 
    "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", 
    "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", 
    "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Sudan", "Spain", "Sri Lanka", 
    "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", 
    "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", 
    "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States of America", "Uruguay", 
    "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Viet Nam", "Yemen", "Zambia", "Zimbabwe"
]


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
            current_page = 0  # Reset trang hiện tại
            create_treeview(df)  # Tạo bảng dữ liệu Treeview
            update_table()  # Hiển thị dữ liệu lên Treeview
            update_pagination()  # Tạo nút phân trang
            update_filter_columns()  # Cập nhật danh sách cột lọc
            refresh_describe_combobox() # Cập nhật danh sách phân tích
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
        tree.heading(col, text=col, anchor="center", command=lambda _col=col:sort_column(tree,_col,sort_states.get(_col,False)))
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
    try:
        # Kiểm tra kiểu dữ liệu của cột và chuyển đổi giá trị tương ứng
        if column_series.dtype == 'int64':
            return int(value)  # Chuyển giá trị thành số nguyên
        elif column_series.dtype == 'float64':
            return float(value)  # Chuyển giá trị thành số thực
        elif column_series.dtype == 'object':
            return str(value)  # Chuyển giá trị thành chuỗi
        else:
            return value  # Nếu không phải kiểu dữ liệu phổ biến, trả về giá trị gốc
    except (ValueError, TypeError) as e:
        messagebox.showerror("Lỗi chuyển đổi", f"Không thể chuyển đổi giá trị '{value}' sang kiểu dữ liệu '{column_series.dtype}': {e}")
        return None  # Trả về None nếu không thể chuyển đổi



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

        # Kiểm tra loại điều kiện và áp dụng bộ lọc tương ứng
        if condition == "=":
            filtered_df = filtered_df[filtered_df[column] == type_conversion(value, df[column])]
        elif condition == "!=":
            filtered_df = filtered_df[filtered_df[column] != type_conversion(value, df[column])]
        elif condition == ">":
            filtered_df = filtered_df[filtered_df[column].astype(float, errors='ignore') > float(value)]
        elif condition == "<":
            filtered_df = filtered_df[filtered_df[column].astype(float, errors='ignore') < float(value)]
        elif condition == "contains":
            filtered_df = filtered_df[filtered_df[column].astype(str).str.contains(value, na=False, case=False)]

        # Cập nhật lại dữ liệu, bảng và phân trang
        df = filtered_df
        create_treeview(df)
        update_table()
        update_pagination()

        messagebox.showinfo("Thông báo", "Lọc dữ liệu thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lọc dữ liệu không thành công: {e}")




def update_filter_columns():
    if df is not None:
        available_columns = df.columns.tolist()
        filter_column_menu["values"] = available_columns



# Giao diện chính
root = tk.Tk()
root.title("   World Education Dataset  ")
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
filter_condition_menu = ttk.Combobox(filter_frame, textvariable=filter_condition_var, font=("Pacifico", 12), state="readonly")
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

tk.Label(frame_left, text="   World Education Dataset   ", font=("Pacifico", 17, "bold"), bg="#CDCDB4", relief="raised").pack(pady=10)
tk.Button(frame_left, text="Chọn file CSV", command=select_file, font=("Pacifico", 15), bg="#669999").pack(pady=10)

pagination_frame = tk.Frame(frame_right, bg="white")
pagination_frame.pack(side="bottom", fill="x", pady=10)

# biến lưu trạng thái sắp xếp
sort_states={}

# hàm sắp xếp dữ liệu 
def sort_column(tree,col,reverse):
    global df
    # Nếu reverse True thì là False và ngược lại
    df=df.sort_values(by=col,ascending=not reverse)
    for row in tree.get_children():
        tree.delete(row)
    # duyệt qua từng dòng trong DataFrame chèn các giá trị của mỗi dòng vào trong TreeView,_ chỉ mục của dòng , dấu gạch dưới sử dụng để bỏ qua giá trị này 
    for _,row in df.iterrows(): # trả về Series rồi thêm thành list 
        tree.insert("","end",values=list(row)) # "" kí hiệu này đại diện cho root tức dòng mới sẽ được chèn vào vị trí gốc ,end được chèn vào cuối 
    sort_states[col]= not reverse


def delete_selected_row():
    selected_items = tree.selection()  # Lấy danh sách dòng được chọn
    if selected_items:  # Kiểm tra có dòng nào được chọn không
        if messagebox.askokcancel("Xác nhận","Bạn có chắc chắn muốn xóa các dòng đã chọn?"):
            try:
                for selected_item in selected_items:
                    row_index = tree.index(selected_item)  # lấy chỉ số dòng trong treeview
                    global df
                    df.drop(df.index[current_page * rows_per_page + row_index],inplace=True)  # Tính chỉ số trong DataFrame và xóa
                    tree.delete(selected_item) # xóa trong tree view
                
                # cập nhật dữ liệu lại sau khi xóa
                refresh_treeview()

                messagebox.showinfo("Thông báo", "Đã xóa dòng dữ liệu thành công!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa dòng dữ liệu: {str(e)}")
    else:
        messagebox.showwarning("Chú ý", "Vui lòng chọn ít nhất một dòng dữ liệu để xóa!")

def refresh_treeview():
    # làm sạch tree view
    for item in tree.get_children():
        tree.delete(item)

    # thêm lại
    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))

def edit_selected_row():
    selected_item = tree.selection()  # lấy dòng được chọn
    if selected_item:
        # Mở cửa sổ mới để nhập dữ liệu
        edit_window = Toplevel(root)
        edit_window.title("Chỉnh sửa dữ liệu")
        edit_window.geometry("900x700")

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
            
            # Thêm gợi ý cho cột 'country' (nếu có)
            if col == 'country':
                # Tạo ComboBox với các quốc gia hợp lệ
                country_var = tk.StringVar(value=current_values[col])
                country_menu = ttk.Combobox(edit_window, textvariable=country_var, values=VALID_COUNTRIES, font=("Pacifico", 12))
                country_menu.grid(row=i, column=1)
                entries[col] = country_menu

            # Thêm gợi ý cho cột 'year' (nếu có)
            elif col == 'year':
                year_value = current_values[col]
                if not (1900 <= year_value <= pd.to_datetime("today").year):
                    year_value = pd.to_datetime("today").year  # Cập nhật lại năm nếu không hợp lệ
                year_var = tk.StringVar(value=year_value)
                year_entry = tk.Entry(edit_window, textvariable=year_var)
                year_entry.grid(row=i, column=1)
                entries[col] = year_entry

        # Hàm để cập nhật dữ liệu
        def update_data():
            try:
                # Kiểm tra và ràng buộc kiểu dữ liệu cho mỗi cột
                for col, entry in entries.items():
                    value = entry.get()
                    
                    # Nếu cột là 'year', kiểm tra giá trị năm hợp lệ
                    if col == 'year':
                        if not value.isdigit():
                            raise ValueError("Cột 'year' chỉ chấp nhận số nguyên!")
                        year_value = int(value)
                        # Kiểm tra nếu năm nằm trong khoảng hợp lệ
                        current_year = pd.to_datetime("today").year  # Lấy năm hiện tại
                        if year_value < 1900 or year_value > current_year:
                            raise ValueError("Năm phải trong khoảng từ 1900 đến năm hiện tại!")

                        # Cập nhật giá trị năm vào DataFrame
                        df.at[current_page * rows_per_page + row_index, col] = year_value

                    elif col == 'country':
                        # Kiểm tra xem tên quốc gia có nằm trong danh sách hợp lệ không
                        value = entry.get()  # Nếu là ComboBox, lấy giá trị đã chọn
                        if value not in VALID_COUNTRIES:
                            raise ValueError(f"'{value}' không phải là tên quốc gia hợp lệ!")

                        # Cập nhật giá trị vào DataFrame nếu tên quốc gia hợp lệ
                        df.at[current_page * rows_per_page + row_index, col] = value

                    # Kiểm tra kiểu dữ liệu đối với các cột khác
                    elif df[col].dtype == 'int64':
                        # Nếu cột là int64, kiểm tra xem giá trị có phải là số nguyên không
                        if not value.isdigit():
                            raise ValueError(f"Giá trị ở cột {col} phải là số nguyên!")
                        df.at[current_page * rows_per_page + row_index, col] = int(value)

                    elif df[col].dtype == 'float64':
                        # Nếu cột là float64, kiểm tra xem giá trị có phải là số thực không
                        try:
                            df.at[current_page * rows_per_page + row_index, col] = float(value)
                        except ValueError:
                            raise ValueError(f"Giá trị ở cột {col} phải là số thực!")

                    elif df[col].dtype == 'object':
                        # Nếu cột là kiểu chuỗi (string), chấp nhận tất cả giá trị
                        df.at[current_page * rows_per_page + row_index, col] = str(value)

                    else:
                        # Nếu có kiểu dữ liệu khác, bạn có thể thêm xử lý tùy theo yêu cầu
                        df.at[current_page * rows_per_page + row_index, col] = value

                # Cập nhật Treeview
                tree.item(selected_item[0], values=[entry.get() for entry in entries.values()])
                messagebox.showinfo("Thông báo", "Dữ liệu đã được cập nhật thành công!")
                edit_window.destroy()

            except ValueError as e:
                messagebox.showerror("Lỗi", f"{str(e)}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật dữ liệu: {e}")

        # Nút cập nhật
        tk.Button(edit_window, text="Cập nhật", command=update_data).grid(row=len(df.columns), column=1)

    else:
        messagebox.showwarning("Chú ý", "Vui lòng chọn dòng dữ liệu để chỉnh sửa!")


def add_data():
    global df  # Khai báo df là biến toàn cục để có thể truy cập và thay đổi

    # Mở cửa sổ nhập dữ liệu mới
    add_window = Toplevel(root)
    add_window.title("Thêm dữ liệu mới")
    add_window.geometry("700x700")
    
    # Tạo nhãn và trường nhập cho mỗi cột
    entries = {}
    for i, col in enumerate(df.columns):
        tk.Label(add_window, text=col).grid(row=i, column=0)
        entry = tk.Entry(add_window)
        entry.grid(row=i, column=1)
        entries[col] = entry
    
    # Hàm để thêm dữ liệu mới vào DataFrame
    def submit_data():
        try:
            global df  # Đảm bảo df là biến toàn cục

            # Tạo từ điển để lưu trữ dữ liệu của dòng mới
            new_row = {}
            
            for col, entry in entries.items():
                value = entry.get()
                
                # Kiểm tra trường hợp trống
                if not value:
                    raise ValueError(f"Cột '{col}' không thể để trống!")

                # Kiểm tra kiểu dữ liệu cho từng cột
                if col == 'year':  # Kiểm tra năm hợp lệ
                    if not value.isdigit():
                        raise ValueError("Cột 'year' chỉ chấp nhận số nguyên!")
                    year_value = int(value)
                    current_year = pd.to_datetime("today").year
                    if year_value < 1900 or year_value > current_year:
                        raise ValueError("Năm phải trong khoảng từ 1900 đến năm hiện tại!")
                    new_row[col] = year_value

                elif col == 'country':  # Kiểm tra quốc gia hợp lệ
                    if value not in VALID_COUNTRIES:
                        raise ValueError(f"'{value}' không phải là tên quốc gia hợp lệ!")
                    new_row[col] = value

                elif df[col].dtype == 'int64':  # Kiểm tra kiểu int
                    if not value.isdigit():
                        raise ValueError(f"Giá trị ở cột {col} phải là số nguyên!")
                    new_row[col] = int(value)

                elif df[col].dtype == 'float64':  # Kiểm tra kiểu float
                    try:
                        new_row[col] = float(value)
                    except ValueError:
                        raise ValueError(f"Giá trị ở cột {col} phải là số thực!")

                elif df[col].dtype == 'object':  # Kiểu chuỗi
                    new_row[col] = str(value)

            # Kiểm tra xem các cột trong dòng mới có khớp với cột của df không
            for col in df.columns:
                if col not in new_row:
                    new_row[col] = None  # Đảm bảo có giá trị cho cột thiếu (nếu có)

            # Thêm dòng mới vào DataFrame
            new_index = len(df)
            df.loc[new_index] = new_row
            create_treeview(df)
            update_table()
            update_pagination()
            messagebox.showinfo("Thông báo", "Dữ liệu đã được thêm thành công!")
            add_window.destroy()

        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thêm dữ liệu: {e}")


    # Nút gửi dữ liệu
    tk.Button(add_window, text="Thêm dữ liệu", command=submit_data).grid(row=len(df.columns), column=1)


# danh sách option
options = [
    ("Chi tiêu chính phủ cho Giáo Dục theo các năm", lambda: gov_exp_pct_gdp(df)),                 # Done
    ("Mối quan hệ giữa chi tiêu Chính Phủ cho giáo dục và \n Tỷ lệ người lớn biết chữ", lambda: Top_lit_rate_adult_pct(df)),              # Done
    ("Phân bổ nhóm các quốc gia theo chi tiêu Chính Phủ \n cho Giáo dục", lambda: Top_gov_exp_by_country(df)), # Done
    ("So sánh tỷ lệ học sinh trên giáo viên cấp \n tiểu học và trung học ở Việt Nam", lambda: Rela_GovExp_LitRate(df)), # Done
    ("Top 10 Quốc Gia Tỷ Lệ Người Biết Chữ Cao Nhất", lambda: Pie_gov_exp(df)), # Done
    ("Top 10 Quốc Gia Tỷ Lệ Chi Tiêu Giáo Dục Cao Nhất", lambda: Top_max_Pupil_Teacher_pri(df)),      
    ("Top 20 Quốc gia có tỷ lệ Pupil/Teacher (Primary) \n cao nhất", lambda: Top_min_Pupil_Teacher_pri(df)), # Done
    ("Top 20 Quốc gia có tỷ lệ Pupil/Teacher (Primary) \n thấp nhất", lambda: Pupil_Teacher_pri_sec(df)), # Done
]
combobox_options=[text for text,_ in options] # danh sách options
selected_option=tk.StringVar()

# combobox hiển thị danh sách chức năng
combobox=ttk.Combobox(frame_left,textvariable=selected_option,values=combobox_options,font=("Pacifico", 12),state="readonly",width=45)

combobox.pack(pady=10)
combobox.set("Chọn biểu đồ bạn muốn xem") 

def execute_choice():
    for text, command in options:
        if text == selected_option.get():  # so sánh với lựa chọn người dùng
            command()  # thực thi hàm tương tự
            break
tk.Button(
    frame_left, 
    text="Xác nhận", 
    command=execute_choice, 
    font=("Pacifico", 13), 
    bg="#6666CC", 
    borderwidth=2, 
    relief="raised"
).pack(pady=10)


tk.Button(frame_left, text="Xóa dòng dữ liệu", command=delete_selected_row, font=("Pacifico", 15), bg="#CC6666", borderwidth=2, relief="raised").pack(pady=10)
tk.Button(frame_left, text="Chỉnh sửa dữ liệu", command=edit_selected_row, font=("Pacifico", 15), bg="#CC9966", borderwidth=2, relief="raised").pack(pady=10)
tk.Button(frame_left, text="Thêm dữ liệu", command=add_data, font=("Pacifico", 15), bg="#66CC66", borderwidth=2, relief="raised").pack(pady=10)


def update_describe_columns():
    if df is not None:
        return df.columns.tolist()
    else:
        return ["Chưa có dữ liệu"]

describe_option = tk.StringVar()
describe_combobox = ttk.Combobox(frame_left, textvariable=describe_option, values=update_describe_columns(), font=("Pacifico", 12), state="readonly", width=45)
describe_combobox.pack(pady=10)

def refresh_describe_combobox():
    describe_combobox["values"] = update_describe_columns()
    describe_combobox.set("Chọn một cột để phân tích")

def describe_single():
    column = describe_option.get()
    if df is None:
        messagebox.showwarning("Cảnh báo", "Chưa có dữ liệu. Vui lòng tải file CSV trước.")
        return
    if column == "":  
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn một cột để thống kê!")
        return

    if df is not None and column in df.columns:
        if df[column].dtype == "object":
            messagebox.showwarning("Cảnh báo", "Cột này có kiểu dữ liệu không thể thống kê mô tả (object type).")
            return
        
        new_dataframe = df[[column]].describe()
        new_dataframe.index = ["count", "mean", "standard deviation", "minimum", "25% quartile",
                               "median", "75% quartile", "max"]
        
        root = tk.Tk()
        root.title(f"Thống kê mô tả cho cột {column}")

        frame1 = tk.Frame(root)
        frame1.pack(side="top")
        frame2 = tk.Frame(root)
        frame2.pack(side="bottom")

        tk.Label(frame1, text="1: count, 2: mean, 3: standard deviation, 4: minimum, 5: 25% quartile, "
                              "6: median, 7: 75% quartile, 8: max").pack()

        table = Table(frame2, dataframe=new_dataframe, width=300, height=200)
        table.show()

        root.mainloop()
    else:
        messagebox.showwarning("Cảnh báo", "Chưa chọn cột hợp lệ hoặc dữ liệu không có sẵn")

def describe_all():
    if df is not None:
        new_dataframe = df.describe()
        new_dataframe.index = ["count", "mean", "standard deviation", "minimum", "25% quartile",
                               "median", "75% quartile", "max"]
        
        root = tk.Tk()
        root.title(f"Thống kê mô tả cho tất cả các cột")

        frame1 = tk.Frame(root)
        frame1.pack(side="top")
        frame2 = tk.Frame(root)
        frame2.pack(side="bottom")

        tk.Label(frame1, text="1: count, 2: mean, 3: standard deviation, 4: minimum, 5: 25% quartile, "
                              "6: median, 7: 75% quartile, 8: max").pack()

        table = Table(frame2, dataframe=new_dataframe, width=750, height=200)
        table.show()

        root.mainloop()
    else:
        messagebox.showwarning("Cảnh báo", "Chưa có dữ liệu. Vui lòng tải file CSV trước.")

def display_histogram():
    column = describe_option.get()
    if df is None:
        messagebox.showwarning("Cảnh báo", "Chưa có dữ liệu. Vui lòng tải file CSV trước.")
        return
    if column == "":  
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn một cột để vẽ biểu đồ!")
        return

    if df is not None and column in df.columns:
        if df[column].dtype == "object":
            messagebox.showwarning("Cảnh báo", "Cột này có kiểu dữ liệu không thể vẽ biểu đồ (object type).")
            return
        
        plt.hist(df[column], bins=math.floor(df.shape[0] ** 0.5))
        plt.title(f"Biểu đồ tần suất cho cột {column}")
        plt.xlabel(column)
        plt.ylabel("Tần suất")
        plt.gcf().text(0.1, 0.01, f"mean={round(df[column].mean(), 3)}, std ={round(df[column].std(), 2)}")
        plt.show()
    else:
        messagebox.showwarning("Cảnh báo", "Chưa chọn cột hợp lệ hoặc dữ liệu không có sẵn")


tk.Button(
    frame_left, 
    text="Thống kê một biến", 
    command=describe_single, 
    font=("Pacifico", 13), 
    bg="#66CC66", 
    borderwidth=2, 
    relief="raised"
).pack(pady=5)

tk.Button(
    frame_left, 
    text="Thống kê tất cả các biến", 
    command=describe_all, 
    font=("Pacifico", 13), 
    bg="#6699CC", 
    borderwidth=2, 
    relief="raised"
).pack(pady=5)

tk.Button(
    frame_left, 
    text="Vẽ Biểu đồ Tần suất",  
    command=display_histogram, 
    font=("Pacifico", 13), 
    bg="#FFCC66", 
    borderwidth=2, 
    relief="raised"
).pack(pady=5)


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
