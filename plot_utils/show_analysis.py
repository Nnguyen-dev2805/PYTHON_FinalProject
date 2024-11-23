import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, Toplevel
import seaborn as sns
import matplotlib.pyplot as plt

def show_top(df, column, metric, title): 
    """Top 10 bộ phim theo (revenue_adj) hoặc (budget_adj) hoặc (popularity)"""
    if df is None:
        messagebox.showerror("Lỗi", "Vui lòng chọn file CSV trước!")
        return
    draw_analysis(df, column, metric, title)

def draw_analysis(df, column, metric, title):
    top = df[[column, metric]].sort_values(by=metric, ascending=False).head(10)
    sns.barplot(x=top[metric], y=top[column])
    plt.title(title, size=30)
    plt.xlabel(metric, size=20)
    plt.ylabel(column, size=20)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.show()


def show_genre_data(df, metric, title):
    if df is None:
        messagebox.showerror("Lỗi", "Vui lòng chọn file CSV trước!")
        return
    
    draw_data(df, metric, title)


def draw_data(df, metric, title):
    df_split = df.assign(genres=df['genres'].str.split('|')).explode('genres')
    genre_data = df_split.groupby('genres')[metric].mean().sort_values(ascending=False)
    genre_data.plot(kind='barh', figsize=(30, 17), color='skyblue')
    plt.title(title, size=30)
    plt.xlabel(metric, size=20)
    plt.ylabel('Thể loại', size=20)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.tight_layout()
    plt.show()



def show_genres_data(df):
    if df is None:
        messagebox.showerror("Lỗi", "Vui lòng chọn file CSV trước!")
        return

    all_genres = df['genres'].str.split('|').explode()
    genre_counts = all_genres.value_counts(ascending=False)
    genre_counts.plot(kind='barh', figsize=(30, 17), color='m', rot=45)
    plt.title('Phim theo thể loại, 1960-2015', size=30)
    plt.xlabel('Thể loại', size=20)
    plt.ylabel('Số lần xuất hiện', size=20)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.tight_layout()
    plt.show()




