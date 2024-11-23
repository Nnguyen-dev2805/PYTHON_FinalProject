import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, Toplevel
import seaborn as sns
import matplotlib.pyplot as plt

# chứa các hàm về phân tích lợi nhuận

def calculate_profit(root, df): 
    """Tính lợi nhuận của bộ phim"""
    if df is None:
        messagebox.showerror("Lỗi", "Vui lòng chọn file CSV trước!")
        return
    
    result = df.loc[:10, ["original_title", "profit"]]
    show_result(root, result.to_string(index=False))

def show_result(root, message):
    result_window = Toplevel(root)
    result_window.title("Kết quả")
    result_window.geometry("1000x1000")
    tk.Label(result_window, bg='white', text=message, font=("Pacifico", 14), wraplength=700, anchor="nw", justify="left").place(x=150, y=150)


def industry_highest_revenue(df):
    """Vẽ biểu đồ tổng lợi nhuận theo năm phát hành."""
    if df is None:
        messagebox.showerror("Lỗi", "Vui lòng chọn file CSV trước")
        return 
    
    profit_peryear = df.groupby("release_year")["profit"].sum()
    profit_peryear.plot(kind='bar', figsize=(30, 17), color='skyblue')
    plt.xlabel("Năm phát hành")
    plt.ylabel("Tổng lợi nhuận")
    plt.title("Tổng lợi nhuận từ các bộ phim theo năm")
    plt.show()

def highest_profit_month(df):
    """Vẽ biểu đồ tổng lợi nhuận theo tháng"""
    if df is None:
        messagebox.showerror("Lỗi", "Vui lòng chọn file CSV trước")
        return 
    
    releasedate_index = df.set_index("release_date")
    profit_permonth = releasedate_index.groupby(releasedate_index.index.month)["profit"].sum()
    sns.barplot(x=profit_permonth.index, y=profit_permonth.values)
    plt.title("Lợi nhuận thu được từ phim theo tháng")
    plt.xlabel("Tháng")
    plt.ylabel("Tổng lợi nhuận")
    plt.show()
