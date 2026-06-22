# 🏗️ 系统设计 / System Design — Day 59
**Topic:** Design an LLM Inference Serving System
**Date:** 2026-06-22 | **Difficulty:** Expert

---

## 想象你在设计... / Imagine You're Designing...

你是 OpenAI 的基础设施工程师。公司刚刚发布了 GPT-X，每秒涌入数万个请求。每个请求都需要调用一个数十亿参数的模型。如何在保证低延迟的同时，让成本不至于爆炸？

You're an infra engineer at OpenAI. The company just launched GPT-X, and tens of thousands of requests per second are flooding in. Every request needs to run through a billion-parameter model. How do you keep latency low without bankrupting the company?

---

## 架构图 / Architecture Diagram

```
                    ┌─────────────────────────────┐
                    │        Load Balancer          │
                    │     (Request Routing)         │
                    └────────────┬────────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
     ┌────────▼────────┐ ┌───────▼───────┐ ┌───────▼────────┐
     │  Inference Node  │ │ Inference Node│ │ Inference Node │
     │  (A100 x 8)     │ │  (A100 x 8)  │ │  (A100 x 8)   │
     │  ┌────────────┐  │ │              │ │                │
     │  │  KV Cache  │  │ │              │ │                │
     │  │  (Per-req) │  │ │              │ │                │
     │  └────────────┘  │ │              │ │                │
     └────────┬────────┘ └───────┬───────┘ └───────┬────────┘
              │                  │                  │
     ┌────────▼──────────────────▼──────────────────▼────────┐
     │                   Continuous Batching Engine            │
     │    (vLLM / TensorRT-LLM — PagedAttention)              │
     └────────────────────────────┬───────────────────────────┘
                                  │
              ┌───────────────────┼────────────────────┐
              │                   │                    │
     ┌────────▼──────┐   ┌────────▼──────┐   ┌────────▼──────┐
     │  Model Store   │   │ Request Queue │   │  Result Store  │
     │  (S3 + NVMe)   │   │  (Redis/Kafka)│   │  (Cache/Redis) │
     └───────────────┘   └───────────────┘   └───────────────┘
```

**关键组件 / Key Components:**
1. **Continuous Batching** — 不等批次填满就开始推理，动态合并请求
2. **PagedAttention (KV Cache)** — 将 KV cache 分页管理，像操作系统管理内存一样
3. **Tensor Parallelism** — 一个模型切分到多张 GPU 卡上并行推理
4. **Speculative Decoding** — 用小模型预测 token，大模型验证，加速 3-5x

---

## 核心权衡 / Key Tradeoffs

**为什么不用普通 batching？**
传统 static batching 需要等最长请求完成才能处理下一批。Continuous batching 允许请求随时进出队列，GPU 利用率从 ~30% 提升到 ~80%+。

**Tensor Parallelism vs Pipeline Parallelism:**
- Tensor Parallelism: 把一层的权重切分到多卡，通信在层内 → 低延迟，适合单请求
- Pipeline Parallelism: 把不同层放到不同卡，流水线处理 → 高吞吐，适合批量

**Model Quantization tradeoffs:**
- FP16 → INT8: 内存减半，速度翻倍，精度损失 <1%
- INT4 (GPTQ/AWQ): 内存减少 4x，精度损失稍大，适合低优先级任务

---

## 别踩这个坑 / Common Mistakes

❌ **用 sequence length 做 batching** — 不同请求长度差异极大，固定 batch size 严重浪费 GPU
✅ 用 token budget 做 batching，按 token 数而非请求数打包

❌ **KV Cache 不做内存管理** — 长上下文会吃光所有显存，新请求无法调度
✅ 用 PagedAttention，把 KV cache 切成固定大小的 page 按需分配

❌ **冷启动未预热** — 第一个请求触发模型加载，延迟高达分钟级
✅ 预热策略 + 模型预加载到 GPU，保持 warm pool

❌ **忽略 prefill 和 decode 阶段差异** — Prefill（处理 prompt）是计算密集型，Decode（生成 token）是内存带宽密集型，应该分开优化
✅ Prefill-decode disaggregation：不同节点专门处理两个阶段

---

## 容量估算 / Capacity Estimation

假设 10K QPS，平均 prompt 500 tokens，输出 200 tokens：
- 每请求 FLOPs ≈ 2 × params × tokens (llama-70B = ~140B × 700 = 98T FLOPs)
- 一块 A100 (312 TFLOPS FP16) 可处理 ~3 req/s
- 10K QPS 需要 ~3,300 A100 → 实际用 continuous batching 后大概 ~600-800 卡

---

## 🧒 ELI5

想象一家餐厅（GPU）同时做很多道菜（请求）。普通餐厅一次只做一桌的菜，做完再做下一桌。聪明的餐厅会把多桌的菜同时放进烤箱，一锅出。LLM 推理系统也一样，KV Cache 就像厨师的记忆，记住每道菜做到哪一步了。

---

## 📚 References
- vLLM (PagedAttention paper): https://arxiv.org/abs/2309.06180
- Continuous Batching Explained: https://www.anyscale.com/blog/continuous-batching-llm-inference
- TensorRT-LLM Docs: https://nvidia.github.io/TensorRT-LLM/
- Prefill-Decode Disaggregation: https://arxiv.org/abs/2401.09670
