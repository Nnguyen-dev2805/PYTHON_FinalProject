import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, Toplevel
import seaborn as sns
import matplotlib.pyplot as plt


def show_genre_data(df, metric, title):
    """Vẽ biểu đồ phân tích dữ liệu thể loại."""
    df_split = df.assign(genres=df['genres'].str.split('|')).explode('genres')
    genre_data = df_split.groupby('genres')[metric].mean().sort_values(ascending=False)
    genre_data.plot(kind='barh', figsize=(10, 8), color='skyblue')
    plt.title(title)
    plt.xlabel(metric)
    plt.ylabel("Thể loại")
    plt.show()
