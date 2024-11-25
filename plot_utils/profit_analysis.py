import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, Toplevel
import seaborn as sns
import matplotlib.pyplot as plt

# chứa các hàm về phân tích lợi nhuận

def calculate_profit(root, df): 
    """Tính lợi nhuận của bộ phim và hiển thị biểu đồ"""
    if df is None:
        from tkinter import messagebox
        messagebox.showerror("Lỗi", "Vui lòng chọn file CSV trước!")
        return
    
    # Lấy dữ liệu top 10
    result = df.loc[:10, ["original_title", "profit"]]
    
    # Vẽ biểu đồ
    plt.figure(figsize=(10, 6))
    plt.bar(result["original_title"], result["profit"], color="skyblue")
    plt.title("Top 10 Bộ Phim và Lợi Nhuận", fontsize=30)
    plt.xlabel("Tên phim", fontsize=20)
    plt.ylabel("Lợi nhuận (USD)", fontsize=15)
    plt.xticks(rotation=45, ha='right', fontsize=15)
    plt.tight_layout()
    plt.show()

def industry_highest_revenue(df):
    """Vẽ biểu đồ tổng lợi nhuận theo năm phát hành."""
    if df is None:
        messagebox.showerror("Lỗi", "Vui lòng chọn file CSV trước")
        return 
    
    profit_peryear = df.groupby("release_year")["profit"].sum()
    profit_peryear.plot(kind='bar', figsize=(30, 17), color='skyblue')
    plt.title("Tổng lợi nhuận từ các bộ phim theo năm", size=30)
    
    plt.xlabel("Năm phát hành", size=20)
    plt.ylabel("Tổng lợi nhuận", size=20)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    
    plt.tight_layout()
    plt.show()

def highest_profit_month(df):
    """Vẽ biểu đồ tổng lợi nhuận theo tháng"""
    if df is None:
        messagebox.showerror("Lỗi", "Vui lòng chọn file CSV trước")
        return 
    
    releasedate_index = df.set_index("release_date")
    profit_permonth = releasedate_index.groupby(releasedate_index.index.month)["profit"].sum()
    sns.barplot(x=profit_permonth.index, y=profit_permonth.values)
    
    plt.title("Lợi nhuận thu được từ phim theo tháng", size=30)
    plt.xlabel("Tháng", size=20)
    plt.ylabel("Tổng lợi nhuận", size=20)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)

    plt.tight_layout()
    plt.show()

