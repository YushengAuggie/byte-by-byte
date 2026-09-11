# 🎨 前端 / Frontend — Day 132
## React 18 并发特性实战：useTransition & useDeferredValue
**React 18 Concurrency in Practice: useTransition & useDeferredValue**

---

## 真实场景 / Real Scenario

你在做一个 dashboard，有一个搜索框，用户每次输入都会触发一个昂贵的列表过滤（1000+ 条记录）。输入卡顿，用户体验差。

You're building a dashboard with a search input that filters 1000+ records on every keystroke. It feels laggy.

---

## 核心概念 / Core Concept

React 18 引入了**并发渲染**：不是所有更新都一样紧急。

- `useTransition` — 把状态更新标记为"非紧急"（用户操作 > 过滤计算）
- `useDeferredValue` — 把一个值标记为"可以延迟同步"

---

## 代码示例 / Code Example

### ❌ 没有并发优化（卡顿）

```tsx
function SearchList() {
  const [query, setQuery] = useState('');
  const results = filterItems(query); // runs sync on every keystroke

  return (
    <>
      <input value={query} onChange={e => setQuery(e.target.value)} />
      <ItemList items={results} />
    </>
  );
}
```

### ✅ 用 useTransition（输入流畅，列表延迟更新）

```tsx
import { useState, useTransition } from 'react';

function SearchList() {
  const [query, setQuery] = useState('');
  const [filteredQuery, setFilteredQuery] = useState('');
  const [isPending, startTransition] = useTransition();

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const val = e.target.value;
    setQuery(val); // urgent: update input immediately
    startTransition(() => {
      setFilteredQuery(val); // non-urgent: defer the expensive filter
    });
  }

  const results = filterItems(filteredQuery);

  return (
    <>
      <input value={query} onChange={handleChange} />
      {isPending && <span>Filtering...</span>}
      <ItemList items={results} />
    </>
  );
}
```

### ✅ 用 useDeferredValue（更简洁，适合外部值）

```tsx
import { useState, useDeferredValue } from 'react';

function SearchList() {
  const [query, setQuery] = useState('');
  const deferredQuery = useDeferredValue(query);

  const results = filterItems(deferredQuery); // uses stale value until idle

  return (
    <>
      <input value={query} onChange={e => setQuery(e.target.value)} />
      <ItemList items={results} />
    </>
  );
}
```

---

## 猜猜输出 / Quiz — What happens?

```tsx
const [val, setVal] = useState('');
const deferred = useDeferredValue(val);

// User types "a", then "ab" rapidly.
// What does <HeavyComponent query={deferred} /> receive during typing?
```

A) `"a"` then `"ab"` immediately  
B) Possibly `""` then `"ab"` (skips `"a"`)  
C) Always the same as `val`  
D) Throws an error  

**Answer: B** — React may skip intermediate values if the UI is busy. The component receives whatever the scheduler decides is the "latest idle" value.

---

## useTransition vs useDeferredValue — 何时用哪个？

| | useTransition | useDeferredValue |
|---|---|---|
| 控制点 | 你控制 state setter | 你只有一个值（来自 props 或外部） |
| isPending | ✅ 有 | ❌ 没有 |
| 适合场景 | 自己的 state transition | 接收外部 prop 并需要延迟 |

---

## 📝 Quiz
```json
{"question":"Which React 18 hook gives you an `isPending` boolean to show a loading indicator during a non-urgent update?","options":["useDeferredValue","useTransition","useOptimistic","useSyncExternalStore"],"correct_index":1}
```

---

## 📚 References
- https://react.dev/reference/react/useTransition
- https://react.dev/reference/react/useDeferredValue
- https://react.dev/blog/2022/03/29/react-v18#new-feature-transitions

## 🧒 ELI5
就像餐厅服务员：先响应客人点菜（紧急），后端整理桌面（不紧急）。`useTransition` 让 React 先响应用户输入，再处理慢的计算。
Like a waiter who takes your order first (urgent) before clearing other tables (less urgent). `useTransition` tells React which updates are most important.
