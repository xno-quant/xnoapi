Đóng góp cho XNO
================

🤝 Đóng góp
~~~~~~~~~~~

Chúng tôi hoan nghênh mọi đóng góp từ cộng đồng! Bạn có thể:

- ⭐ Star dự án trên GitHub
- 🐛 Báo cáo lỗi hoặc đề xuất tính năng
- 📝 Cải thiện tài liệu
- 💻 Đóng góp code

🛠️ Các cách đóng góp
-------------------

**1. Báo cáo Bug**

Nếu bạn tìm thấy bug, hãy tạo Issue trên GitHub với thông tin sau:

.. code-block:: text

   **Bug Description:**
   Mô tả ngắn gọn về bug
   
   **Steps to Reproduce:**
   1. Bước 1
   2. Bước 2
   3. Kết quả không mong muốn
   
   **Expected Behavior:**
   Kết quả mong đợi
   
   **Environment:**
   - OS: Windows/Mac/Linux
   - Python version: 3.x
   - XNO API version: x.x.x
   
   **Code Sample:**
   ```python
   # Code để reproduce bug
   ```

**2. Đề xuất tính năng mới**

.. code-block:: text

   **Feature Request:**
   Tên tính năng đề xuất
   
   **Problem Statement:**
   Vấn đề cần giải quyết
   
   **Proposed Solution:**
   Giải pháp đề xuất
   
   **Use Case:**
   Trường hợp sử dụng cụ thể
   
   **Additional Context:**
   Thông tin bổ sung

**3. Cải thiện Documentation**

- Sửa lỗi chính tả và grammar
- Thêm ví dụ code rõ ràng
- Cập nhật thông tin lỗi thời
- Dịch documentation sang ngôn ngữ khác

**4. Đóng góp Code**

📋 Development Setup
~~~~~~~~~~~~~~~~~~~

**1. Fork và Clone Repository:**

.. code-block:: bash

   git clone https://github.com/xno-quant/xnoapi.git
   cd xnoapi

**2. Tạo Virtual Environment:**

.. code-block:: bash

   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows

**3. Install Dependencies:**

.. code-block:: bash

   pip install -e .
   pip install -r requirements-dev.txt

**4. Tạo Feature Branch:**

.. code-block:: bash

   git checkout -b feature/your-feature-name

🧪 Testing Guidelines
~~~~~~~~~~~~~~~~~~~~

**Chạy Tests:**

.. code-block:: bash

   # Chạy tất cả tests
   pytest
   
   # Chạy tests với coverage
   pytest --cov=xnoapi
   
   # Chạy tests cho module cụ thể
   pytest tests/test_stocks.py

**Viết Tests Mới:**

.. code-block:: python

   import pytest
   from xnoapi.vn.data import get_stock_hist
   
   def test_get_stock_hist():
       """Test lấy dữ liệu lịch sử cổ phiếu"""
       data = get_stock_hist("VIC", resolution='D')
       
       assert not data.empty
       assert 'Close' in data.columns
       assert 'Volume' in data.columns
       assert data['Close'].dtype in ['float64', 'int64']

📝 Code Style Guidelines
~~~~~~~~~~~~~~~~~~~~~~~

**1. Python Style:**

- Sử dụng PEP 8
- Type hints cho functions
- Docstrings cho classes và methods
- Meaningful variable names

.. code-block:: python

   def get_stock_data(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
       """
       Lấy dữ liệu cổ phiếu trong khoảng thời gian.
       
       Args:
           symbol: Mã cổ phiếu
           start_date: Ngày bắt đầu (YYYY-MM-DD)
           end_date: Ngày kết thúc (YYYY-MM-DD)
           
       Returns:
           DataFrame chứa dữ liệu OHLCV
           
       Raises:
           ValueError: Nếu symbol không hợp lệ
       """
       pass

**2. Error Handling:**

.. code-block:: python

   try:
       data = api_call(symbol)
       if data.empty:
           raise ValueError(f"No data found for {symbol}")
       return data
   except requests.RequestException as e:
       logger.error(f"API request failed: {e}")
       raise
   except Exception as e:
       logger.error(f"Unexpected error: {e}")
       raise

**3. Logging:**

.. code-block:: python

   import logging
   
   logger = logging.getLogger(__name__)
   
   def fetch_data(symbol: str):
       logger.info(f"Fetching data for {symbol}")
       try:
           data = api_request(symbol)
           logger.info(f"Successfully fetched {len(data)} records")
           return data
       except Exception as e:
           logger.error(f"Failed to fetch data: {e}")
           raise

🔄 Pull Request Process
~~~~~~~~~~~~~~~~~~~~~~

**1. Chuẩn bị PR:**

.. code-block:: bash

   # Đảm bảo code đúng style
   black xnoapi/
   flake8 xnoapi/
   
   # Chạy tests
   pytest
   
   # Commit changes
   git add .
   git commit -m "feat: add new stock analysis feature"
   
   # Push to fork
   git push origin feature/your-feature-name

**2. Tạo Pull Request:**

- Title rõ ràng và mô tả tính năng
- Link đến Issues liên quan
- Checklist các items đã hoàn thành
- Screenshots nếu có UI changes

**3. PR Template:**

.. code-block:: text

   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update
   
   ## Testing
   - [ ] Tests pass locally
   - [ ] New tests added for new features
   - [ ] Manual testing completed
   
   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] Documentation updated
   - [ ] No breaking changes

🏅 Recognition Program
~~~~~~~~~~~~~~~~~~~~~

**Contributor Levels:**

- **🌱 First-time Contributor**: First merged PR
- **⭐ Regular Contributor**: 5+ merged PRs  
- **🚀 Core Contributor**: 20+ merged PRs + major features
- **👑 Maintainer**: Long-term commitment + leadership

**Benefits:**

- Tên trong CONTRIBUTORS.md
- Special Discord role và badge

📈 Impact Tracking
~~~~~~~~~~~~~~~~~

**Metrics chúng tôi theo dõi:**

- Number of contributors
- Code quality improvements
- Bug fix rate
- Feature adoption rate
- Community growth
- User satisfaction

**Monthly Reports:**

- Top contributors recognition
- Feature usage statistics
- Community feedback summary
- Roadmap updates

🎯 Areas needing contribution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**High Priority:**

1. **Performance Optimization**
   - Caching mechanisms
   - Async API calls
   - Memory usage optimization

2. **Testing Coverage**
   - Unit tests cho new features
   - Integration tests
   - Performance benchmarks

3. **Documentation**
   - API reference completion
   - Tutorial improvements
   - Translation to English

**Medium Priority:**

4. **New Features**
   - Additional technical indicators
   - More market data sources
   - Portfolio optimization tools

5. **Developer Experience**
   - Better error messages
   - IDE integration improvements
   - Debugging tools

**Low Priority:**

6. **Nice-to-have**
   - GUI applications
   - Mobile SDK
   - Additional language bindings

🚀 Getting Started Tips
~~~~~~~~~~~~~~~~~~~~~~

**For New Contributors:**

1. Start with small issues labeled "good first issue"
2. Join our Discord for real-time help
3. Read existing code to understand patterns
4. Don't hesitate to ask questions
5. Focus on one thing at a time

**Best Practices:**

- Write tests for your code
- Keep PRs small and focused  
- Update documentation
- Be responsive to feedback
- Help review others' PRs