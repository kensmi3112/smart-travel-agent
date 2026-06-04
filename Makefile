.PHONY: run install clean help

# Default target
run:
	python grok_api_improved.py

# Install dependencies
install:
	pip install -r requirements.txt

# Clean up Python cache
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

# Help
help:
	@echo "Available commands:"
	@echo "  make run      - Run the main Grok API script"
	@echo "  make install  - Install dependencies from requirements.txt"
	@echo "  make clean    - Clean Python cache files"
	@echo "  make help     - Show this help message"
