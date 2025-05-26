# Django Management Commands

## What Are Django Commands?

Django provides built-in **management commands** for tasks like running the server, applying migrations, or creating users.

Run them via:

```bash
python manage.py <command> [options]
```

---

## Most Common Commands

| Command                 | Description                                |
| ----------------------- | ------------------------------------------ |
| `runserver`             | Starts the development server              |
| `migrate`               | Applies database migrations                |
| `makemigrations`        | Creates migration files from model changes |
| `createsuperuser`       | Creates an admin user                      |
| `shell`                 | Opens an interactive Python shell          |
| `startapp`              | Creates a new Django app                   |
| `startproject`          | Creates a new Django project               |
| `showmigrations`        | Shows applied and unapplied migrations     |
| `check`                 | Validates your project setup               |
| `flush`                 | Deletes all data from the database         |
| `loaddata` / `dumpdata` | Import/export data as JSON fixtures        |

---

## 📂 Example: Start a New App

```bash
python manage.py startapp blog
```

---

## Example: Create a Superuser

```bash
python manage.py createsuperuser
```

---

## Example: Use Django Shell

```bash
python manage.py shell
```

You can explore models interactively.

---

## Writing a Custom Command

To create a custom command:

1. Inside any app, create this structure:

```
your_app/
└── management/
    └── commands/
        └── sort_products.py
```

Each folder must include `__init__.py`.

---

### Example: Custom Command to Sort Products

```python
# your_app/management/commands/sort_products.py

from django.core.management.base import BaseCommand
from your_app.models import Product  # Replace with your actual app and model

class Command(BaseCommand):
    help = 'Sorts products by a given field and updates the "order" field sequentially'

    def add_arguments(self, parser):
        parser.add_argument(
            'sort_field',
            type=str,
            help='Field to sort by, e.g., "-id", "title"'
        )

    def handle(self, *args, **kwargs):
        sort_field = kwargs['sort_field']
        products = Product.objects.order_by(sort_field)

        for index, product in enumerate(products, start=1):
            product.order = index
            product.save(update_fields=['order'])

        self.stdout.write(self.style.SUCCESS(
            f"Updated order for {products.count()} products"
        ))
```

---

### ▶️ Run It

```bash
python manage.py sort_products -id
```

Sorts products by descending ID and updates their `order` field.

---

## 🧠 Summary

| Use Case        | Command/Example                      |
| --------------- | ------------------------------------ |
| Run server      | `python manage.py runserver`         |
| Migrations      | `makemigrations`, `migrate`          |
| Data management | `dumpdata`, `loaddata`, `flush`      |
| Custom task     | `python manage.py sort_products -id` |
