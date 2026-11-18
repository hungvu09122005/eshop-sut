# Performance Log Analysis & Bottleneck Triage Guide
## jmeter-performance-engineering Agent Skill

This reference documents the parsing, statistical validation, bottleneck isolation, and continuous performance regression detection mechanisms for JMeter JTL execution logs.

---

### 1. JTL Format Specification

JMeter logs execution metrics in either CSV (recommended) or XML format:

#### Standard CSV Columns:
`timeStamp,elapsed,label,responseCode,responseMessage,threadName,dataType,success,failureMessage,bytes,sentBytes,grpThreads,allThreads,URL,Latency,IdleTime,Connect`

* **`timeStamp`:** Epoch millisecond timestamp when the sampler started.
* **`elapsed`:** Total request duration in milliseconds.
* **`label`:** Transaction or Sampler identifier.
* **`responseCode`:** HTTP status code (e.g., `200`, `201`, `401`, `500`).
* **`success`:** Boolean (`true` or `false`).
* **`Connect`:** Time spent establishing the socket connection in milliseconds.

---

### 2. Statistical Validation & Metric Computation

1. **Total Samples ($N$):** Count of all parsed rows excluding header.
2. **Error Rate ($E$):** $\frac{\sum [success == false]}{N} \times 100\%$.
3. **Throughput ($TPS$):**
   $$TPS = \frac{N}{\frac{timeStamp_{\max} - timeStamp_{\min}}{1000}}$$
4. **Percentiles ($p50, p90, p95, p99$):**
   * Computed via linear interpolation over sorted `elapsed` values:
   $$k = (N - 1) \times \left(\frac{P}{100}\right),\quad v = d_{\lfloor k \rfloor} + (k - \lfloor k \rfloor) \times (d_{\lceil k \rceil} - d_{\lfloor k \rfloor})$$

---

### 3. Bottleneck Triage & Root Cause Analysis

When analyzing performance degradations, apply the following diagnostic decision tree:

```text
Latency Spike Detected?
 │
 ├── High Connect Time (> 50ms)?
 │    └── Network Congestion / TCP Backlog / Port Exhaustion
 │
 ├── High Latency (TTFB) on Single Endpoint?
 │    ├── High CPU Usage (> 85%)?
 │    │    └── CPU-Bound Operation (Bcrypt hashing, JSON parsing, heavy loops)
 │    │
 │    └── Low CPU Usage (< 20%)?
 │         └── I/O or Lock Contention (Database lock, unindexed disk scan, unbatched queries)
 │
 └── Linear RSS Memory Growth Over Time?
      └── In-Memory State Leak (Global dictionaries, unevicted caches, uncollected event listeners)
```

---

### 4. Optimization Categorization Matrix

All performance recommendations produced by the AI Agent must be rigorously triaged into one of three distinct categories:

| Category | Definition | Concrete Architectural Examples |
| :--- | :--- | :--- |
| **1. Feasible** | Pragmatic, proven, directly supported by the underlying tech stack with immediate ROI. | * Adding database indexes on foreign keys (`user_id`, `email`).<br>* Enabling SQLite WAL mode (`PRAGMA journal_mode = WAL;`).<br>* Wrapping multi-query checkout operations in an atomic transaction.<br>* In-memory caching for static product catalog reads. |
| **2. Requires Further Investigation** | Technically valid but entails architectural trade-offs, state migration, or complexity. | * Node.js Clustering / Multi-worker threads (requires migrating in-memory carts and sessions to Redis first).<br>* Read-Replica database splitting.<br>* Asynchronous message queues (RabbitMQ/Kafka) for order processing. |
| **3. Unsupported / Hallucinated** | Technically counterproductive, invalid, or impossible for the specific runtime architecture. | * **Connection Pooling on SQLite:** SQLite is an embedded single-file database; multi-connection pools cause locking crashes.<br>* **JVM GC Tuning on Node.js:** Node.js runs on Google V8 engine, not a JVM.<br>* **HTTP/2 Push without SSL/TLS.** |

---

### 5. Continuous Performance Regression Detection

To prevent performance regressions from slipping into production via CI/CD pipelines, use the **Two-Tier Regression Rule**:

$$\mathbf{Condition\;1:\;}\Delta p95 \ge +20.0\% \quad \mathbf{AND} \quad \mathbf{Condition\;2:\;}\Delta p95 \ge +15.0\text{ ms}$$

#### Why Both Tiers Are Mandatory:
* *Why not percentage alone?* If an endpoint increases from $2.0\text{ ms}$ to $2.8\text{ ms}$, the relative increase is $+40\%$, but the absolute delta is only $0.8\text{ ms}$ (harmless OS scheduling noise). Triggering a CI build failure here causes costly false alarms.
* *Why not absolute delta alone?* A $20\text{ ms}$ increase on a $3,000\text{ ms}$ report generation endpoint is negligible ($< 1\%$).
* **Conclusion:** Requiring both relative ($+20\%$) and absolute ($+15\text{ ms}$) increases eliminates false alarms while catching true regressions.
