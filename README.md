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


## 使用docker安装mysql

```bash
docker run --name local-mysql --restart unless-stopped -e MYSQL_ROOT_PASSWORD=12345678 -p 3306:3306 -v mysql-data:/var/lib/mysql -d mysql:8.0
```

## 安装redis

```bash
docker run --name redis --restart unless-stopped -v redis-data:/data -p 6379:6379 -d redis
```

## 创建数据库

```sql
CREATE DATABASE `tpl_db` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```
