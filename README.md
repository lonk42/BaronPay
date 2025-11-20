# BaronPay

![Version](https://img.shields.io/badge/version-1.5.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Django](https://img.shields.io/badge/django-5.x-green.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A self-service point of sale kiosk web application built with Django. Designed for touchless checkout using RFID card readers that function as USB HID devices. The system uses a hidden text input field to capture card scans, enabling quick product selection and payment processing without physical interaction. Cart items preserve historical pricing, and all transactions are tracked through the Django admin interface.

![Example](baronpay_example.png)

## Getting Started

```bash
# Install dependencies
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Navigate to Django project
cd webapp

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver

# Create test data if you need some
python manage.py populate_products    # Create 12 dummy products with random prices ($0.20-$5.00)
python manage.py populate_sales_data  # 30 days, 50 cards, 5-40 sales/day
```

Access the kiosk at `http://127.0.0.1:8000/` and admin at `http://127.0.0.1:8000/admin/` (create superuser with `python manage.py createsuperuser`).