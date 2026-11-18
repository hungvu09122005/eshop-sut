# JMeter Best Practices Guide
## jmeter-performance-engineering Agent Skill

This reference documents industry-standard performance engineering best practices for Apache JMeter test plan design, headless non-GUI execution, and resource optimization.

---

### 1. Headless CLI (Non-GUI) Execution

**Rule:** Never run performance, stress, or spike tests from the JMeter graphical user interface (GUI). The GUI is intended solely for test creation, debugging, and initial validation.

```bash
# Standard Non-GUI execution command
jmeter -n \
  -t <test_plan>.jmx \
  -l <execution_log>.jtl \
  -e -o <html_report_dir>/ \
  -JBASE_URL=localhost \
  -JPORT=3000
```

#### CLI Flag Definitions:
* `-n`: Specifies headless Non-GUI mode.
* `-t`: Path to source JMX test plan.
* `-l`: Path to output raw JTL log file.
* `-e`: Generates HTML dashboard report upon test completion.
* `-o`: Destination directory for HTML report dashboard (must be empty or deleted prior to run).
* `-J<prop>=<value>`: Passes global runtime properties dynamically without modifying JMX files.

---

### 2. JVM Heap and Garbage Collection Tuning

Default JMeter heap configurations (`-Xms1g -Xmx1g`) are frequently inadequate for high-concurrency workloads.

#### Recommended JVM Environment Variables:
```bash
export HEAP="-Xms2g -Xmx4g -XX:MaxMetaspaceSize=512m"
export JVM_ARGS="-XX:+UseG1GC -XX:InitiatingHeapOccupancyPercent=45 -XX:G1ReservePercent=15"
```
* **G1GC:** Minimizes Stop-the-World pauses during high sample throughput.
* **Heap Sizing:** Set initial (`-Xms`) and maximum (`-Xmx`) to identical or balanced values to prevent dynamic memory allocation overhead.

---

### 3. Listener Pruning & Overhead Minimization

* **Disable Heavy Listeners:** Listeners such as `View Results Tree`, `View Results in Table`, or `Graph Results` consume substantial heap memory by buffering raw response payloads.
* **Keep Listeners Disabled in JMX:** Ensure `enabled="false"` or delete debug listeners prior to executing headless runs.
* **Minimal Logging (`jmeter.properties`):**
  ```properties
  jmeter.save.saveservice.output_format=csv
  jmeter.save.saveservice.response_data=false
  jmeter.save.saveservice.samplerData=false
  jmeter.save.saveservice.requestHeaders=false
  jmeter.save.saveservice.url=true
  jmeter.save.saveservice.connect_time=true
  ```

---

### 4. Correlation and Dynamic Token Extraction

* **JSON Extractor:** Preferred for modern REST APIs returning JSON payloads.
  * *JSON Path Expressions:* `$.token`, `$.id`, `$.data.orderId`.
  * *Match No.:* `1` (first match), `0` (random match), `-1` (all matches).
  * *Default Value:* Always provide an explicit default value (e.g., `NOT_FOUND`) to simplify assertion checks.
* **Boundary Extractor / Regex Extractor:** Use for HTML or plain-text legacy responses where JSON parsing is inapplicable.

---

### 5. Workload Pacing & Think Time

* **Prevent Harmonic Hammer Effect:** Sending requests without timers creates an artificial, bursty workload that hammers web servers unnaturally.
* **Gaussian Random Timer:**
  * Simulates natural human cognitive hesitation.
  * Recommended parameters: Constant Delay Offset = $1,500\text{ ms}$, Deviations = $500\text{ ms}$ (Gaussian distribution centered at 1.5s with 68% between 1.0s and 2.0s).
* **Flow Control Action (Pacing):** Use Pacing / Constant Throughput Timers when modeling exact transactions-per-second (TPS) quotas.

---

### 6. Transaction Controllers

* **Generate Parent Sample:** Always enable `<boolProp name="TransactionController.parent">true</boolProp>`.
* **Rationale:** Merges internal redirects, authentication handshakes, and sub-requests into a unified, high-level business transaction. This enables clean, unambiguous SLA reporting without skewing sample counts.

---

### 7. Assertion Strategy

* **Two-Level Validation:**
  1. **Transport Layer:** HTTP Response Code assertion (`200`, `201`).
  2. **Business Layer:** Payload assertion (`{"success":true}`, `"status":"completed"`, or token presence).
* **Scope Assertions Carefully:** Apply assertions only to main samples (`Main sample only`) rather than child redirects to avoid false negatives.
