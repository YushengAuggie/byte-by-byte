# 🎨 Python Craft — Day 50: Cryptography Basics — Hashing, Signing, bcrypt

*Category: Security & Production | Week 12*

---

## 场景 / Scenario

你在做一个 SaaS 平台，需要：
1. 安全存储用户密码
2. 给 API webhook 请求做签名验证
3. 生成文件校验和

这三个需求，三种不同的加密原语。

---

## 三类操作，三种工具

```
┌────────────┬──────────────┬─────────────────────────────┐
│ 需求        │ 工具         │ 特点                        │
├────────────┼──────────────┼─────────────────────────────┤
│ 密码存储    │ bcrypt       │ 慢哈希，有 salt，抗暴力破解  │
│ HMAC 签名  │ hmac + sha256│ 验证消息来源，防篡改         │
│ 数据校验和  │ hashlib      │ 快速，不可逆，不加盐         │
└────────────┴──────────────┴─────────────────────────────┘
```

---

## 代码示例

```python
# pip install bcrypt
import bcrypt
import hashlib
import hmac
import secrets

# ============================================
# 1. Password hashing with bcrypt
# ============================================
def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt(rounds=12)  # higher = slower = safer
    return bcrypt.hashpw(password.encode(), salt)

def verify_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed)

# Usage
hashed = hash_password("my_secret_pass")
print(verify_password("my_secret_pass", hashed))   # True
print(verify_password("wrong_pass", hashed))        # False

# ============================================
# 2. HMAC signature (webhook verification)
# ============================================
SECRET_KEY = b"super-secret-webhook-key"

def sign_payload(payload: bytes) -> str:
    sig = hmac.new(SECRET_KEY, payload, hashlib.sha256)
    return sig.hexdigest()

def verify_signature(payload: bytes, signature: str) -> bool:
    expected = sign_payload(payload)
    # Use compare_digest to prevent timing attacks!
    return hmac.compare_digest(expected, signature)

# Usage — mimics how Stripe/GitHub verify webhooks
body = b'{"event": "payment.success", "amount": 100}'
sig = sign_payload(body)
print(verify_signature(body, sig))  # True

# ============================================
# 3. File checksum (integrity verification)
# ============================================
def sha256_file(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()
```

---

## ❌ 常见错误 vs ✅ 正确做法

❌ `hashlib.md5(password)` 存密码 → MD5 无盐，彩虹表秒破  
❌ 自己写签名比较 `sig1 == sig2` → 时序攻击漏洞  
❌ `bcrypt.gensalt(rounds=4)` → 太快，不安全  
✅ 密码用 bcrypt/argon2，签名用 HMAC，校验用 SHA-256  
✅ 签名比较必须用 `hmac.compare_digest()`

---

## 猜猜输出什么？

```python
import hashlib
print(hashlib.sha256(b"hello").hexdigest() == 
      hashlib.sha256(b"hello").hexdigest())
```

**A)** False（每次不同）  
**B)** True（确定性哈希）✅  
**C)** Error  
**D)** 取决于系统

→ 答案：**B**。哈希是确定性的——相同输入永远输出相同摘要。这是文件校验和的基础。

---

## When to use / When NOT to use

| 场景 | 用什么 |
|------|--------|
| 用户密码存储 | bcrypt / argon2 |
| JWT / Webhook 签名 | HMAC-SHA256 |
| 文件完整性 / Git commit hash | SHA-256 |
| 数字证书 / TLS | RSA / ECDSA (asymmetric) |
| **不要用** | MD5、SHA-1 用于安全场景 |

---

## 📚 References
- https://docs.python.org/3/library/hmac.html
- https://pypi.org/project/bcrypt/
- https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html

## 🧒 ELI5
哈希就像榨果汁——苹果→果汁是单向的，你不能从果汁还原苹果。bcrypt 是"特别慢的榨汁机"——慢是故意的，让黑客暴力猜密码要等几百年。HMAC 是给果汁加了只有你和收件人知道的"秘密香料"，别人改了果汁，香料就对不上。
