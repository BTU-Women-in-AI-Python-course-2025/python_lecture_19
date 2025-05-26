# Django Management Commands

## 🔹 What Are Django Commands?

Django provides a set of built-in **management commands** you can run from the terminal to interact with your project.

You use them like this:

```bash
python manage.py <command> [options]
```

---

## ✅ Most Common Commands

| Command                 | Description                                         |
| ----------------------- | --------------------------------------------------- |
| `runserver`             | Starts the development server                       |
| `migrate`               | Applies database migrations                         |
| `makemigrations`        | Creates migration files from model changes          |
| `createsuperuser`       | Creates an admin user                               |
| `shell`                 | Opens a Python shell with Django context            |
| `startapp`              | Creates a new Django app                            |
| `startproject`          | Creates a new Django project                        |
| `showmigrations`        | Displays all migrations and their status            |
| `sqlmigrate`            | Shows raw SQL for a given migration                 |
| `check`                 | Checks for problems in your project                 |
| `collectstatic`         | Gathers all static files into one folder (for prod) |
| `flush`                 | Resets the database                                 |
| `loaddata` / `dumpdata` | Import/export data using fixtures                   |

---

## 📂 Example: Create App

```bash
python manage.py startapp blog
```

Creates a folder structure for a new Django app named `blog`.

---

## 👤 Example: Create Superuser

```bash
python manage.py createsuperuser
```

You'll be prompted to enter username, email, and password.

---

## 🔄 Example: Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

First command creates migration files, second applies them to the database.

---

## 🐚 Example: Django Shell

```bash
python manage.py shell
```

You can import and play with your models:

```python
from blog.models import Post
Post.objects.all()
```

---

## 🧪 Example: Test Database with `flush`

```bash
python manage.py flush
```

Deletes **all data** in the database and resets primary keys. Useful in development.

---

## 🗃️ Fixtures (Backup / Load Data)

```bash
python manage.py dumpdata > data.json
python manage.py loaddata data.json
```

Export and import data — great for saving sample data.

---

## 🛠️ Custom Management Commands

You can create your own command by placing a file in:

```
<your_app>/management/commands/say_hello.py
```

Make sure to include `__init__.py` files in both `management/` and `commands/` folders.

### ✅ Example: `say_hello` Command

```python
# say_hello.py
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Greets the user with their name'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Your name')

    def handle(self, *args, **kwargs):
        name = kwargs['name']
        self.stdout.write(self.style.SUCCESS(f'Hello, {name}! Welcome to Django.'))
```

### ▶️ Run the Command

```bash
python manage.py say_hello Mariam
```

### ✅ Output

```
Hello, Mariam! Welcome to Django.
```

---

## 🧠 Summary

| Category       | Example Command                         |
| -------------- | --------------------------------------- |
| Server         | `runserver`                             |
| Database       | `makemigrations`, `migrate`, `flush`    |
| Admin & Shell  | `createsuperuser`, `shell`              |
| App Management | `startapp`, `startproject`              |
| Data           | `loaddata`, `dumpdata`                  |
| Debugging      | `check`, `showmigrations`, `sqlmigrate` |
| Custom         | Create under `management/commands/`     |
