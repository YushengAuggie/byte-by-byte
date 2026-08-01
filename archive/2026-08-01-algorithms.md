# 🧮 Rotting Oranges (LeetCode #994) — BFS Deep Dive

> **Note:** This is a Saturday. The full content for this topic is in the [Saturday Deep Dive](./2026-08-01-deepdive.md). This file is a reference stub.

## Quick Summary

- **Pattern:** Graphs — Multi-Source BFS
- **LeetCode:** https://leetcode.com/problems/rotting-oranges/
- **NeetCode:** https://www.youtube.com/watch?v=y704fEOx0s0
- **Difficulty:** Medium

## Core Idea

Multi-source BFS: enqueue all initially rotten oranges simultaneously at time=0, then spread. Track `fresh_count` to detect unreachable oranges.

See [Saturday Deep Dive](./2026-08-01-deepdive.md) for complete theory, implementation, edge cases, and interview Q&A.
