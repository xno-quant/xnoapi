# Đóng góp tài liệu cho `xnoapi`

Chúng tôi hoan nghênh mọi đóng góp nhằm cải thiện tài liệu cho dự án `xnoapi`. Vui lòng làm theo các bước dưới đây để bắt đầu.

---

## Bước 1: Fork & clone dự án

Truy cập vào github: `https://github.com/xnoproject/xnoapi`
Tiếp theo fork dự án về github của bạn và clone về.

```bash
git clone https://github.com/your-username/xnoapi
```

---

## Bước 2: Tạo nhánh mới từ main

Vui lòng đặt tên nhánh theo chuẩn `docs/ten-chu-de`:

```bash
git checkout -b docs/your-topic
```

---

## Bước 3: Viết tài liệu

Viết tài liệu mới vào `index.rst` trong thư mục `source/`

---

## Bước 4: Build tài liệu cục bộ

```bash
.\make.bat html # Trên Windows
```

Sau đó mở file `build/html/index.html` trong trình duyệt để xem tài liệu đã build.

---

## Bước 5: Gửi Pull Request

- Commit các thay đổi với message rõ ràng.
- Tạo pull request từ nhánh `docs/your-topic` vào nhánh `main`.
- Mô tả thay đổi trong phần mô tả PR.

---

## Tips khi viết tài liệu (Sphinx + reStructuredText)

Để giúp tài liệu của `xnoapi` rõ ràng, dễ đọc và dễ maintain, bạn vui lòng tuân theo các quy tắc sau khi viết file `.rst` (sử dụng Sphinx):

---

### 1. Tiêu đề rõ ràng, có cấu trúc

Sử dụng các ký tự lặp lại để thể hiện cấp độ tiêu đề trong `.rst`:

| Cấp độ | Ký hiệu | Ví dụ                        |
| ------ | ------- | ---------------------------- |
| 1      | `===`   | `XnoAPI Documentation`       |
| 2      | `---`   | `Module: xnoapi.vn.data`     |
| 3      | `~~~`   | `Function: get_hist`         |
| 4      | `^^^^`  | `Parameters` hoặc `Examples` |

**Ví dụ trong file `.rst`:**

```rst
XnoAPI Documentation
====================

Module: xnoapi.vn.data
----------------------

Function: get_hist
~~~~~~~~~~~~~~~~~~
```

### 2. Dùng `autodoc` để tự động generate tài liệu từ docstring

Chèn directive sau vào file `.rst`:

- Function:

```rst
.. autofunction:: xnoapi.vn.data.stocks.get_hist
```

- Class & Method:

```rst
.. autoclass:: xnoapi.api.MyAPIClient
   :members:
   :undoc-members:
   :show-inheritance:
```

- Lưu ý: đảm bảo thư mục chứa mã nguồn đã được thêm vào `sys.path` trong file `conf.py`.

### 3. Thêm ví dụ sử dụng (code example)

Sử dụng directive `.. code-block:: python` để minh họa cách dùng function/class:

```rst
Examples
^^^^^^^^

.. code-block:: python

   from xnoapi.vn.data.stocks import get_hist

   df = get_hist("VIC", frequency="1d")
   print(df.head())
```

### 4. Mô tả tham số và kết quả trả về (nếu không dùng `autodoc`)

Bạn có thể viết tay mô tả function như sau:

```rst
get_hist
~~~~~~~~

Lấy dữ liệu lịch sử của cổ phiếu.

:param asset_name: Mã cổ phiếu, ví dụ 'VIC'
:type asset_name: str
:param frequency: Tần suất, ví dụ '1d', '1w'
:type frequency: str
:return: DataFrame chứa dữ liệu lịch sử
:rtype: pandas.DataFrame
```

### 5. Tổ chức nội dung tài liệu bằng `toctree`

Chia nhỏ các phần tài liệu theo module:

```rst
source/
├── index.rst
├── usage.rst
├── api/
│   ├── stocks.rst
│   ├── derivatives.rst
```

Trong `index.rst`, khai báo mục lục bằng `toctree`:

```rst
.. toctree::
   :maxdepth: 2
   :caption: Nội dung

   usage
   api/stocks
   api/derivatives
```

### 6. Checklist trước khi gửi Pull Request

Chia nhỏ các phần tài liệu theo module:

- [ ] Đặt tiêu đề rõ ràng, theo đúng cấu trúc tiêu đề

- [ ] Sử dụng .. autofunction:: hoặc .. autoclass:: nếu có thể

- [ ] Thêm ví dụ sử dụng bằng code-block

- [ ] Ghi rõ :param: và :return: nếu không dùng autodoc

- [ ] Kiểm tra hiển thị bằng lệnh make html trước khi gửi PR

- [ ] Nếu viết bài hướng dẫn, đính kèm link vào mục Tutorials trong docs

Cảm ơn bạn đã đóng góp cho `xnoapi`! 💙
