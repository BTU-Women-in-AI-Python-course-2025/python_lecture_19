# Django REST Framework: Pagination

## 🔹 What is Pagination?

**Pagination** lets you control how many results are returned in a single API response — useful when working with large datasets.

⚙️ Without pagination, a single request might return thousands of records, slowing down your API.

---

## ✅ Pagination Styles in DRF

Django REST Framework offers three main pagination classes:

| Class                   | Description                                                         |
| ----------------------- | ------------------------------------------------------------------- |
| `PageNumberPagination`  | Standard page numbers (`?page=2`)                                   |
| `LimitOffsetPagination` | Limit + offset (`?limit=10&offset=20`)                              |
| `CursorPagination`      | Encrypted cursor-based pagination (best for performance & security) |

---

## 1️⃣ `PageNumberPagination`

### 📁 `settings.py`

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,
}
```

### 🔍 Example API Call

`GET /products/?page=2`

```json
{
  "count": 12,
  "next": "http://localhost:8000/products/?page=3",
  "previous": "http://localhost:8000/products/?page=1",
  "results": [
    // 5 product objects here
  ]
}
```

---

## 2️⃣ `LimitOffsetPagination`

### 📁 `settings.py`

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 5,
}
```

### 🔍 Example API Call

`GET /products/?limit=5&offset=10`

```json
{
  "count": 100,
  "next": "http://localhost:8000/products/?limit=5&offset=15",
  "previous": "http://localhost:8000/products/?limit=5&offset=5",
  "results": [
    // next 5 results starting from offset 10
  ]
}
```

---

## 3️⃣ `CursorPagination`

Best for real-time data, secure, and resistant to data shifts (e.g. due to inserts/deletes).

### 📁 `settings.py`

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.CursorPagination',
    'PAGE_SIZE': 5,
}
```

> You can also set a custom ordering in your `CursorPagination` subclass:

```python
from rest_framework.pagination import CursorPagination

class ProductCursorPagination(CursorPagination):
    page_size = 5
    ordering = '-created_at'
```

---

## ⚙️ Custom Pagination Class

You can define a reusable pagination class in your project:

```python
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'
    max_page_size = 100
```

Then use it in your viewset:

```python
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
```

---

## 🧠 Summary Table

| Pagination Type | Params               | Best For                    |
| --------------- | -------------------- | --------------------------- |
| Page Number     | `?page=2`            | Simple client-side paging   |
| Limit & Offset  | `?limit=5&offset=10` | Frontends with more control |
| Cursor          | `?cursor=XYZ...`     | Real-time apps, performance |
