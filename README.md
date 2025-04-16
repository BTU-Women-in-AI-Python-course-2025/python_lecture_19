# Django Rest Framework

- **Pagination** - https://www.django-rest-framework.org/api-guide/pagination/:
  - Efficiently handle large datasets by delivering data in manageable chunks, enhancing performance and user experience.
- **Django Filters** - https://www.django-rest-framework.org/api-guide/filtering/:
  - Add filtering capabilities to your API endpoints, allowing clients to retrieve only the necessary data and making your API more flexible.
- **Commands** - https://docs.djangoproject.com/en/5.1/howto/custom-management-commands/

### 📚 **Student Task: Filter and Paginate Your API + Create a Custom Command**

1. **Use an existing DRF API** (or create a simple model like `Product` with `name`, `category`, `price`).

2. **Add Pagination**  
   - Use `PageNumberPagination` or `LimitOffsetPagination` in `settings.py`.
   - Create custom pagination class
   - Ensure `/products/` returns paginated results.

3. **Add Filtering**  
   - Use `django-filter` to allow filtering by fields like `category` or price range (`price__gte`, `price__lte`).
   - Example: `/products/?category=Books&price__lte=100`

4. **Create a Custom Django Management Command**  
   - Create a command like `python manage.py count_products` that prints the number of products in the database.

---

#### 🔍 Example Output:
- `GET /products/?category=Books&price__lte=100` → filtered + paginated list.
- Console:  
  ```
  Total Products: 128
  ```
