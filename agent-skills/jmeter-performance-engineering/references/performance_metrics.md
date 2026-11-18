# Performance Metrics & Statistical Evaluation Guide
## jmeter-performance-engineering Agent Skill

This reference provides rigorous definitions, mathematical formulas, and interpretation rules for performance metrics collected during Apache JMeter executions.

---

### 1. The Perils of Average vs. Percentile Metrics

In performance engineering, relying solely on **Average (Arithmetic Mean)** response time is a dangerous anti-pattern. 

#### Why Averages Mislead:
* **Asymmetric Distributions:** Web request latencies follow long-tailed, log-normal distributions rather than Gaussian (bell-curve) shapes.
* **Outlier Masking:** A cluster of severe database query timeouts or garbage collection stalls can be completely masked by a high volume of sub-millisecond cached static reads.

#### Percentile Definitions:
* **Median ($p50$):** The 50th percentile. Represents the experience of the typical user. Exactly 50% of requests are faster, and 50% are slower.
* **90th Percentile ($p90$):** 90% of transactions completed within this latency threshold.
* **95th Percentile ($p95$):** Standard Service Level Agreement (SLA) metric for enterprise APIs. 95 out of 100 requests complete within this time window.
* **99th Percentile ($p99$):** Evaluates tail latency. Captures the worst 1% of transactions, often exposing database lock contention, thread starvation, or memory eviction stalls.

$$\text{Nearest-Rank Method:}\quad k = \left\lceil \frac{P}{100} \times N \right\rceil$$

---

### 2. Response Time Decomposition

JMeter breaks down request duration into three distinct chronological phases:

```text
[------------------------------ Elapsed Time ---------------------------------]
[-- Connect Time --]
[------------------ Latency (TTFB) -----------------]
                                                     [-- Response Download --]
```

1. **Connect Time (`Connect`):**
   * Time taken to establish the network socket connection with the target server.
   * Includes TCP three-way handshake ($SYN \rightarrow SYN-ACK \rightarrow ACK$) and TLS/SSL cryptographic negotiation.
   * *Diagnosis:* Elevated connect time indicates network congestion, saturated TCP accept queues, or firewall exhaustion.
2. **Latency (`Latency` / Time to First Byte - TTFB):**
   * Time from the moment the request is sent until the first byte of the HTTP response header is received back by JMeter.
   * Measures server-side processing, database execution, and network round-trip delay.
3. **Elapsed Time (`elapsed`):**
   * Total elapsed time from just before sending the request until the last byte of the response body has been completely ingested.

---

### 3. Throughput and Little's Law

#### Definition:
Throughput ($X$) measures the rate of successful work completed by the system per unit of time:

$$X = \frac{\text{Total Processed Transactions}}{\Delta t_{\text{elapsed}}}$$

* **Transactions Per Second (TPS):** Measures high-level business actions (e.g., full checkout workflows).
* **Requests Per Second (RPS):** Measures individual HTTP samplers.

#### Little's Law:
In a stable queuing system with no lost requests:

$$N = X \times R$$

* $N$: Number of Concurrent Virtual Users (in-flight concurrency).
* $X$: Throughput (Transactions per second).
* $R$: Total Residence Time (Response Time + User Think Time).

$$\text{Pacing / Think Time Formulation:}\quad Z = \frac{N}{X} - R_{\text{server}}$$

---

### 4. Error Rate and SLA Compliance

$$\text{Error Rate (\%)} = \left( \frac{\text{Failed Samples}}{\text{Total Samples}} \right) \times 100\%$$

#### Standard Industry SLA Gates:
* **Error Rate:** Must be $\le 1.0\%$ (critical transactional flows should achieve $0.00\%$).
* **Read-Heavy API Latency ($p95$):** $\le 500\text{ ms}$.
* **Transactional API Latency ($p95$):** $\le 1,200\text{ ms}$.
* **Auth-Heavy API Latency ($p95$):** $\le 800\text{ ms}$.
