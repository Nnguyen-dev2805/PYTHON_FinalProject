import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, Toplevel
import seaborn as sns
import matplotlib.pyplot as plt

# các hàm về thời gian

def favorite_runtime(df):
    """Vẽ biểu đồ thời lượng phim được yêu thích nhất"""
    if df is None:
        messagebox.showerror("Lỗi", "Vui lòng chọn file CSV trước!")
        return
    
    # Nhóm dữ liệu theo thời lượng và tính trung bình độ phổ biến
    run_pop = df.groupby('runtime')['popularity'].mean()
    
    # Vẽ biểu đồ
    run_pop.plot(figsize=(30, 17))
    plt.title("Thời lượng phim được khán giả yêu thích nhất", size=30)
    plt.xlabel('Thời lượng', size=20)
    plt.ylabel('Độ phổ biến', size=20)

    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    
    plt.show()

