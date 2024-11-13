import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

path = "clean_data.csv"
df = pd.read_csv(path)

# Hàm lấy Min Max
def getMinMax(x):
    highest = df[x].idxmax()
    highest_details = pd.DataFrame(df.loc[highest])
    lowest = df[x].idxmin()
    lowest_details = pd.DataFrame(df.loc[lowest])
    print("Bộ phim có giá trị cao nhất " + x + " : ", df["original_title"][highest])
    print("Bộ phim có giá trị thấp nhất " + x + " : ", df["original_title"][lowest])
    return pd.concat([highest_details, lowest_details], axis=1)
# Count frequency and inascending sort
def extract_data(x):
    all_data = df[x].str.cat(sep = '|')
    all_data = pd.Series(all_data.split('|'))
    return all_data.value_counts(ascending = False)

# Add col profit
df["profit"] = df["revenue_adj"] - df["budget_adj"]
df["release_date"] = pd.to_datetime(df["release_date"], format="mixed")
Top_doanhthu = df[["original_title", "revenue_adj"]]
Top_ngansach = df[["original_title", "budget_adj"]]
Top_noitieng = df[["original_title", "popularity"]]
df_split = df.assign(genres = df['genres'].str.split('|')).explode('genres')

while True:
    print("------------Menu-------------")
    print("0.Exit")
    print("1.Tính toán lợi nhuận của bộ phim")
    print("2.Ngành công nghiệp điện ảnh đạt doanh thu cao nhất vào năm nào ?")
    print("3.Tháng nào ngành công nghiệp điện ảnh có lợi nhuận cao nhất ?")
    print("4.Thời lượng của bộ phim được khán giả yêu thích nhất là bao nhiêu?")
    print("5.Top 10 bộ phim hàng đầu dựa vào doanh thu")
    print("6.Top 10 bộ phim có ngân sách cao nhất")
    print("7.Top 10 bộ phim nổi tiếng nhất")
    print("8.Số lượng phim sản xuất theo thể loại")
    print("9.Những thể loại nào có lợi thế hơn về tổng thể")
    print("10.Những thể loại nào phổ biến hơn tổng thể")
    print("11.Top 10 diễn viên xuất hiện nhiều nhất")
    print("12.Top 10 đạo diễn có số lượng phim nhiều nhất")
    print("13.Top 10 công ty sản xuất số lượng phim nhiều nhất")

    choice=int(input("Nhập sự lựa chọn của bạn: "))
    if choice == 1 :
        print(df.loc[:1, ["original_title", "profit"]])
        print(getMinMax('profit'))
    elif choice == 2:
        profit_peryear = df.groupby("release_year")["profit"].sum()
        ax = profit_peryear.plot(stacked=True, figsize=(10, 8))
        ax.set(
            xlabel="Năm phát hành",
            ylabel="Tổng lợi nhuận",
            title="Tổng lợi nhuận thu được từ tất cả bộ phim mỗi năm",
        )
        plt.show()
        max_profit = profit_peryear.idxmax()
        print("Ngành công nghiệp điện ảnh đạt lợi nhuận cao nhất trong ", max_profit, ".")
    elif choice == 3:
        releasedate_index = df.set_index("release_date")
        groupby_index = releasedate_index.groupby([releasedate_index.index.month])
        profit_permonth = groupby_index["profit"].sum()
        profit_permonth = pd.DataFrame(profit_permonth)

        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 8))

        profit_permonth_bar = sns.barplot(
            x=profit_permonth.index, y=profit_permonth["profit"], data=profit_permonth
        )
        profit_permonth_bar.axes.set_title(
            "Lợi nhuận thu được từ phim theo tháng", color="red", fontsize=18
        )

        profit_permonth_bar.set_xlabel("Tháng phát hành")
        profit_permonth_bar.set_ylabel("Tổng lợi nhuận")

        month_list = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
        profit_permonth_bar.set_xticks(range(len(month_list)))
        profit_permonth_bar.set_xticklabels(month_list, rotation=90, size=14);
        plt.show()
    elif choice == 4:
        run_pop = df.groupby('runtime')['popularity'].mean()
        run_pop.plot(figsize = (10, 8))
        plt.title("Thời lượng phim được khán giả yêu thích nhất", fontsize=14)
        plt.xlabel('Thời lượng', fontsize=13)
        plt.ylabel('Độ phổ biến', fontsize=13)
        max_run = run_pop.idxmax()
        print('Thời lượng phim được khán giả yêu thích nhất:', max_run, 'phút.')
        plt.show()
    elif choice == 5:
        sns.set(rc={"figure.figsize": (12, 8)}, style="whitegrid")
        ax = sns.barplot(
            x=Top_doanhthu.sort_values(by="revenue_adj", ascending=False)
            .head(10)
            .original_title,
            y=Top_doanhthu.sort_values(by="revenue_adj", ascending=False).head(10).revenue_adj,
        )
        plt.xticks(rotation=90)
        ax.set(
            xlabel="Tên phim",
            ylabel="Doanh thu",
            title="Top 10 bộ phim có daonh thu nhiều nhất",
        )
        plt.show()
    elif choice == 6:
        sns.set(rc={"figure.figsize": (12, 8)}, style="whitegrid")
        ax = sns.barplot(
            x=Top_ngansach.sort_values(by="budget_adj", ascending=False)
            .head(10)
            .original_title,
            y=Top_ngansach.sort_values(by="budget_adj", ascending=False).head(10).budget_adj,
        )
        plt.xticks(rotation=90)
        ax.set(
            xlabel="Tên phim", ylabel="Ngân sách", title="Top 10 bộ phim có ngân sách lớn nhất"
        )
        plt.show()
    elif choice == 7:
        sns.set(rc={"figure.figsize": (12, 8)}, style="whitegrid")
        ax = sns.barplot(
            x=Top_noitieng.sort_values(by="popularity", ascending=False)
            .head(10)
            .original_title,
            y=Top_noitieng.sort_values(by="popularity", ascending=False).head(10).popularity,
        )
        plt.xticks(rotation=90)
        ax.set(xlabel="Tên phim", title="Top 10 bộ phim nổi tiếng nhất")
        plt.show()               
    elif choice == 8:
        df_split['genres'].value_counts(ascending = False).plot(kind='bar',figsize = (10,8),color='m');
        plt.title('Phim theo thể loại, 1960-2015', size = 18)
        plt.xlabel('Thể loại', size = 15)
        plt.ylabel('Số lần xuất hiện', size = 15)   
        plt.show()  
    elif choice == 9:
        profit_and_genres_df = df_split[['original_title', 'profit', 'genres']]
        mean_profit_vs_genre_df = (
            profit_and_genres_df.groupby('genres', as_index=False)['profit'].mean()
        )
        mean_profit_vs_genre_df = mean_profit_vs_genre_df.sort_values('profit', ascending=False)
        mean_profit_vs_genre_df.head()
        mean_profit_vs_genre_df.plot(
            x='genres',  # Dùng 'genres' làm nhãn trục
            y='profit',  # Lợi nhuận tương ứng với thể loại
            kind='barh', 
            figsize=(10, 8), 
            color='g'
        )

        plt.title('Phân loại thể loại phim theo lợi nhuận', size=18)
        plt.xlabel('Lợi nhuận thu được', size=12)
        plt.ylabel('Thể loại phim', size=12)
        plt.show()
    elif choice == 10:
        mean_popular_vs_genre_df = df_split[['original_title', 'popularity', 'genres']]
        mean_popular_vs_genre_df = (
            mean_popular_vs_genre_df.groupby('genres', as_index=False)['popularity'].mean()
        )
        mean_popular_vs_genre_df = mean_popular_vs_genre_df.sort_values('popularity', ascending=False)
        mean_popular_vs_genre_df.head()
        mean_popular_vs_genre_df.plot(
            y='popularity',  
            kind='barh', 
            figsize=(8, 8), 
            color='g'
        )

        plt.title('Phân loại thể loại phim theo mức độ phổ biến', size=18) 
        plt.xlabel('Mức độ phổ biến', size=12)  
        plt.ylabel('Thể loại', size=12) 
        plt.show()
    elif choice == 11:
        top10_act = extract_data('cast').iloc[:10]
        top10_act.plot.bar(figsize=(10, 8), colormap='RdBu', fontsize=12)
        plt.title("Top 10 diễn viên xuất hiện nhiều nhất trong phim", fontsize=14)
        plt.xlabel('Diễn viên', fontsize=13)
        plt.ylabel('Số lần xuất hiện', fontsize=13)
        print('Top 10 diễn viên xuất hiện nhiều nhất trong phim:')
        print(top10_act)
        plt.show()
    elif choice == 12:
        top10_direct = extract_data('director').iloc[:10]
        top10_direct.plot.bar(figsize=(10, 8), colormap='viridis', fontsize=12)
        plt.title("10 đạo diễn có số lượng phim nhiều nhất", fontsize=14)
        plt.xlabel('Directors', fontsize=13)
        plt.ylabel('Number of movies', fontsize=13)
        print('Những đạo diễn hàng đầu với số lượng phim nhiều nhất:')
        print(top10_direct)
        plt.show()
    elif choice == 13:
        top10_prod = extract_data('production_companies').iloc[:10]
        top10_prod.plot.bar(figsize=(10, 8), colormap='tab20c', fontsize=12)
        plt.title("10 công ty sản xuất hàng đầu có số lượng phim nhiều nhất", fontsize=14)
        plt.xlabel('Các công ty sản xuất', fontsize=13)
        plt.ylabel('Số lượng phim', fontsize=13)
        print('10 công ty sản xuất hàng đầu có số lượng phim nhiều nhất:')
        print(top10_prod)
        plt.show()
    elif choice == 0:
        break;
