Hướng dẫn cài đặt
=================

📦 Cài đặt từ PyPI
------------------

Cách đơn giản nhất để cài đặt XNO API là thông qua PyPI:

.. code-block:: bash

   pip install xnoapi

📥 Cài đặt từ mã nguồn
----------------------

Nếu bạn muốn sử dụng phiên bản mới nhất từ GitHub:

.. code-block:: bash

   git clone https://github.com/xnoproject/xnoapi.git
   pip install ./xnoapi

🔑 Khởi tạo API Key
-------------------

Sau khi cài đặt, bạn cần khởi tạo API key để sử dụng:

.. code-block:: python

   from xnoapi import client
   
   # Khởi tạo client với API key
   client(apikey="your_api_key")

.. note::
   Để lấy API key miễn phí, vui lòng truy cập `xno.vn <https://xno.vn>`_ và đăng ký tài khoản.

📋 Yêu cầu hệ thống
-------------------

- Python 3.7+
- pandas
- numpy
- requests

Tất cả các dependencies sẽ được tự động cài đặt cùng với XNO API.