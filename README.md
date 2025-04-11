# Phân Tích Dữ Liệu Giáo Dục Thế Giới - Đồ Án Cuối Kỳ Môn Lập Trình Python

## Mục lục
1. [Giới thiệu](#giới-thiệu)
2. [Các chức năng chính](#các-chức-năng-chính)
3. [Hướng dẫn sử dụng](#hướng-dẫn-sử-dụng)
4. [Cấu trúc dự án](#cấu-trúc-dự-án)
5. [Video demo](#video-demo)
6. [Một số kết quả nổi bật](#một-số-kết-quả-nổi-bật)
7. [Tác giả](#tác-giả)

---

## Giới thiệu
Dự án này tập trung vào việc phân tích dữ liệu giáo dục của các quốc gia trên thế giới. Mục tiêu chính là khám phá các xu hướng, mối quan hệ và sự khác biệt trong các chỉ số giáo dục như chi tiêu chính phủ cho giáo dục, tỷ lệ người biết chữ, tỷ lệ nhập học và tỷ lệ học sinh trên giáo viên.

Dự án sử dụng các công cụ và thư viện Python như `pandas`, `matplotlib`, `seaborn`, và `tkinter` để xử lý dữ liệu, trực quan hóa và xây dựng giao diện người dùng.

---

## Các chức năng chính

### 1. Xử lý dữ liệu
- **Xóa cột không cần thiết**: Loại bỏ các cột không hữu ích như `country_code`.
- **Xử lý giá trị thiếu**:
  - Xóa các hàng có số lượng giá trị thiếu lớn hơn hoặc bằng 4.
  - Điền giá trị thiếu bằng giá trị trung bình của từng quốc gia hoặc giá trị trung bình toàn cục.
- **Loại bỏ dữ liệu không liên quan**: Loại bỏ các hàng chứa giá trị không đại diện cho quốc gia cụ thể (ví dụ: `IDA only`, `World`, `High income`).

### 2. Phân tích dữ liệu
- **Thống kê mô tả**:
  - Đếm số lượng giá trị thiếu (`NaN`) và giá trị bằng 0 trong từng cột.
  - Tính toán các chỉ số thống kê như trung bình, độ lệch chuẩn, giá trị lớn nhất và nhỏ nhất.
- **Phân tích mối quan hệ**:
  - Mối quan hệ giữa chi tiêu giáo dục (% GDP) và tỷ lệ người biết chữ.
  - So sánh tỷ lệ học sinh trên giáo viên ở cấp tiểu học và trung học.
- **Phân tích theo quốc gia**:
  - Tỷ lệ người biết chữ trung bình theo quốc gia.
  - Tỷ lệ chi tiêu giáo dục (% GDP) trung bình theo quốc gia.
  - Phân bố các quốc gia theo mức độ chi tiêu giáo dục (Thấp, Trung bình, Cao).

### 3. Trực quan hóa dữ liệu
- **Biểu đồ đường**:
  - Xu hướng thay đổi tỷ lệ người biết chữ qua các năm.
  - Chi tiêu giáo dục (% GDP) theo thời gian.
- **Biểu đồ cột**:
  - Top 10 quốc gia có tỷ lệ người biết chữ cao nhất.
  - Top 10 quốc gia có tỷ lệ chi tiêu giáo dục cao nhất.
- **Biểu đồ tròn**:
  - Phân bố các quốc gia theo mức độ chi tiêu giáo dục.
- **Biểu đồ kết hợp**:
  - So sánh tỷ lệ hoàn thành tiểu học và số học sinh/giáo viên ở Việt Nam.

### 4. Giao diện người dùng
- **Tải và hiển thị dữ liệu**:
  - Cho phép người dùng chọn file CSV và hiển thị dữ liệu trong bảng.
- **Lọc dữ liệu**:
  - Lọc dữ liệu theo cột, điều kiện và giá trị cụ thể.
- **Chỉnh sửa dữ liệu**:
  - Thêm, xóa và chỉnh sửa dữ liệu trực tiếp từ giao diện.
- **Phân trang**:
  - Hiển thị dữ liệu theo từng trang để dễ dàng quản lý.

---

## Hướng dẫn sử dụng

### 1. Clone dự án
- Sử dụng lệnh sau để clone dự án về máy:
  ```bash
  git clone git@github.com:Nnguyen-dev2805/PYTHON_FinalProject.git
  ```

### 2. Cài đặt môi trường
- Cài đặt Python (phiên bản >= 3.7).
- Cài đặt các thư viện cần thiết:
  ```bash
  pip install pandas matplotlib seaborn tkinter pandastable
  ```

### 3. Chạy chương trình
- Chạy file `Chinh.py` để mở giao diện người dùng:
  ```bash
  python Chinh.py
  ```

### 4. Các bước phân tích
1. **Tải dữ liệu**: Chọn file CSV chứa dữ liệu giáo dục.
2. **Xử lý dữ liệu**:
   - Kiểm tra và xử lý giá trị thiếu.
   - Loại bỏ dữ liệu không liên quan.
3. **Phân tích và trực quan hóa**:
   - Chọn các biểu đồ hoặc phân tích từ giao diện.
   - Lọc dữ liệu theo nhu cầu.
4. **Xuất dữ liệu**: Lưu dữ liệu đã xử lý vào file `clean_data.csv`.

---

## Cấu trúc dự án

```
16_PhanTichGiaoDucTheGioi/
├── source-code/
│   ├── Chinh.py                # File chính, giao diện người dùng
│   ├── plot_utils/
│   │   ├── drawplot.py         # Các hàm vẽ biểu đồ
│   ├── main.ipynb              # Notebook phân tích dữ liệu
│   ├── README.md               # Tài liệu dự án
├── data/
│   ├── data.csv                # Dữ liệu gốc
│   ├── clean_data.csv          # Dữ liệu đã xử lý

```

---

## Video demo
Xem video demo tại đây: [YouTube Demo](https://youtu.be/_5jgEoz8XUA)

---

## Một số kết quả nổi bật

### 1. Xu hướng chi tiêu giáo dục (% GDP) theo thời gian
- Chi tiêu giáo dục có xu hướng dao động nhưng tương đối ổn định từ năm 2000-2015.
- Sau năm 2020, mức chi tiêu giảm mạnh, có thể do tác động của đại dịch COVID-19.

### 2. Mối quan hệ giữa chi tiêu giáo dục và tỷ lệ biết chữ
- Hệ số tương quan là 0.23, cho thấy mối quan hệ yếu và dương.
- Tăng chi tiêu giáo dục không đồng nghĩa với việc tăng mạnh tỷ lệ biết chữ.

### 3. Phân bố quốc gia theo mức độ chi tiêu giáo dục
- Nhóm chi tiêu trung bình (3-6% GDP) chiếm phần lớn.
- Nhóm chi tiêu thấp (0-3% GDP) chiếm khoảng 18%.
- Nhóm chi tiêu cao (>6% GDP) chiếm tỷ lệ ít, phản ánh sự đầu tư mạnh mẽ vào giáo dục ở một số quốc gia.

---

## Tác giả
- **Trương Nhất Nguyên**  
  - MSSV: 23110273  
  - GitHub: [Nnguyen-dev2805](https://github.com/Nnguyen-dev2805)

- **Nguyễn Hoàng Hà**  
  - MSSV: 23110207  
  - GitHub: [nguyenhoangha0710](https://github.com/nguyenhoangha0710)

- **Đặng Ngọc Tài**  
  - MSSV: 23110304  
  - GitHub: [taidang05](https://github.com/taidang05)

- **Nghiêm Quang Huy**  
  - MSSV: 23110222  
  - GitHub: [HuyinCP](https://github.com/HuyinCP)

- **Nguyễn Tấn Yên**  
  - MSSV: 23110369
  - GitHub: [NguyenTanYen](https://github.com/NguyenTanYen)

