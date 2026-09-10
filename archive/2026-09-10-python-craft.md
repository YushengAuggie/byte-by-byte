# 🎨 前端 / Frontend — Day 131
**主题：React 并发渲染 — useTransition & useDeferredValue 实战**
**Topic: React Concurrent Rendering — useTransition & useDeferredValue in Production**

---

## 真实场景 / Real Scenario

你在做一个电商搜索页，用户每输入一个字符就触发过滤。输入框卡顿，体验很差。

You're building an e-commerce search page. Every keystroke triggers filtering 10,000 items. The input feels laggy. How do you fix it without adding a debounce timer?

---

## 核心概念 / Core Concepts

React 18 引入了**并发特性（Concurrent Features）**：允许 React 中断、暂停、恢复渲染。

`useTransition` 和 `useDeferredValue` 都是告诉 React：**"这个更新不紧急，可以让位给更重要的更新。"**

---

## 代码示例 / Code Example

```tsx
import { useState, useTransition, useDeferredValue, useMemo } from 'react';

// ============ useTransition: 标记状态更新为"低优先级" ============
function SearchWithTransition({ items }: { items: string[] }) {
  const [query, setQuery] = useState('');
  const [filteredItems, setFilteredItems] = useState(items);
  const [isPending, startTransition] = useTransition();

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const value = e.target.value;
    setQuery(value); // ✅ 高优先级：输入框立即响应

    startTransition(() => {
      // ✅ 低优先级：过滤操作可以被打断
      setFilteredItems(items.filter(item =>
        item.toLowerCase().includes(value.toLowerCase())
      ));
    });
  }

  return (
    <div>
      <input value={query} onChange={handleChange} aria-label="Search input" />
      {isPending && <span>Loading...</span>}
      <ul>
        {filteredItems.map(item => <li key={item}>{item}</li>)}
      </ul>
    </div>
  );
}

// ============ useDeferredValue: 延迟派生值的更新 ============
function SearchWithDeferred({ items }: { items: string[] }) {
  const [query, setQuery] = useState('');
  const deferredQuery = useDeferredValue(query); // stale query for heavy computation

  // This memo only re-runs when deferredQuery changes (deferred, low priority)
  const filteredItems = useMemo(() =>
    items.filter(item =>
      item.toLowerCase().includes(deferredQuery.toLowerCase())
    ),
    [items, deferredQuery]
  );

  const isStale = query !== deferredQuery; // Show stale state to user

  return (
    <div style={{ opacity: isStale ? 0.7 : 1 }}>
      <input
        value={query}
        onChange={e => setQuery(e.target.value)}
        aria-label="Search input"
      />
      <ul>
        {filteredItems.map(item => <li key={item}>{item}</li>)}
      </ul>
    </div>
  );
}
```

---

## 猜猜输出 / Quiz

```tsx
const [isPending, startTransition] = useTransition();
const [count, setCount] = useState(0);

startTransition(() => setCount(c => c + 1));
console.log(isPending); // 在 startTransition 调用后同步打印
```

A. `true`
B. `false`
C. `undefined`
D. 报错

**答案：B** — `isPending` 在 `startTransition()` 调用后**同步读取**时仍为 `false`。`startTransition()` 只是调度了状态更新，不会同步修改当前渲染闭包中的 `isPending`。`isPending` 只有在 React **下一次渲染**期间 transition 未完成时才为 `true`。(Production mode assumed)

---

## ❌ vs ✅ 对比

```tsx
// ❌ 老方式：手动 debounce，有延迟且难与 React 状态协调
const debouncedSearch = useCallback(
  debounce((q) => setResults(filter(q)), 300), []
);

// ✅ 新方式：React 原生调度，无固定延迟，与浏览器空闲时间协调
const [, startTransition] = useTransition();
const handleChange = (q: string) => {
  setQuery(q);                               // urgent
  startTransition(() => setResults(filter(q))); // non-urgent
};
```

---

## 什么时候用 / When to Use

| | `useTransition` | `useDeferredValue` |
|---|---|---|
| 控制点 | 你控制状态更新 | 你只能接收值（props/外部） |
| 显示 pending | ✅ `isPending` | 手动比较 `value !== deferred` |
| 适合场景 | 按钮触发的慢渲染 | 父组件传入的搜索词 |

**不要用于：** 网络请求（用 Suspense）、副作用（用 useEffect）

---

## 📚 References
- https://react.dev/reference/react/useTransition
- https://react.dev/reference/react/useDeferredValue
- https://react.dev/blog/2022/03/29/react-v18#new-feature-transitions

## 🧒 ELI5
你在画画，同时还要回答朋友的问题。
`useTransition` 就像告诉大脑：「回答问题是紧急的，画画可以先暂停」。
React 也一样：输入框响应是紧急的，重新渲染大列表可以先等等。
