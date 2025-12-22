## Database Migration

This project uses [Alembic](https://alembic.sqlalchemy.org/) for database migrations.

create database:

```sql
CREATE DATABASE fastapi_db CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
```

1. **Generate migration script** (after modifying models):

   ```bash
   alembic revision --autogenerate -m "Your revision message"
   ```

2. **Apply migrations**:
   ```bash
   alembic upgrade head
   ```
