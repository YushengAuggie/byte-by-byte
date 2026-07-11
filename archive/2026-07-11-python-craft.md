# 🐍 Python Craft — Day 88 · Feature Flags: Simple Implementation to LaunchDarkly

**分类 / Category:** Practical Patterns — Week 8

---

## 什么是 Feature Flag / What Are Feature Flags

Feature flags (also called feature toggles) let you deploy code to production but control whether it's enabled for users. This decouples **deployment** from **release**.

**核心用途 / Core Uses:**
- A/B testing
- Canary releases (10% → 50% → 100%)
- Kill switches for problematic features
- Dark launches (collect data before enabling)

---

## Level 1: 最简实现 / Simplest Implementation

```python
# Simple dict-based feature flags
FEATURE_FLAGS = {
    "new_checkout_flow": True,
    "ai_recommendations": False,
    "dark_mode": True,
}

def is_enabled(flag_name: str) -> bool:
    return FEATURE_FLAGS.get(flag_name, False)

# Usage
if is_enabled("new_checkout_flow"):
    return new_checkout()
else:
    return old_checkout()
```

**问题 / Problems:** Can't change at runtime without redeployment. No per-user targeting.

---

## Level 2: 带环境变量的配置 / Env-var Based

```python
import os

def is_enabled(flag_name: str, default: bool = False) -> bool:
    # Check env var: FEATURE_AI_RECOMMENDATIONS=true
    env_key = f"FEATURE_{flag_name.upper()}"
    value = os.environ.get(env_key, "").lower()
    if value in ("1", "true", "yes"):
        return True
    if value in ("0", "false", "no"):
        return False
    return default
```

**改进：** Can change per-environment without code changes.

---

## Level 3: 基于百分比的 Rollout / Percentage Rollout

```python
import hashlib

def is_enabled_for_user(flag_name: str, user_id: str, rollout_pct: float) -> bool:
    """Deterministic: same user always gets same result."""
    # Hash user_id + flag_name for consistent assignment
    hash_input = f"{flag_name}:{user_id}".encode()
    hash_value = int(hashlib.md5(hash_input).hexdigest(), 16)
    user_bucket = (hash_value % 100) / 100.0  # 0.0 to 0.99...
    return user_bucket < rollout_pct

# 10% rollout
if is_enabled_for_user("new_search", user.id, 0.10):
    return new_search(query)
```

**关键：** Hash-based bucketing ensures the same user always lands in the same bucket (no flickering).

---

## Level 4: LaunchDarkly / Production SDK Pattern

```python
import ldclient
from ldclient.config import Config

ldclient.set_config(Config("sdk-key-here"))
client = ldclient.get()

def is_enabled(flag_key: str, user_context: dict, default: bool = False) -> bool:
    """
    user_context = {
        "kind": "user",
        "key": "user-123",           # required
        "email": "user@example.com",
        "plan": "enterprise",
        "country": "US"
    }
    """
    return client.variation(flag_key, user_context, default)

# Target by attribute: enterprise users get new feature
# No code change needed — configure in LaunchDarkly UI
```

**LaunchDarkly 的优势 / LaunchDarkly Advantages:**
- Streaming updates (flag changes apply in <100ms without restart)
- Targeting rules (by email, plan, country, custom attributes)
- Percentage rollouts with consistent bucketing
- Audit log of every flag change
- Scheduled rollouts

---

## 实际设计考虑 / Production Considerations

```python
# 1. Cache flags locally to avoid latency
# LaunchDarkly SDK does this automatically

# 2. Default to OFF for new features
# If the flag system is down, features should fail closed

# 3. Clean up old flags (flag debt is real!)
# A flag that's been at 100% for 3 months should become default behavior

# 4. Use structured logging to track flag evaluations
import structlog
log = structlog.get_logger()

def is_enabled(flag: str, user_id: str) -> bool:
    result = _evaluate_flag(flag, user_id)
    log.info("feature_flag_evaluated", flag=flag, user_id=user_id, result=result)
    return result
```

---

## 面试要点 / Interview Points

**Q: How do you avoid "flag debt"?**
> Set a TTL when creating flags. When a rollout hits 100% and stays there for a sprint, the flag goes on the cleanup backlog. Old flags = dead code that still runs.

**Q: How do you test code with feature flags?**
> Three approaches: (1) inject flag evaluator as dependency, mock in tests; (2) use test environments with flags always ON/OFF; (3) use LaunchDarkly's test data source.
