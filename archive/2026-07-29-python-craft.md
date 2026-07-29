# Python Craft — Day 103: Database Migrations — Alembic, Zero-Downtime

## 🎨 前端 Python Craft — Database Migrations: Alembic & Zero-Downtime 策略

> **Week 11 · Category: Data & Performance**

---

### 🌍 真实场景 / Real Scenario

你在做一个用户量增长中的 SaaS 产品。产品经理说："我们需要给 `orders` 表加一个 `status` 字段，并把所有旧数据的默认值设为 `'pending'`"。听起来简单，但：

- 生产数据库有 500 万行
- 服务 24/7 在线，不能停机
- 回滚必须安全

You're on a growing SaaS product. PM says: "add a `status` column to `orders`, backfill all existing rows to `'pending'`." Sounds simple, but 5M rows, 24/7 uptime, and safe rollback required.

---

### 🏗️ Alembic 基础：版本控制你的数据库结构
### Alembic Basics: Version-Control Your Schema

```python
# Step 1: Initialize Alembic in your project
# pip install alembic sqlalchemy

# alembic.ini and env.py are auto-generated
# alembic init alembic

# env.py — point to your models
from myapp.models import Base
target_metadata = Base.metadata

# Step 2: Create a migration
# alembic revision --autogenerate -m "add_status_to_orders"
```

生成的迁移文件 `versions/xxxx_add_status_to_orders.py`：

```python
from alembic import op
import sqlalchemy as sa

def upgrade():
    # ADD column with a server-side default (fast — doesn't rewrite all rows immediately on Postgres 11+)
    op.add_column('orders',
        sa.Column('status', sa.String(50), nullable=True)
    )

def downgrade():
    op.drop_column('orders', 'status')
```

---

### ⚠️ 零停机迁移：展开-迁移-收缩
### Zero-Downtime: Expand-Migrate-Contract Pattern

**❌ 危险做法（会锁表）**：
```python
# This acquires an ACCESS EXCLUSIVE lock on Postgres — blocks all reads/writes
def upgrade():
    op.add_column('orders',
        sa.Column('status', sa.String(50), nullable=False, server_default='pending')
    )
    # On 5M rows, this rewrites the whole table. Downtime!
```

**✅ 安全的三阶段做法**：

**Phase 1 — Expand（扩展）**: 加可空列，不设 NOT NULL，不回填
```python
def upgrade():
    op.add_column('orders',
        sa.Column('status', sa.String(50), nullable=True)  # nullable!
    )
    # Deploy app code that writes status on new rows
```

**Phase 2 — Migrate（迁移）**: 批量回填旧数据，每次处理小批量
```python
# Separate script — run as background job, NOT in migration
def backfill_status():
    from sqlalchemy import text
    engine = get_engine()
    batch_size = 10_000
    last_id = 0
    
    while True:
        with engine.begin() as conn:
            result = conn.execute(text("""
                UPDATE orders
                SET status = 'pending'
                WHERE id > :last_id AND status IS NULL
                LIMIT :batch_size
            """), {"last_id": last_id, "batch_size": batch_size})
            
            if result.rowcount == 0:
                break
            last_id += batch_size  # simplified; in prod use actual max id
        
        time.sleep(0.1)  # give DB breathing room
```

**Phase 3 — Contract（收缩）**: 确认回填完成后，再加 NOT NULL 约束
```python
def upgrade():
    # Postgres 12+ can add NOT NULL without table rewrite if constraint is valid
    op.alter_column('orders', 'status', nullable=False, server_default='pending')
```

---

### 🔄 常见模式：重命名列（高风险）
### Common Pattern: Renaming a Column (High Risk)

```
❌ 直接 ALTER COLUMN RENAME → 老代码立刻 crash
✅ 四阶段：
   1. 加新列 new_name
   2. 用 trigger 双写（old + new）
   3. 回填，部署读新列的代码
   4. 删旧列
```

---

### ❌ vs ✅ 迁移反模式

| ❌ 危险 | ✅ 安全 |
|--------|--------|
| 在迁移文件里跑大量数据操作 | 迁移只改结构，数据在应用层批量处理 |
| `NOT NULL` 没有默认值直接加 | 先加可空，回填后再加约束 |
| 迁移和部署同时进行 | 先迁移（向后兼容），再部署，再清理 |
| 跳过 downgrade() | 总是写 downgrade，哪怕是 `raise NotImplementedError` |

---

### 📚 References
- https://alembic.sqlalchemy.org/en/latest/
- https://gist.github.com/jberkus/6b1bcaf9724ff7cebbe0 (Postgres zero-downtime guide)
- https://brandur.org/postgres-queues (Expand-contract pattern)

### 🧒 ELI5
数据库迁移就像在一个开着的餐厅里重新装修厨房。你不能直接说"我们关门三天装修"——你得一点一点换：先装新的炉子，让两台炉子并排运行，确认新炉子正常了，再拆旧炉子。Alembic 就是帮你记录每一步装修步骤的施工日志。

Database migrations are like renovating a kitchen in an open restaurant. You can't close for 3 days — you install the new stove alongside the old one, run both, confirm the new one works, then remove the old one. Alembic is the renovation logbook that records every step.
