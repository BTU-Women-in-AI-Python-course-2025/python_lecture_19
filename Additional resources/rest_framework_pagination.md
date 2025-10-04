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

### 🧩 Example Use Case

`LimitOffsetPagination` is great when you want **direct control** over how many records to skip and how many to retrieve.

For example:

```bash
GET /products/?limit=3&offset=6
```

returns products **7, 8, and 9** (because it skips the first 6 items, then returns 3).

---

### ⚙️ Custom Offset Pagination Class

You can also define your own custom offset pagination class, similar to `PageNumberPagination`:

```python
from rest_framework.pagination import LimitOffsetPagination

class CustomOffsetPagination(LimitOffsetPagination):
    default_limit = 10                   # Default number of items per page
    limit_query_param = 'limit'          # Query param to set limit
    offset_query_param = 'offset'        # Query param to set offset
    max_limit = 100                      # Maximum allowed limit
```

Then use it in your viewset:

```python
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomOffsetPagination
```

Example requests:

```
GET /products/?limit=5&offset=0
GET /products/?limit=10&offset=20
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

### 🔍 Example API Response

**First request:**

```
GET /products/
```

```json
{
  "next": "http://localhost:8000/products/?cursor=cD0yMDI1LTEwLTA0KzEzJTNBMzUlM0E1Ni4zOTI3ODclMkIwMCUzQTAw",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Laptop",
      "created_at": "2025-10-04T13:40:00Z"
    },
    {
      "id": 2,
      "name": "Keyboard",
      "created_at": "2025-10-04T13:38:00Z"
    },
    ...
  ]
}
```

---

### ▶️ What Happens When You Go to the Next Page

When you call:

```
GET /products/?cursor=cD0yMDI1LTEwLTA0KzEzJTNBMzUlM0E1Ni4zOTI3ODclMkIwMCUzQTAw
```

Django REST Framework decodes the cursor internally — it represents the **position** of the last item from the previous page.

Example decoded content (conceptually):

```json
{
  "position": "2025-10-04T13:35:56.392787+00:00",
  "reverse": false
}
```

Then DRF performs a query like this under the hood:

```python
Product.objects.filter(created_at__lt="2025-10-04T13:35:56.392787+00:00")
               .order_by('-created_at')[:5]
```

This means:

| Step | Action                                                            |
| ---- | ----------------------------------------------------------------- |
| 1️⃣  | Select records **older** than the last one from the previous page |
| 2️⃣  | Keep same ordering (`-created_at`)                                |
| 3️⃣  | Return the next 5 items                                           |
| 4️⃣  | Encode a new cursor for the next request                          |

---

### ⏪ When Going to the Previous Page

If you click the `"previous"` link, DRF reverses the logic internally:

```python
Product.objects.filter(created_at__gt="2025-10-04T13:35:56.392787+00:00")
               .order_by('created_at')[:5]
```

Then it reverses the results before sending them back, so the order remains consistent for the client.

---

### ⚙️ Why CursorPagination Is Powerful

| Feature             | Description                                           |
| ------------------- | ----------------------------------------------------- |
| **Performance**     | No SQL `OFFSET`, uses indexed lookups instead         |
| **Consistency**     | Stable pagination even when new rows are inserted     |
| **Security**        | Cursor is cryptographically signed and base64 encoded |
| **Direction Aware** | Supports forward and backward navigation              |

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
