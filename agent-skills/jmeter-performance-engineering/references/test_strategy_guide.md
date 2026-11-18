# Performance Testing Strategy Guide
## jmeter-performance-engineering Agent Skill

This reference outlines workload modeling methodologies, scenario design archetypes, ramp-up calculations, and safety abort conditions for performance testing.

---

### 1. The Four Standard Performance Testing Archetypes

| Scenario Type | Primary Objective | Concurrency Profile | Typical Duration | Key Focus Metrics |
| :--- | :--- | :--- | :---: | :--- |
| **Load Testing** | Validate SLAs under expected peak production traffic | Constant sustained load ($N_{\text{peak}}$) | 10 – 60 min | $p95$, $p99$, Error Rate, Throughput |
| **Stress Testing** | Identify saturation threshold and maximum capacity limit | Step-up staircase ($N_{\text{base}} \rightarrow N_{\text{max}}$) | 15 – 45 min | Saturation inflection point, Knee-of-curve |
| **Spike Testing** | Evaluate resilience and recovery from sudden surges | Dual-stage: Low baseline $\rightarrow$ Immediate surge $\rightarrow$ Recovery | 5 – 15 min | Buffer overflow, MTTR, Data consistency |
| **Endurance / Soak** | Detect memory leaks, resource exhaustion, and state drift | Moderate constant load ($50\% - 70\% N_{\text{peak}}$) | 4 – 24 hours | Memory RSS slope ($d\text{RAM}/dt$), Connection leaks |

---

### 2. Workload Profile Modeling

```text
Load Testing:
Concurrency
    ^
50  |      /--------------------------\
    |     /                            \
 0  +----+------------------------------+---> Time
       60s (Ramp)       540s (Hold)     60s (Ramp-down)

Stress Testing:
Concurrency
    ^
    |                       /-- Break?
150 |               /------/
100 |       /------/
 50 |  /---/
 0  +--+---+---+---+---+---+---+---------> Time
      Step 1  Step 2  Step 3  Step 4

Spike Testing:
Concurrency
    ^
150 |           /-------\
    |          /|       |\
 20 |  -------/ |       | \------------
 0  +---------+-+-------+-+-------------> Time
       Normal   Spike   Hold  Recovery
```

---

### 3. Ramp-Up Calculation Methodology

* **Formula:**
  $$\text{Ramp-Up Time} = \frac{\text{Total Virtual Users}}{\text{Spawn Rate per Second}}$$
* **Best Practice:** Do not spawn all virtual users simultaneously at $t = 0$. Spawning 100 users in 0 seconds causes artificial thread contention on the test injector and server sockets.
* **Guideline:** Allow 1 to 2 seconds of ramp-up per 1–5 virtual users depending on injector hardware.

---

### 4. Pacing and Think Time Modeling

* **Real Users Do Not Act Instantly:** A script with 0ms think time executes requests faster than any human, producing inaccurate throughput and thread starvation.
* **Distribution Archetype:** Use **Gaussian Random Timers** centered around realistic cognitive delays:
  * Browse / Catalog Read: $1,500\text{ ms} \pm 500\text{ ms}$.
  * Form Fill / Profile Update: $2,500\text{ ms} \pm 1,000\text{ ms}$.
  * Checkout Decision: $3,000\text{ ms} \pm 1,000\text{ ms}$.

---

### 5. Automated Safety Abort Rules (Fail-Safe Conditions)

To protect non-production and shared staging environments, tests must abort immediately if any of the following fail-safe conditions are breached:

1. **Error Rate Spike:** Consecutive error rate $> 10\%$ over any 15-second rolling window.
2. **Latency Explosion:** $p95$ response time exceeds $10,000\text{ ms}$ for 3 consecutive intervals.
3. **Host Resource Saturation:** Injector or SUT host CPU utilization exceeds $95\%$ continuously for $> 30$ seconds.
4. **Socket / Connection Refusal:** Server begins rejecting TCP sockets (`ECONNREFUSED` or `ETIMEDOUT`).
