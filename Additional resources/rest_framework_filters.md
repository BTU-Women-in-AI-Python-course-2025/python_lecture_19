# Django REST Framework: Filtering

## 🔹 Why Filtering?

APIs often need to return a *subset* of data — for example, all products that are in stock or all users from a specific country.
Filtering allows clients to refine results without modifying the backend logic.

---

## ✅ Built-in Filter Types

| Type                | Description                                | Example Query     |
| ------------------- | ------------------------------------------ | ----------------- |
| Basic Filter        | Filter by exact match                      | `?category=books` |
| Search Filter       | Keyword search across fields               | `?search=laptop`  |
| Ordering Filter     | Sort results by one or more fields         | `?ordering=price` |
| DjangoFilterBackend | Advanced filtering (similar to Django ORM) | `?price__gt=100`  |

---

## 🛠️ Setup

Install `django-filter` if not already:

```bash
pip install django-filter
```

Add to `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'django_filters',
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ]
}
```

---

## 1️⃣ Basic Field Filtering

```python
from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = ['category', 'in_stock']  # 👈 basic field filtering
```

### 🔍 Example

`GET /products/?category=electronics&in_stock=True`

---

## 2️⃣ Search Filter

```python
from rest_framework import viewsets, filters

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
```

### 🔍 Example

`GET /products/?search=laptop`

> 🔎 Partial match is allowed (like SQL `LIKE`)

---

## 3️⃣ Ordering Filter

```python
from rest_framework import viewsets, filters

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['price', 'created_at']
```

### 🔍 Example

`GET /products/?ordering=price`
`GET /products/?ordering=-created_at`

---

## 4️⃣ DjangoFilterBackend (Advanced)

For more complex filtering (e.g. `price__gt`, date ranges):

```python
# Example 1
import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['min_price', 'max_price', 'category']
```

```python
# Example 2
import django_filters
from django.utils import timezone
from datetime import timedelta
from .models import Product

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    keyword = django_filters.CharFilter(method='filter_by_keyword')  # 👈 custom filter
    recent = django_filters.BooleanFilter(method='filter_recent')   # 👈 boolean custom filter

    class Meta:
        model = Product
        fields = ['min_price', 'max_price', 'category', 'keyword', 'recent']

    def filter_by_keyword(self, queryset, name, value):
        """Filter products by name or description containing keyword."""
        return queryset.filter(
            Q(name__icontains=value) | Q(description__icontains=value)
        )

    def filter_recent(self, queryset, name, value):
        """Return only products created in the last 7 days if recent=True."""
        if value:
            last_week = timezone.now() - timedelta(days=7)
            return queryset.filter(created_at__gte=last_week)
        return queryset
```

Then in your view:

```python
from django_filters.rest_framework import DjangoFilterBackend

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
```

### 🔍 Example

`GET /products/?min_price=50&max_price=150&category=books`

---

## 🧠 Summary Table

| Filter Type           | Required Setup     | Use Case                       |
| --------------------- | ------------------ | ------------------------------ |
| `filterset_fields`    | Minimal            | Field-level filtering          |
| `SearchFilter`        | `search_fields`    | Keyword search across fields   |
| `OrderingFilter`      | `ordering_fields`  | Sort results                   |
| `DjangoFilterBackend` | Custom `FilterSet` | Complex filtering with lookups |
