#!/usr/bin/env python3
"""
JMeter Performance Log (JTL) Analyzer
Part of the jmeter-performance-engineering Agent Skill.

Parses raw JMeter JTL logs (CSV or XML format), calculates exact statistical metrics
(Mean, Median, p90, p95, p99, Min, Max, TPS, Error Rate, Connect Time), detects
p95 regressions against baselines, and exports JSON/Markdown reports.
Zero external dependencies (uses standard library csv, math, json).
"""

import sys
import os
import csv
import math
import json
import argparse
from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict


def percentile(data: List[float], p: float) -> float:
    """Calculates percentile using standard nearest-rank / linear interpolation."""
    if not data:
        return 0.0
    sorted_data = sorted(data)
    n = len(sorted_data)
    if n == 1:
        return sorted_data[0]
    
    k = (n - 1) * (p / 100.0)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return sorted_data[int(k)]
    d0 = sorted_data[int(f)] * (c - k)
    d1 = sorted_data[int(c)] * (k - f)
    return round(d0 + d1, 2)


def std_dev(data: List[float], mean: float) -> float:
    """Calculates population standard deviation."""
    if len(data) <= 1:
        return 0.0
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    return round(math.sqrt(variance), 2)


class SampleRecord:
    __slots__ = ('timestamp', 'elapsed', 'label', 'response_code', 'success', 'bytes', 'connect_time')
    def __init__(self, timestamp: int, elapsed: float, label: str, response_code: str, success: bool, bytes_rcv: int, connect_time: float):
        self.timestamp = timestamp
        self.elapsed = elapsed
        self.label = label
        self.response_code = response_code
        self.success = success
        self.bytes = bytes_rcv
        self.connect_time = connect_time


class JtlParser:
    def __init__(self, file_path: str):
        self.file_path = os.path.abspath(file_path)

    def parse(self) -> List[SampleRecord]:
        if not os.path.isfile(self.file_path):
            raise FileNotFoundError(f"JTL log file not found: {self.file_path}")

        records = []
        with open(self.file_path, mode='r', encoding='utf-8', errors='replace') as f:
            first_line = f.readline().strip()
            if not first_line:
                return []

            if first_line.startswith("<?xml") or "<testResults" in first_line:
                f.seek(0)
                records = self._parse_xml(f)
            else:
                f.seek(0)
                records = self._parse_csv(f)

        return records

    def _parse_csv(self, f) -> List[SampleRecord]:
        reader = csv.DictReader(f)
        records = []
        for row in reader:
            try:
                ts = int(row.get('timeStamp', 0))
                elapsed = float(row.get('elapsed', 0.0))
                label = row.get('label', 'Unknown')
                code = row.get('responseCode', '200')
                success_val = row.get('success', 'true').lower()
                success = success_val in ('true', '1')
                bytes_rcv = int(row.get('bytes', 0))
                connect = float(row.get('Connect', 0.0))
                records.append(SampleRecord(ts, elapsed, label, code, success, bytes_rcv, connect))
            except (ValueError, KeyError):
                continue
        return records

    def _parse_xml(self, f) -> List[SampleRecord]:
        import xml.etree.ElementTree as ET
        records = []
        tree = ET.parse(f)
        root = tree.getroot()
        for elem in root.findall(".//*"):
            if elem.tag in ('httpSample', 'sample'):
                try:
                    ts = int(elem.attrib.get('tStamp', elem.attrib.get('ts', 0)))
                    elapsed = float(elem.attrib.get('t', 0.0))
                    label = elem.attrib.get('lb', 'Unknown')
                    code = elem.attrib.get('rc', '200')
                    success = elem.attrib.get('s', 'true').lower() == 'true'
                    bytes_rcv = int(elem.attrib.get('by', 0))
                    connect = float(elem.attrib.get('ct', 0.0))
                    records.append(SampleRecord(ts, elapsed, label, code, success, bytes_rcv, connect))
                except (ValueError, KeyError):
                    continue
        return records


class MetricCalculator:
    @staticmethod
    def compute_group_metrics(records: List[SampleRecord], group_name: str) -> Dict[str, Any]:
        if not records:
            return {}

        total_samples = len(records)
        successful_samples = sum(1 for r in records if r.success)
        failed_samples = total_samples - successful_samples
        error_rate = round((failed_samples / total_samples) * 100.0, 2)

        elapsed_times = [r.elapsed for r in records]
        connect_times = [r.connect_time for r in records]
        bytes_total = sum(r.bytes for r in records)

        min_time = round(min(elapsed_times), 2)
        max_time = round(max(elapsed_times), 2)
        mean_time = round(sum(elapsed_times) / total_samples, 2)
        median_time = percentile(elapsed_times, 50.0)
        p90_time = percentile(elapsed_times, 90.0)
        p95_time = percentile(elapsed_times, 95.0)
        p99_time = percentile(elapsed_times, 99.0)
        sd = std_dev(elapsed_times, mean_time)

        min_ts = min(r.timestamp for r in records)
        max_ts = max(r.timestamp for r in records)
        duration_s = max((max_ts - min_ts) / 1000.0, 0.001)
        throughput = round(total_samples / duration_s, 2)
        kb_per_s = round((bytes_total / 1024.0) / duration_s, 2)

        mean_connect = round(sum(connect_times) / total_samples, 2)
        p95_connect = percentile(connect_times, 95.0)

        return {
            "label": group_name,
            "total_samples": total_samples,
            "successful_samples": successful_samples,
            "failed_samples": failed_samples,
            "error_rate_pct": error_rate,
            "average_ms": mean_time,
            "median_ms": median_time,
            "p90_ms": p90_time,
            "p95_ms": p95_time,
            "p99_ms": p99_time,
            "min_ms": min_time,
            "max_ms": max_time,
            "std_dev": sd,
            "throughput_tps": throughput,
            "duration_seconds": round(duration_s, 2),
            "kb_per_second": kb_per_s,
            "connect_avg_ms": mean_connect,
            "connect_p95_ms": p95_connect
        }

    @classmethod
    def analyze_all(cls, records: List[SampleRecord]) -> Dict[str, Any]:
        if not records:
            return {"total_samples": 0}

        overall = cls.compute_group_metrics(records, "Total / Overall")

        by_label = defaultdict(list)
        for r in records:
            by_label[r.label].append(r)

        label_metrics = []
        for label, group_records in by_label.items():
            label_metrics.append(cls.compute_group_metrics(group_records, label))

        label_metrics.sort(key=lambda x: x["label"])

        return {
            "overall": overall,
            "labels": label_metrics
        }


def compare_jtl(baseline_metrics: Dict[str, Any], current_metrics: Dict[str, Any], p95_pct_thresh: float = 20.0, p95_abs_thresh: float = 15.0) -> Dict[str, Any]:
    """Compares current run against baseline and detects p95 regressions."""
    base_overall = baseline_metrics.get("overall", {})
    curr_overall = current_metrics.get("overall", {})

    b_p95 = base_overall.get("p95_ms", 0.0)
    c_p95 = curr_overall.get("p95_ms", 0.0)
    delta_p95 = round(c_p95 - b_p95, 2)
    delta_p95_pct = round(((c_p95 - b_p95) / max(b_p95, 0.001)) * 100.0, 2) if b_p95 > 0 else 0.0

    b_tps = base_overall.get("throughput_tps", 0.0)
    c_tps = curr_overall.get("throughput_tps", 0.0)
    delta_tps_pct = round(((c_tps - b_tps) / max(b_tps, 0.001)) * 100.0, 2) if b_tps > 0 else 0.0

    b_err = base_overall.get("error_rate_pct", 0.0)
    c_err = curr_overall.get("error_rate_pct", 0.0)

    is_regression = (delta_p95_pct >= p95_pct_thresh) and (delta_p95 >= p95_abs_thresh)

    return {
        "is_regression": is_regression,
        "delta_p95_ms": delta_p95,
        "delta_p95_pct": delta_p95_pct,
        "delta_tps_pct": delta_tps_pct,
        "baseline_p95": b_p95,
        "current_p95": c_p95,
        "baseline_tps": b_tps,
        "current_tps": c_tps,
        "baseline_err": b_err,
        "current_err": c_err
    }


def format_markdown(analysis: Dict[str, Any], title: str = "Performance Log Analysis") -> str:
    ov = analysis["overall"]
    md = []
    md.append(f"# {title}")
    md.append(f"\n**Total Samples:** {ov['total_samples']:,} | **Success:** {ov['successful_samples']:,} | **Errors:** {ov['failed_samples']} ({ov['error_rate_pct']}%)")
    md.append(f"**Throughput:** {ov['throughput_tps']:.2f} req/s | **Duration:** {ov['duration_seconds']:.2f}s | **Data Rate:** {ov['kb_per_second']:.2f} KB/s\n")

    md.append("## 1. Overall Key Percentiles (Milliseconds)")
    md.append("| Metric | Average | Median (p50) | p90 | p95 | p99 | Min | Max | Std Dev | Connect (p95) |")
    md.append("| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |")
    md.append(f"| **Overall Value** | **{ov['average_ms']:.2f}** | **{ov['median_ms']:.2f}** | **{ov['p90_ms']:.2f}** | **{ov['p95_ms']:.2f}** | **{ov['p99_ms']:.2f}** | {ov['min_ms']:.2f} | {ov['max_ms']:.2f} | {ov['std_dev']:.2f} | {ov['connect_p95_ms']:.2f} |\n")

    md.append("## 2. Per-Endpoint / Transaction Breakdown")
    md.append("| Label | Samples | Errors | Error % | Avg (ms) | Median | p95 (ms) | p99 (ms) | Max (ms) | TPS |")
    md.append("| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |")
    for item in analysis["labels"]:
        md.append(f"| `{item['label']}` | {item['total_samples']:,} | {item['failed_samples']} | {item['error_rate_pct']:.2f}% | {item['average_ms']:.2f} | {item['median_ms']:.2f} | {item['p95_ms']:.2f} | {item['p99_ms']:.2f} | {item['max_ms']:.2f} | {item['throughput_tps']:.2f} |")
    
    return "\n".join(md)


def main():
    parser = argparse.ArgumentParser(description="Analyze JMeter JTL log files and calculate empirical performance metrics.")
    parser.add_argument("--jtl", required=True, help="Path to raw JTL file (CSV or XML).")
    parser.add_argument("--compare", default=None, help="Optional path to baseline JTL file for regression comparison.")
    parser.add_argument("--json", default=None, help="Output path to export results as JSON.")
    parser.add_argument("--markdown", default=None, help="Output path to export results as Markdown.")
    args = parser.parse_args()

    parser_obj = JtlParser(args.jtl)
    records = parser_obj.parse()

    if not records:
        print(f"[!] Warning: No sample records found in {args.jtl}")
        sys.exit(1)

    analysis = MetricCalculator.analyze_all(records)
    ov = analysis["overall"]

    print("=" * 80)
    print(f" JMeter Performance Metrics Summary: {os.path.basename(args.jtl)}")
    print("=" * 80)
    print(f"Total Samples   : {ov['total_samples']:,}")
    print(f"Success Samples : {ov['successful_samples']:,}")
    print(f"Failed Samples  : {ov['failed_samples']} (Error Rate: {ov['error_rate_pct']}%)")
    print(f"Test Duration   : {ov['duration_seconds']:.2f} seconds")
    print(f"Throughput      : {ov['throughput_tps']:.2f} req/s (or TPS)")
    print(f"Bandwidth       : {ov['kb_per_second']:.2f} KB/s")
    print("-" * 80)
    print(f"Response Times  : Avg: {ov['average_ms']}ms | Median: {ov['median_ms']}ms | p90: {ov['p90_ms']}ms")
    print(f"Latency Gates   : p95: {ov['p95_ms']}ms | p99: {ov['p99_ms']}ms | Max: {ov['max_ms']}ms")
    print(f"Connect Time    : Avg: {ov['connect_avg_ms']}ms | p95: {ov['connect_p95_ms']}ms")
    print("=" * 80)

    if args.compare:
        base_parser = JtlParser(args.compare)
        base_records = base_parser.parse()
        base_analysis = MetricCalculator.analyze_all(base_records)
        diff = compare_jtl(base_analysis, analysis)

        print("\n" + "=" * 80)
        print(f" Regression Analysis vs Baseline: {os.path.basename(args.compare)}")
        print("=" * 80)
        print(f"Baseline p95 : {diff['baseline_p95']:.2f} ms  --> Current p95 : {diff['current_p95']:.2f} ms")
        print(f"Delta p95    : {diff['delta_p95_ms']:+.2f} ms ({diff['delta_p95_pct']:+.2f}%)")
        print(f"Baseline TPS : {diff['baseline_tps']:.2f} req/s --> Current TPS : {diff['current_tps']:.2f} req/s ({diff['delta_tps_pct']:+.2f}%)")
        print(f"Error Rate   : Baseline: {diff['baseline_err']}% --> Current: {diff['current_err']}%")
        if diff["is_regression"]:
            print("\n[!] CRITICAL ALERT: p95 Performance Regression Detected! (exceeds +20% and +15ms threshold)")
        else:
            print("\n[+] SUCCESS: No significant p95 regression detected within normal variance.")
        print("=" * 80)

        analysis["regression_comparison"] = diff

    if args.json:
        with open(args.json, "w", encoding="utf-8") as jf:
            json.dump(analysis, jf, indent=2)
        print(f"\n[+] Exported JSON metrics to: {args.json}")

    if args.markdown:
        md_content = format_markdown(analysis, title=f"Performance Analysis: {os.path.basename(args.jtl)}")
        with open(args.markdown, "w", encoding="utf-8") as mf:
            mf.write(md_content)
        print(f"[+] Exported Markdown report to: {args.markdown}")


if __name__ == "__main__":
    main()
