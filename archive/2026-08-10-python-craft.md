# 🎨 Python Craft — Day 48: Secrets Management — env vars, Vault, keyring

## 真实场景 / Real Scenario

你在做一个后端服务，需要连接 PostgreSQL + Redis + 第三方 API。
You're building a backend service that connects to PostgreSQL + Redis + third-party APIs.

**问题：密钥放哪里？** / Where do secrets go?
- 硬编码在代码里 → 推上 GitHub → 黑客 / Hardcode → push to GitHub → hacker
- 只用环境变量 → 容器里如何注入？如何轮换？ / Env vars only → how to inject in containers? how to rotate?
- 正确答案：按安全等级分层 / Right answer: layered by security level

---

## 三层密钥管理 / Three-Tier Secrets Management

```
Level 1: Dev — .env file (gitignored)
Level 2: Staging/Prod — Environment variables injected by platform (K8s Secrets, ECS TaskDef)
Level 3: High-security/dynamic — Vault / AWS Secrets Manager (rotation, audit log)
```

---

## 代码示例 / Code Examples

### Level 1: python-dotenv + pydantic-settings

```python
# pip install python-dotenv pydantic-settings
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    redis_url: str
    api_key: str
    debug: bool = False

    class Config:
        env_file = ".env"           # loads from .env in dev
        env_file_encoding = "utf-8"

settings = Settings()               # reads from env or .env
print(settings.database_url)       # never print in prod!
```

```bash
# .env (NEVER commit this)
DATABASE_URL=postgresql://user:pass@localhost/mydb
REDIS_URL=redis://localhost:6379
API_KEY=sk-abc123
```

### Level 2: keyring — OS Keychain for local dev

```python
# pip install keyring
import keyring

# Store (run once, stores in macOS Keychain / Windows Credential Store)
keyring.set_password("my-app", "api_key", "sk-abc123")

# Retrieve
secret = keyring.get_password("my-app", "api_key")
# Returns None if not found — always handle!
if not secret:
    raise RuntimeError("API key not found in keychain")
```

### Level 3: HashiCorp Vault via hvac

```python
# pip install hvac
import hvac

client = hvac.Client(url="http://vault:8200", token=os.environ["VAULT_TOKEN"])

# Read secret
secret = client.secrets.kv.read_secret_version(path="myapp/prod")
db_password = secret["data"]["data"]["DB_PASSWORD"]

# Dynamic credentials — Vault generates a new DB user each time!
creds = client.secrets.database.generate_credentials("my-role")
# {"username": "v-token-abc123", "password": "A1B2-..."}  <- rotates automatically
```

---

## ❌ vs ✅ 对比 / Common Mistake

```python
# ❌ 永远不要这样做 / NEVER do this
DATABASE_URL = "postgresql://admin:supersecret@prod.db.internal/orders"

# ✅ 从环境变量读，有默认值处理
import os
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")
```

---

## 何时用哪个 / When to Use What

| 场景 | 方案 |
|------|------|
| 本地开发 | `.env` + `python-dotenv` |
| CI/CD | 平台 Secret Variables (GitHub Actions Secrets) |
| Kubernetes | K8s Secrets (base64, 非加密 → 配合 Sealed Secrets 或 External Secrets Operator) |
| 高安全需求 | HashiCorp Vault / AWS Secrets Manager (动态凭证、审计日志、自动轮换) |
| 本地 CLI 工具 | `keyring` — 存入 OS keychain |

---

## 📚 References
- https://docs.pydantic.dev/latest/concepts/pydantic_settings/
- https://developer.hashicorp.com/vault/docs/secrets/databases
- https://pypi.org/project/keyring/

## 🧒 ELI5
你的秘密日记：在家放在抽屉里（.env）；带去学校放在储物柜里（环境变量）；最重要的秘密交给学校的专门保险箱管理员（Vault），他还帮你定期换锁。
