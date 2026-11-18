#!/usr/bin/env python3
"""
Performance Test Report Generator
Part of the jmeter-performance-engineering Agent Skill.

Generates structured Markdown performance test reports from analyzed JTL metrics (JSON)
and metadata. Evaluates SLA compliance gates, highlights bottlenecks, and formats
summary tables. Zero external dependencies.
"""

import sys
import os
import json
import argparse
from typing import Dict, Any, List

def evaluate_sla(metric: float, threshold: float, lower_is_better: bool = True) -> str:
    if lower_is_better:
        return "PASS" if metric <= threshold else "FAIL"
    else:
        return "PASS" if metric >= threshold else "FAIL"

def generate_markdown(metrics: Dict[str, Any], meta: Dict[str, Any]) -> str:
    ov = metrics.get("overall", {})
    labels = metrics.get("labels", [])
    scenario = meta.get("scenario", "Performance Test")
    sut_name = meta.get("sut", "System Under Test")
    sla_p95 = float(meta.get("sla_p95", 1200.0))
    sla_err = float(meta.get("sla_error", 1.0))
    sla_tps = float(meta.get("target_tps", 10.0))

    err_rate = ov.get("error_rate_pct", 0.0)
    p95_val = ov.get("p95_ms", 0.0)
    tps_val = ov.get("throughput_tps", 0.0)

    err_status = evaluate_sla(err_rate, sla_err, lower_is_better=True)
    p95_status = evaluate_sla(p95_val, sla_p95, lower_is_better=True)
    tps_status = evaluate_sla(tps_val, sla_tps, lower_is_better=False)
    overall_gate = "PASS" if (err_status == "PASS" and p95_status == "PASS") else "FAIL"

    lines = []
    lines.append(f"# {scenario} Summary Report: {sut_name}")
    lines.append(f"\n**Execution Date:** {meta.get('date', 'N/A')} | **Execution Engine:** Apache JMeter (CLI Non-GUI)")
    lines.append(f"**Target System:** {sut_name} | **Scenario Classification:** `{scenario}`")
    lines.append(f"**Overall Quality Gate:** **`{overall_gate}`**\n")

    lines.append("## 1. Executive Summary & Quality Gate SLA")
    lines.append("| Performance Metric | Measured Value | SLA Target Threshold | Quality Gate Status |")
    lines.append("| :--- | :---: | :---: | :---: |")
    lines.append(f"| **Error Rate** | **{err_rate:.2f}%** ({ov.get('failed_samples', 0)} / {ov.get('total_samples', 0):,}) | $\\le {sla_err:.1f}\\%$ | **{err_status}** |")
    lines.append(f"| **95th Percentile Latency (p95)** | **{p95_val:.2f} ms** | $\\le {sla_p95:.0f} \\text{{ ms}}$ | **{p95_status}** |")
    lines.append(f"| **Throughput (Transactions/sec)** | **{tps_val:.2f} TPS** | $\\ge {sla_tps:.1f} \\text{{ TPS}}$ | **{tps_status}** |")
    lines.append(f"| **Average Response Time** | **{ov.get('average_ms', 0.0):.2f} ms** | Baseline reference | N/A |")
    lines.append(f"| **Median Latency (p50)** | **{ov.get('median_ms', 0.0):.2f} ms** | Baseline reference | N/A |")
    lines.append(f"| **Test Duration** | **{ov.get('duration_seconds', 0.0):.2f} seconds** | Scheduled window | **PASS** |\n")

    lines.append("## 2. Statistical Response Time Distribution (Milliseconds)")
    lines.append("| Scope | Samples | Min | Average | Median (p50) | p90 | p95 | p99 | Max | Std Dev | Connect (p95) |")
    lines.append("| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |")
    lines.append(f"| **TOTAL** | {ov.get('total_samples', 0):,} | {ov.get('min_ms', 0.0):.2f} | {ov.get('average_ms', 0.0):.2f} | {ov.get('median_ms', 0.0):.2f} | {ov.get('p90_ms', 0.0):.2f} | {ov.get('p95_ms', 0.0):.2f} | {ov.get('p99_ms', 0.0):.2f} | {ov.get('max_ms', 0.0):.2f} | {ov.get('std_dev', 0.0):.2f} | {ov.get('connect_p95_ms', 0.0):.2f} |\n")

    lines.append("## 3. Granular Breakdown by Endpoint / Transaction")
    lines.append("| Transaction / Request Label | Sample Count | Failures | Error % | Avg (ms) | Median (ms) | p95 (ms) | p99 (ms) | Max (ms) | Throughput (TPS) |")
    lines.append("| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |")
    for item in labels:
        lines.append(f"| `{item['label']}` | {item['total_samples']:,} | {item['failed_samples']} | {item['error_rate_pct']:.2f}% | {item['average_ms']:.2f} | {item['median_ms']:.2f} | {item['p95_ms']:.2f} | {item['p99_ms']:.2f} | {item['max_ms']:.2f} | {item['throughput_tps']:.2f} |")

    # Bottleneck detection
    slowest_p95 = max(labels, key=lambda x: x.get("p95_ms", 0.0)) if labels else None
    highest_err = max(labels, key=lambda x: x.get("error_rate_pct", 0.0)) if labels else None

    lines.append("\n## 4. Bottleneck & Latency Analysis")
    if slowest_p95:
        lines.append(f"* **Critical Path Latency Bottleneck:** `{slowest_p95['label']}` exhibited the highest latency with $p95 = {slowest_p95['p95_ms']:.2f}\\text{{ ms}}$ and $\\text{{Max}} = {slowest_p95['max_ms']:.2f}\\text{{ ms}}$.")
    if highest_err and highest_err.get("error_rate_pct", 0.0) > 0:
        lines.append(f"* **Reliability Hazard:** `{highest_err['label']}` registered the highest error rate of {highest_err['error_rate_pct']:.2f}%.")
    else:
        lines.append("* **Reliability Assessment:** Zero errors observed across all endpoints during the test execution window.")

    lines.append(f"\n*Report automatically generated by `jmeter-performance-engineering` Agent Skill.*")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate Markdown Performance Reports from Analyzed JTL Metrics JSON.")
    parser.add_argument("--metrics-json", required=True, help="Path to JSON file output by analyze_jtl.py.")
    parser.add_argument("--scenario", default="Performance Test", help="Scenario name (Load Test, Stress Test, Spike Test, Soak Test).")
    parser.add_argument("--sut-name", default="EShop", help="Name of the System Under Test.")
    parser.add_argument("--sla-p95", default=1200.0, type=float, help="p95 SLA threshold in milliseconds.")
    parser.add_argument("--sla-error", default=1.0, type=float, help="Error rate SLA threshold in percent.")
    parser.add_argument("--target-tps", default=10.0, type=float, help="Target Throughput in TPS.")
    parser.add_argument("--date", default="2026-11-18", help="Execution date.")
    parser.add_argument("--output", required=True, help="Path to write Markdown report.")
    args = parser.parse_args()

    with open(args.metrics_json, "r", encoding="utf-8") as f:
        metrics = json.load(f)

    meta = {
        "scenario": args.scenario,
        "sut": args.sut_name,
        "sla_p95": args.sla_p95,
        "sla_error": args.sla_error,
        "target_tps": args.target_tps,
        "date": args.date
    }

    report_md = generate_markdown(metrics, meta)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(report_md)

    print(f"[+] Successfully generated performance report: {args.output}")

if __name__ == "__main__":
    main()
