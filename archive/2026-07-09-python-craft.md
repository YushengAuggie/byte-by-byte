# Python Craft — Day 86

## 🎨 前端 / Python Craft — 配置管理：pydantic-settings & 12-Factor App

### 真实场景

你在做一个后端服务，需要在本地、staging 和 production 环境中使用不同的数据库、API key 和日志级别。如何让配置管理既安全又方便？

*You're building a backend service that needs different DB URLs, API keys, and log levels across local/staging/production. How do you manage this cleanly and securely?*

---

### 🌍 12-Factor App 配置原则

12-Factor App（Heroku 提出的云原生最佳实践）的第三条规则：

> **"将配置存储在环境变量中"**

这意味着：
- ❌ 不要把配置写死在代码里 (`DB_URL = "localhost:5432"`)
- ❌ 不要把 secrets 提交到 Git
- ✅ 用环境变量 + `.env` 文件（开发用）+ Secret Manager（生产用）

---

### 🔧 代码示例：pydantic-settings

```python
# pip install pydantic-settings python-dotenv

from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, HttpUrl, field_validator
from functools import lru_cache

class Settings(BaseSettings):
    # Required — will raise error if missing
    database_url: PostgresDsn
    secret_key: str
    
    # Optional with defaults
    debug: bool = False
    log_level: str = "INFO"
    api_rate_limit: int = 100
    
    # Nested config
    redis_url: str = "redis://localhost:6379/0"
    
    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        allowed = {"DEBUG", "INFO", "WARNING", "ERROR"}
        if v.upper() not in allowed:
            raise ValueError(f"log_level must be one of {allowed}")
        return v.upper()
    
    class Config:
        # Load from .env file automatically
        env_file = ".env"
        env_file_encoding = "utf-8"
        # Prefix all env vars: APP_DATABASE_URL, APP_SECRET_KEY
        env_prefix = "APP_"
        case_sensitive = False

# Singleton pattern — parse once, reuse everywhere
@lru_cache()
def get_settings() -> Settings:
    return Settings()

# Usage
settings = get_settings()
print(settings.database_url)   # postgresql://user:pass@localhost:5432/db
print(settings.debug)           # False (or True if APP_DEBUG=true)
```

**.env 文件（不要提交到 Git！）**

```env
APP_DATABASE_URL=postgresql://user:pass@localhost:5432/mydb
APP_SECRET_KEY=dev-secret-not-for-production
APP_DEBUG=true
APP_LOG_LEVEL=DEBUG
```

**.gitignore：**

```
.env
.env.local
*.env
```

---

### ❌ 常见错误 vs ✅ 正确做法

**❌ 错误：**
```python
# Hardcoded config
DB_URL = "postgresql://admin:password123@prod.db.example.com/mydb"
API_KEY = "sk-abc123def456"
```

**✅ 正确：**
```python
# pydantic-settings loads from environment
settings = get_settings()
# DB_URL and API_KEY come from env vars or Secret Manager
```

**❌ 错误：多套 if/else 判断环境**
```python
if os.environ.get("ENV") == "production":
    DB_URL = "..."
elif os.environ.get("ENV") == "staging":
    DB_URL = "..."
```

**✅ 正确：每个环境有自己的环境变量文件**
```
.env.local     → 开发
.env.staging   → staging CI/CD 注入
production     → Secret Manager (AWS SSM / HashiCorp Vault)
```

---

### 🧪 猜猜输出什么？

```python
import os
os.environ["APP_DEBUG"] = "1"
os.environ["APP_LOG_LEVEL"] = "debug"

settings = Settings()
print(type(settings.debug), settings.debug)
print(settings.log_level)
```

**A.** `<class 'str'> "1"`, `"debug"`
**B.** `<class 'bool'> True`, `"DEBUG"`
**C.** `<class 'bool'> True`, `"debug"`
**D.** Error: invalid log_level

<details><summary>显示答案 / Show Answer</summary>
**B.** pydantic-settings 会自动将 `"1"` 强制转换为 `bool True`，`field_validator` 将 `"debug"` 转换为大写 `"DEBUG"`。类型强制转换是 pydantic 的核心特性。
</details>

---

### 🤔 何时用 / 何时不用

**✅ 用 pydantic-settings 当：**
- FastAPI / Django / 任何 Python 后端项目
- 需要类型验证的配置
- 团队需要清晰的配置文档

**⚠️ 考虑额外方案当：**
- Production secrets → 用 AWS SSM Parameter Store / GCP Secret Manager + 在启动时注入环境变量
- 超复杂的分层配置（多个 override 层）→ 考虑 Dynaconf 或 Hydra (ML 项目)
- 微服务配置中心 → 用 Consul / etcd + 动态刷新

---

### 📚 References

- [pydantic-settings 官方文档](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [The Twelve-Factor App - Config](https://12factor.net/config)
- [FastAPI Settings & Environment Variables](https://fastapi.tiangolo.com/advanced/settings/)
- [AWS SSM Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html)

### 🧒 ELI5

配置就像食谱里的"盐"。不同的厨房（本地/生产）需要不同的量。
pydantic-settings 就是一个智能容器：你告诉它"我需要盐（类型：克，范围：0-100）"，它去冰箱（环境变量）拿，还会检查你拿的是不是真的盐。

*Config is like "salt" in a recipe. Different kitchens (local/prod) need different amounts. pydantic-settings is a smart container: you declare what you need (type + validation), it fetches from the environment, and verifies it's actually salt.*
