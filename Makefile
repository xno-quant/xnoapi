.PHONY: install format lint check

# Cài đặt các công cụ cần thiết
install:
	pip install flake8 black

# Format code với Black (chuẩn PEP8)
format:
	black xnoapi

# Kiểm tra lỗi code với Flake8
lint:
	flake8 xnoapi

# Chạy cả format và lint cùng lúc
check: format lint
