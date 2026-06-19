# 🏗️ 系统设计 / System Design — Day 57
**主题 / Topic:** Design a Secrets Management System (Vault)
**日期 / Date:** 2026-06-18

---

## 🏗️ 系统设计 / System Design

**Secrets Management System（密钥管理系统）— 像 HashiCorp Vault**

---

### 场景 / Scenario

想象你在一家有 200 个微服务的公司工作。每个服务都需要数据库密码、API 密钥、TLS 证书……如果这些密钥硬编码在代码里，一旦泄露，后果不堪设想。你需要一个中心化的"密钥银行"。

You work at a company with 200 microservices. Each needs DB passwords, API keys, TLS certs. Hardcoding secrets is a disaster waiting to happen. You need a centralized "secrets bank."

---

### 架构图 / Architecture

```
        ┌─────────────────────────────────────────┐
        │           Secrets Management System      │
        └─────────────────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
    ┌─────▼─────┐  ┌───────▼──────┐  ┌─────▼──────┐
    │   Auth    │  │   Secrets    │  │   Policy   │
    │  Service  │  │    Engine    │  │   Engine   │
    │(JWT/Cert) │  │  (KV, PKI,  │  │  (ACL/    │
    │           │  │  Database)  │  │  RBAC)    │
    └─────┬─────┘  └───────┬──────┘  └─────┬──────┘
          │                │                │
          └────────────────┼────────────────┘
                           │
               ┌───────────▼──────────┐
               │     Audit Log         │
               │  (Immutable, append-  │
               │   only, encrypted)    │
               └──────────────────────┘
                           │
               ┌───────────▼──────────┐
               │    Storage Backend    │
               │ (Consul/etcd/Dynamo) │
               └──────────────────────┘

  Clients:
  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
  │  Service A  │   │  CI/CD Job  │   │  Operator   │
  │ (K8s SA)    │   │ (GitHub     │   │ (mTLS cert) │
  │             │   │  Actions)   │   │             │
  └─────────────┘   └─────────────┘   └─────────────┘
```

---

### 核心组件 / Core Components

**1. Authentication Methods（认证方式）**
- **Kubernetes Auth:** Pod 用 Service Account Token 认证 → 获取临时凭证
- **AppRole:** CI/CD 流水线使用 role_id + secret_id 获取 token
- **AWS/GCP IAM:** 云上服务用 instance identity 认证
- **mTLS 证书认证:** 操作员使用客户端证书

**2. Secrets Engines（密钥引擎）**
- **KV（Key-Value）:** 静态密钥存储，支持版本化（v1 vs v2）
- **Dynamic Secrets:** 按需生成数据库凭证，TTL 后自动吊销 ← 杀手级功能
- **PKI Engine:** 自动颁发短期 TLS 证书（24h 有效）
- **Transit Engine:** 加密即服务，应用不存明文，只存密文

**3. Policy Engine（策略引擎）**
```hcl
# Vault HCL policy
path "secret/data/db/*" {
  capabilities = ["read"]  # read-only for app
}
path "secret/data/db/admin" {
  capabilities = ["deny"]  # override: block admin creds
}
```

**4. Dynamic Secrets 工作流 / Dynamic Secrets Flow**
```
Service → Vault: "我需要 PostgreSQL 凭证"
Vault → DB: CREATE ROLE app_xyz_1234 WITH PASSWORD '...' VALID UNTIL '...+1h'
Vault → Service: {username: "app_xyz_1234", password: "...", ttl: 3600}
[1小时后 / 1 hour later]
Vault → DB: DROP ROLE app_xyz_1234  ← 自动清理
```

---

### 关键权衡 / Key Tradeoffs

| 方案 | 优点 | 缺点 |
|------|------|------|
| **Dynamic Secrets** | 泄露影响有限（TTL 短）| 需 DB 支持动态用户 |
| **Static Secrets + Rotation** | 兼容性好 | 轮换期间有窗口期 |
| **Seal/Unseal（Shamir）** | 高安全性，防单点 | 重启需手动解封，运维负担 |
| **Auto-unseal（KMS）** | 自动运维 | 依赖云 KMS，费用增加 |

**Seal/Unseal 机制：**  
Vault 启动时处于 Sealed 状态（完全加密）。需要 n-of-m Shamir Key Shares 才能解封。生产中通常配合 AWS KMS/GCP KMS 做 Auto-unseal。

---

### High Availability

```
                  ┌─────────────┐
    requests ────▶│  Load Balancer│
                  └──────┬──────┘
             ┌───────────┼───────────┐
      ┌──────▼──┐  ┌──────▼──┐  ┌──────▼──┐
      │ Vault 1 │  │ Vault 2 │  │ Vault 3 │
      │ (active)│  │(standby)│  │(standby)│
      └─────────┘  └─────────┘  └─────────┘
             └───────────┼───────────┘
                  ┌──────▼──────┐
                  │   Consul /  │
                  │   Raft HA   │
                  └─────────────┘
```
- **Raft 共识:** Vault Enterprise 内置 Raft，无需 Consul
- **只有 Active 节点处理写请求，Standby 可处理读（PR 模式）**

---

### 别踩这个坑 / Common Mistakes

❌ **Token 不设 TTL** — Token 泄露后永久有效，应设短 TTL + 自动续约  
❌ **Root Token 常用** — Root Token 只应用于初始化，然后吊销  
❌ **密钥缓存过长** — 应用缓存 Dynamic Secret 超过 TTL，导致认证失败  
❌ **忽略 Audit Log** — 合规系统必须开启 audit device，且做不可变存储  
❌ **Vault 单点** — 生产环境必须 HA，Vault 挂了 = 所有服务挂了  

---

### 📚 References

- [HashiCorp Vault Documentation](https://developer.hashicorp.com/vault/docs)
- [Vault Architecture Deep Dive](https://developer.hashicorp.com/vault/docs/internals/architecture)
- [Dynamic Secrets: Database Secrets Engine](https://developer.hashicorp.com/vault/docs/secrets/databases)

### 🧒 ELI5

想象你家有一个超级保险箱（Vault）。你不把钥匙直接给每个家庭成员，而是让他们去保险箱说"我是小明，我要开车库"。保险箱验证身份后，吐出一把**临时钥匙**，1小时后自动失效。如果临时钥匙丢了？没关系，它很快就过期了。这就是 Secrets Management。

Imagine a super-safe at home (Vault). Instead of giving each family member permanent keys, they go to the safe and say "I'm Xiaoming, I need the garage key." The safe verifies their identity and gives a **temporary key** that expires in 1 hour. Lost key? No big deal — it expires soon anyway. That's secrets management.
