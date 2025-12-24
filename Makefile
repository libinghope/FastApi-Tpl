
# 运行所有测试
test:
	pytest tests -v -s

# 运行指定文件的测试
# 使用方法: make test-file FILE=tests/api/v1/admin/sys/test_user.py
test-file:
	pytest $(FILE) -v -s

# 运行带有覆盖率报告的测试
test-cov:
	pytest --cov=app tests -v -s --cov-report=term-missing

# 启动开发服务器
run:
	uvicorn app.main:app --reload

# 交互式选择并运行测试文件
test-select:
	@./scripts/run_test.sh

# 显示帮助信息
help:
	@echo "Available commands:"
	@echo "  make test          - 运行所有测试"
	@echo "  make test-file     - 运行指定文件的测试 (usage: make test-file FILE=path/to/test)"
	@echo "  make test-select   - 交互式选择并运行测试文件"
	@echo "  make test-cov      - 运行带有覆盖率报告的测试"
	@echo "  make run           - 启动开发服务器"
