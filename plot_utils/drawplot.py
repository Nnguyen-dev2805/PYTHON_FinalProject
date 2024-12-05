import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, Toplevel
import seaborn as sns
import matplotlib.pyplot as plt

def gov_exp_pct_gdp(df): 
    """Chi tiêu chính phủ cho Giáo Dục (%GDP) theo thời gian"""
    if df is None:
        from tkinter import messagebox
        messagebox.showerror("Lỗi", "Vui lòng chọn file CSV trước!")
        return
    
    plt.figure(figsize=(15,15))
    avg_gov_exp=df.groupby('year')['gov_exp_pct_gdp'].mean()
    sns.lineplot(data=avg_gov_exp)
    plt.yticks(fontsize=15)
    plt.xticks(fontsize=15)
    plt.title("Chi tiêu chính phủ cho Giáo Dục (%GDP) theo thời gian", fontsize=20)
    plt.xlabel("Năm", fontsize=20)
    plt.ylabel("Chi tiêu trung bình (%GDP)", fontsize=20)
    plt.grid(True)
    plt.show()

def Top_lit_rate_adult_pct(df):
    """Top 10 Quốc Gia Có Tỷ Lệ Trung Bình Người Biết Chữ Cao Nhất"""
    if df is None:
        from tkinter import messagebox
        messagebox.showerror("Lỗi", "Vui lòng chọn file CSV trước!")
        return
    
    plt.figure(figsize=(15,15))
    lil_rate_by_country=df.groupby('country')['lit_rate_adult_pct'].mean().sort_values().head(10)
    lil_rate_by_country.plot(kind="barh",color='skyblue')
    plt.yticks(fontsize=15)
    plt.xticks(fontsize=15)
    plt.title('Top 10 Quốc Gia Có Tỷ Lệ Trung Bình Người Biết Chữ Cao Nhất', fontsize=20)
    plt.xlabel('Tỷ Lệ Biết Chữ (%)', fontsize=20)
    plt.ylabel('Quốc Gia', fontsize=20)
    plt.show()

def Top_gov_exp_by_country(df):
    """Top 10 Quốc Gia Có Tỷ Lệ Chi Tiêu Giáo Dục (%GDP)  Cao Nhất"""
    if df is None:
        from tkinter import messagebox
        messagebox.showerror("Lỗi", "Vui lòng chọn file CSV trước!")
        return
    
    gov_exp_by_country=df.groupby('country')['gov_exp_pct_gdp'].mean().sort_values().head(10)
    gov_exp_by_country.plot(kind='barh',figsize=(15,15),color='lightgreen')
    plt.yticks(fontsize=15)
    plt.xticks(fontsize=15)
    plt.title('Top 10 Quốc Gia Có Tỷ Lệ Chi Tiêu Giáo Dục (%GDP)  Cao Nhất', fontsize=20)
    plt.xlabel('Chi Tiêu (% GDP)', fontsize=20)
    plt.ylabel('Quốc Gia', fontsize=20)
    plt.show()


def Rela_GovExp_LitRate(df):
    """Mối Quan Hệ Giữa Chi Tiêu Chính Phủ cho Giáo Dục (% GDP) Và Tỷ Lệ Người Lớn (15 tuổi trở lên) Biết Chữ (%)"""
    if df is None:
        from tkinter import messagebox
        messagebox.showerror("Lỗi", "Vui lòng chọn file CSV trước!")
        return
    
    correlation = df['gov_exp_pct_gdp'].corr(df['lit_rate_adult_pct'])
    plt.figure(figsize=(15,15))
    plt.yticks(fontsize=15)
    plt.xticks(fontsize=15)
    sns.scatterplot(data=df,x='gov_exp_pct_gdp',y='lit_rate_adult_pct',color='blue',alpha=0.7)
    # ve duong hoi qui tuyen tinh, nhung khong ve phan tan
    sns.regplot(data=df,x='gov_exp_pct_gdp',y='lit_rate_adult_pct',scatter=False,color='red',label='Đường xu hướng')
    plt.title(f'Mối Quan Hệ Giữa Chi Tiêu Chính Phủ cho Giáo Dục (% GDP) \nVà Tỷ Lệ Người Lớn (15 tuổi trở lên) Biết Chữ (%)\nHệ Số Tương Quan: {correlation:.2f}', fontsize=20)
    plt.xlabel('Chi Tiêu Chính Phủ cho Giáo Dục (% GDP)', fontsize=20)
    plt.ylabel('Tỷ Lệ Người Lớn Biết Chữ (%)', fontsize=20)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.show()


def Pie_gov_exp(df):
    """Phân bố các quốc gia theo Chi tiêu Chính phủ cho Giáo dục (% GDP)"""
    if df is None:
        from tkinter import messagebox
        messagebox.showerror("Lỗi", "Vui lòng chọn file CSV trước!")
        return
    
    gov_exp_by_country = df.groupby('country')['gov_exp_pct_gdp'].mean()

    # Phân loại quốc gia thành các nhóm dựa trên tỉ lệ chi tiêu giáo dục
    bins = [0, 3, 6, float('inf')]
    labels = ['Thấp', 'Trung Bình', 'Cao']
    gov_exp_group = pd.cut(gov_exp_by_country, bins=bins, labels=labels)

    # Đếm số lượng từng nhóm
    gov_exp_group_count = gov_exp_group.value_counts()

    plt.figure(figsize=(15, 15))

    # Chỉnh kích thước phông chữ cho nhãn trục
    plt.yticks(fontsize=15)
    plt.xticks(fontsize=15)

    # Chỉnh màu sắc
    colors = ['lightgreen', 'lightblue', 'lightcoral']

    # Vẽ biểu đồ tròn (pie chart)
    ax = gov_exp_group_count.plot(kind='pie', autopct='%1.1f%%', startangle=90, 
                                  colors=colors, wedgeprops={'edgecolor': 'black'})

    # Tiêu đề của biểu đồ
    plt.title('Phân bố các quốc gia theo Chi tiêu Chính phủ cho Giáo dục (% GDP)', fontsize=20)

    # Chỉnh cỡ chữ của legend và khoảng cách giữa các label
    handles = [plt.Line2D([0], [0], color=color, lw=4) for color in ['lightblue', 'lightgreen', 'lightcoral']]
    plt.legend(handles=handles, labels=labels, loc='upper left', title='Mức độ chi tiêu', 
               fontsize=18, labelspacing=1.5)  # labelspacing thêm để khoảng cách giữa các nhãn rộng hơn

    # Chỉnh cỡ chữ của các nhãn trong biểu đồ tròn (từng phần)
    for text in ax.texts:
        text.set_fontsize(18)

    plt.show()


def Top_max_Pupil_Teacher_pri(df):
    """Top 20 Quốc gia có tỷ lệ Pupil/Teacher (Primary) cao nhất"""
    if df is None:
        from tkinter import messagebox
        messagebox.showerror("Lỗi", "Vui lòng chọn file CSV trước!")
        return
    
    # Đầu tiên, nhóm dữ liệu theo quốc gia và tính giá trị trung bình cho mỗi quốc gia
    df_grouped = df.groupby('country')['pupil_teacher_primary'].mean().reset_index()

    # Sắp xếp theo tỷ lệ Pupil_teacher_primary từ cao đến thấp và lấy top 20 quốc gia
    df_top20 = df_grouped.sort_values('pupil_teacher_primary', ascending=False).head(20)

    # Vẽ biểu đồ cột
    plt.figure(figsize=(15, 15))
    plt.yticks(fontsize=15)
    plt.xticks(fontsize=15)
    plt.barh(df_top20['country'], df_top20['pupil_teacher_primary'], color='skyblue')
    plt.xlabel('Tỷ lệ học sinh trên giáo viên (Primary)', fontsize=20)
    plt.ylabel('Quốc gia', fontsize=20)
    plt.title('Top 20 Quốc gia có tỷ lệ Pupil/Teacher (Primary) cao nhất', fontsize=20)
    plt.gca().invert_yaxis()  # Đảo ngược trục Y để quốc gia có tỷ lệ cao nhất nằm trên cùng
    plt.show()


def Top_min_Pupil_Teacher_pri(df):
    """Top 20 Quốc gia có tỷ lệ học sinh / giáo viên cấp tiểu học thấp nhất"""
    if df is None:
        from tkinter import messagebox
        messagebox.showerror("Lỗi", "Vui lòng chọn file CSV trước!")
        return
    
    # Đầu tiên, nhóm dữ liệu theo quốc gia và tính giá trị trung bình cho mỗi quốc gia
    df_grouped = df.groupby('country')['pupil_teacher_primary'].mean().reset_index()

    # Sắp xếp theo tỷ lệ Pupil_teacher_primary từ cao đến thấp và lấy top 20 quốc gia
    df_top20 = df_grouped.sort_values('pupil_teacher_primary', ascending=True).head(20)

    # Vẽ biểu đồ cột
    plt.figure(figsize=(15, 15))
    plt.yticks(fontsize=15)
    plt.xticks(fontsize=15)
    plt.barh(df_top20['country'], df_top20['pupil_teacher_primary'], color='skyblue')
    plt.xlabel('Tỷ lệ học sinh trên giáo viên (Primary)', fontsize=20)
    plt.ylabel('Quốc gia', fontsize=20)
    plt.title('Top 20 Quốc gia có tỷ lệ học sinh / giáo viên cấp tiểu học thấp nhất', fontsize=20)
    plt.gca().invert_yaxis()  # Đảo ngược trục Y để quốc gia có tỷ lệ cao nhất nằm trên cùng
    plt.show()

def Pupil_Teacher_pri_sec(df):
    """So sánh tỷ lệ học sinh / giáo viên cấp tiểu học và trung học ở Việt Nam"""
    if df is None:
        from tkinter import messagebox
        messagebox.showerror("Lỗi", "Vui lòng chọn file CSV trước!")
        return
    
    df_vietnam = df[df['country'] == 'Viet Nam'][['year', 'pupil_teacher_primary', 'pupil_teacher_secondary']]

    # Vẽ biểu đồ đường
    plt.figure(figsize=(15, 15))
    plt.yticks(fontsize=15)
    plt.xticks(fontsize=15)
    # Vẽ đường cho tỷ lệ giáo viên tiểu học
    plt.plot(df_vietnam['year'], df_vietnam['pupil_teacher_primary'], label='Tỷ lệ giáo viên tiểu học', marker='o', color='lightcoral')

    # Vẽ đường cho tỷ lệ giáo viên trung học
    plt.plot(df_vietnam['year'], df_vietnam['pupil_teacher_secondary'], label='Tỷ lệ giáo viên trung học', marker='o', color='skyblue')

    # Thêm nhãn, tiêu đề và chú thích
    plt.xlabel('Năm', fontsize=20)
    plt.ylabel('Tỷ lệ học sinh trên giáo viên', fontsize=20)
    plt.title('So sánh tỷ lệ học sinh / giáo viên cấp tiểu học và trung học ở Việt Nam', fontsize=20)
    plt.legend()

    # Hiển thị biểu đồ
    plt.grid(True)
    plt.show()
