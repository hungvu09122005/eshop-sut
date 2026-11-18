---
name: jmeter-performance-engineering
description: End-to-end automated performance engineering skill using Apache JMeter. Discovers REST APIs, designs test strategies (Load, Stress, Spike, Soak), parameterizes test data, generates valid JMX test plans, executes headless tests, parses raw JTL logs, analyzes percentiles/TPS/bottlenecks, detects p95 regressions, and generates Markdown reports across arbitrary web applications.
---

# Skill: JMeter Performance Engineering

## 1. Skill Name
`jmeter-performance-engineering` (Automated Performance Testing & Log Analysis Skill)

## 2. Description
The `jmeter-performance-engineering` skill provides an automated, rigorous, and reusable workflow for end-to-end Performance Testing and Performance Engineering using **Apache JMeter** (executed in headless Non-GUI mode).

The skill is built strictly following the **AI-First strategy with Human-in-the-Loop governance**. It avoids hardcoding application-specific logic, enabling seamless reuse across arbitrary web architectures (Node.js Express, Java Spring Boot, Python FastAPI/Django, Go Gin, etc.). It autonomously discovers APIs, parameterizes multi-user test data, builds structurally valid `.jmx` test plans, enforces mathematical rigor on execution logs (`.jtl`), isolates system bottlenecks, and evaluates Service Level Agreements (SLAs).

---

## 3. Objective & Guiding Principles

* **Empirical Integrity:** Never fabricate test numbers, response times, or error counts. All reported metrics must derive directly from raw execution logs or verifiable mathematical formulas.
* **Architecture Agnostic (Reusability):** Decoupled from any single System Under Test (SUT). Analyzes any REST API repository dynamically.
* **Three Mandatory Endpoint Groups:** Automatically analyzes and covers:
  1. **Auth-heavy:** Authentication, JWT signing, password hashing, lockout logic.
  2. **Read-heavy:** Catalog queries, entity detail reads, cached data retrievals.
  3. **Transactional:** State mutations, order checkouts, inventory updates, database commits.
* **Statistical Rigor:** Relies on true percentiles ($p50, p90, p95, p99$), throughput ($TPS$), and connect times rather than misleading arithmetic averages.
* **Human-in-the-Loop Safety:** Demands explicit user confirmation prior to executing high-load stress/spike tests, modifying databases, or altering application code.

---

## 4. When to Use & When Not to Use

### When to Use:
* Designing automated Load, Stress, Spike, or Soak test suites for RESTful APIs.
* Parameterizing concurrent multi-user workloads using CSV datasets.
* Generating, validating, and linting Apache JMeter test plans (`.jmx`).
* Analyzing raw `.jtl` execution logs and extracting statistical summaries.
* Diagnosing critical path bottlenecks (database lock contention, event loop blocking, memory leaks).
* Establishing Shift-Left CI/CD Continuous Performance Testing pipelines with $p95$ regression gates.

### When Not to Use:
* Simple functional single-user unit tests (use Jest, Mocha, JUnit, or PyTest instead).
* Front-end UI visual rendering and usability evaluations (use GUI Testing / Cypress / Playwright skills).
* Distributed denial-of-service (DDoS) simulations without authorized target infrastructure.

---

## 5. Skill Architecture: The 9 Core Modules

```text
┌────────────────────────────────────────────────────────────────────────┐
│               jmeter-performance-engineering Skill Pipeline             │
└────────────────────────────────────────────────────────────────────────┘
  │
  ├── [Module 1: API Discovery & Analysis] ──> API_INVENTORY.md
  │     Discover endpoints, auth mechanism, DB models, classify groups
  │
  ├── [Module 2: Performance Test Strategy] ─> PERFORMANCE_TEST_STRATEGY.md
  │     Workload modeling, Little's Law, VUs, Ramp-up, Pacing, SLAs
  │
  ├── [Module 3: Test Data Engineering] ─────> TEST_DATA_DESIGN.md + CSVs
  │     CSV generation, account isolation, DB seeder, collision prevention
  │
  ├── [Module 4: JMeter Test Plan Gen] ──────> *.jmx (Load, Stress, Spike)
  │     HTTP Defaults, Headers, Extractors, Assertions, Timers, Parent TCs
  │
  ├── [Module 5: Execution Management] ──────> Non-GUI CLI Execution
  │     Pre-flight safety check, JVM tuning, JTL logs, HTML dashboards
  │
  ├── [Module 6: Performance Log Analysis] ──> AI_PERFORMANCE_ANALYSIS.md
  │     Parse JTL, compute Mean/Median/p90/p95/p99/TPS, regression comparison
  │
  ├── [Module 7: Bottleneck & Optimization] ─> Triage (Feasible/Investigate/Unsupported)
  │     Database locks, indexing, memory leak detection, event loop stalls
  │
  ├── [Module 8: Endurance Threshold] ───────> ENDURANCE_ANALYSIS.md
  │     Sustained VUs, RSS memory slope, short-term vs long-term soak audit
  │
  └── [Module 9: Final Report Generation] ───> Standardized Markdown Reports
        Summary reports, SLA evaluation gates, compliance matrices
```

---

### Module 1: API Discovery & Analysis
* **Mechanism:** Inspects backend routes, controllers, middleware, and database schemas.
* **Extraction:** Detects HTTP methods (`GET`, `POST`, `PUT`, `DELETE`), URL paths, headers, query parameters, JSON payload schemas, and response formats.
* **Authentication Mapping:** Identifies auth schemes (JWT Bearer, Session Cookies, OAuth2, API Keys) and token expiry/renewal lifecycles.
* **Classification:** Categorizes discovered routes into *Auth-heavy*, *Read-heavy*, and *Transactional*.
* **Output:** `API_INVENTORY.md`.

---

### Module 2: Performance Test Strategy
* **Workload Modeling:** Uses Little's Law ($N = X \times R$) to balance concurrent threads ($N$), target throughput ($X$), and residence time ($R$).
* **Scenario Profiles:**
  1. *Load Testing:* Constant sustained peak load (validates standard SLAs).
  2. *Stress Testing:* Step-up staircase load (identifies saturation threshold and knee-of-curve).
  3. *Spike Testing:* Dual-stage sudden surge (tests queue buffers, MTTR, and recovery stability).
  4. *Endurance / Soak Testing:* Prolonged moderate load (tests memory RSS growth and connection leaks).
* **Pacing:** Configures Gaussian Random Timers (e.g., $1,500\text{ ms} \pm 500\text{ ms}$) to simulate realistic human cognitive hesitation.
* **Output:** `PERFORMANCE_TEST_STRATEGY.md`.

---

### Module 3: Test Data Engineering
* **Data Parameterization:** Identifies dynamic fields required per request (credentials, IDs, search queries, payment data).
* **Concurrency Isolation:** Enforces 1 unique user account per Virtual User thread (`Recycle on EOF = False`, `Stop Thread on EOF = True`) to prevent account lockout or cart collisions.
* **Database Synchronization:** Provides or verifies automated asynchronous seed scripts to populate test databases before test execution.
* **Output:** `TEST_DATA_DESIGN.md` and CSV datasets (`users.csv`, `products.csv`, etc.).

---

### Module 4: JMeter Test Plan Generation
* **Structure:** Generates clean, well-formed Apache JMeter `.jmx` XML files.
* **Components Standard:**
  * `TestPlan` & `ThreadGroup` (standard or ConcurrencyThreadGroup).
  * `ConfigTestElement` (HTTP Request Defaults with `${BASE_URL}` and `${PORT}`).
  * `HeaderManager` (Content-Type `application/json`, Authorization `Bearer ${token}`).
  * `CSVDataSet` (dataset bindings).
  * `TransactionController` (Parent sample enabled for business step aggregation).
  * `HTTPSamplerProxy` (HTTP endpoints).
  * `JSONPostProcessor` (Extracting session tokens, entity IDs, order numbers).
  * `ResponseAssertion` (Dual-level: HTTP status code + business payload validation).
  * `GaussianRandomTimer` (Pacing simulation).
  * `ResultCollector` (Summary Report, Aggregate Report, or Graph Results).
* **Validation:** Validated via `scripts/validate_jmx.py`.

---

### Module 5: Test Execution Management
* **Pre-flight Safety Checklist:**
  1. Verify Java runtime and JMeter binary (`jmeter -v`).
  2. Verify target server availability (`curl -I http://target:port/health`).
  3. Verify CSV test datasets exist and contain sufficient rows ($\ge \text{Virtual Users}$).
  4. Verify `.jmx` test plan syntax with validator.
* **Execution Command:**
  ```bash
  jmeter -n -t <test_plan>.jmx -l <output>.jtl -e -o <report_dashboard_dir>/
  ```
* **Guardrails:** Prevents accidental overwrite of existing `.jtl` logs without explicit authorization.

---

### Module 6: Performance Log Analysis
* **Execution:** Parsed and computed using `scripts/analyze_jtl.py`.
* **Statistical Metrics:**
  * Sample Counts: Total, Success, Failures, Error Rate ($E\%$).
  * Latencies (ms): Min, Max, Arithmetic Mean, Median ($p50$), $p90$, $p95$, $p99$, Standard Deviation.
  * Throughput ($TPS$): Calculated as $\frac{N}{\Delta t_{\text{test}}}$.
  * Connect Time: TCP socket establishment and TLS handshake latency ($p95$).
* **Regression Comparison:** Compares run metrics against baseline; flags regression if:
  $$\Delta p95 \ge +20.0\% \quad \mathbf{AND} \quad \Delta p95 \ge +15.0\text{ ms}$$
* **Output:** `AI_PERFORMANCE_ANALYSIS.md` and structured JSON.

---

### Module 7: Bottleneck & Optimization Analysis
* **Diagnostic Decision:** Distinguishes between CPU-bound, I/O-bound, memory-bound, and network-bound degradations.
* **Three-Tier Optimization Triage:**
  1. **Feasible:** Database indexes, SQLite WAL mode, atomic SQL transactions, catalog caching.
  2. **Requires Further Investigation:** Multi-worker clustering, state offloading to Redis, read/write splitting.
  3. **Unsupported / Hallucinated:** Connection pooling on local SQLite, JVM GC tuning on Node.js/Python runtimes.

---

### Module 8: Endurance Threshold Analysis
* **Short-term vs Long-term Distinction:**
  * *Short-term stability (10–30 min):* Validates transient throughput and latency stability.
  * *Extended Soak (4–24 hours):* Mandatory to verify true endurance; monitors memory leak slope ($d\text{RAM}/dt$), file descriptor leaks, and database table bloat.
* **Strict Assertion:** Never declare long-term endurance verified from a short stress test.
* **Output:** `ENDURANCE_ANALYSIS.md`.

---

### Module 9: Report Generation
* **Templating:** Uses `assets/report_template.md` and `scripts/generate_report.py`.
* **Standard Deliverables:**
  * Executive Summary & Quality Gate Status (PASS / FAIL).
  * Latency Percentile Distribution Table.
  * Granular Transaction & Endpoint Breakdown.
  * Hardware & Resource Utilization Correlation.
  * Bottleneck Isolation & Root Cause Findings.

---

## 6. Human-in-the-Loop Governance & Safety Guardrails

To protect systems and preserve academic/engineering integrity, the AI Agent must pause and seek explicit human confirmation before performing any of the following:

1. **Executing Tests on Live Staging/Production Servers:** Confirmation required to verify target URL, maintenance window, and authorization.
2. **Executing High-Concurrency Stress or Spike Workloads:** Confirmation required to review max thread count and prevent injector server freeze.
3. **Database State Mutation or Seeding:** Confirmation required prior to executing scripts that insert, alter, or drop database records.
4. **Overwriting Existing Artifacts:** Confirmation required before deleting or overwriting prior `.jtl` logs or HTML reports.
5. **Code Modification:** The skill must never modify application source code directly; optimizations are delivered as actionable recommendations.
6. **Academic/Audit Reports:** The AI Agent must never draft personal student reflections (e.g., AI Critique, AI Audit Report) on behalf of the user.

---

## 7. Supporting Automation Scripts

The skill provides three standalone, dependency-free Python 3 scripts in `scripts/`:

### 1. `validate_jmx.py`
Validates test plan XML syntax, thread groups, timers, extractors, assertions, and CSV existence.
```bash
python3 scripts/validate_jmx.py --jmx <test_plan>.jmx --csv-dir <data_dir>
```

### 2. `analyze_jtl.py`
Parses raw JTL files (CSV/XML), computes percentiles ($p50, p90, p95, p99$), TPS, error rates, and compares against baselines.
```bash
python3 scripts/analyze_jtl.py --jtl <run>.jtl --compare <baseline>.jtl --json <summary>.json --markdown <summary>.md
```

### 3. `generate_report.py`
Renders structured Markdown summary reports from analyzed JSON metrics and SLA thresholds.
```bash
python3 scripts/generate_report.py --metrics-json <summary>.json --scenario "Load Test" --sut-name "EShop" --output <report>.md
```

---

## 8. Usage Instructions & Example Prompts

### Example 1: Full Pipeline on a New Project
```text
@jmeter-performance-engineering
Please analyze the REST API in repository './order-service', identify Auth-heavy, Read-heavy, and Transactional endpoints, create an API_INVENTORY.md, design a 50-VU Load Test strategy, and generate a validated 23120268_Load.jmx test plan.
```

### Example 2: Analyzing Execution Logs & Detecting Regression
```text
@jmeter-performance-engineering
Analyze the raw execution log '23120268_Stress_20261118.jtl' using analyze_jtl.py. Compare it against baseline '23120268_Load_20261118.jtl'. Check if there is any p95 regression exceeding +20% and +15ms, identify the slowest endpoint, and generate a performance summary report.
```
