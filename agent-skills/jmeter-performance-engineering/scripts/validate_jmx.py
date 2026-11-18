#!/usr/bin/env python3
"""
JMeter Test Plan (JMX) Validator
Part of the jmeter-performance-engineering Agent Skill.

Validates XML well-formedness, structural completeness, parameterization,
assertion coverage, extractors, timers, and best practice compliance for any JMeter Test Plan.
Zero external dependencies (uses standard library xml.etree.ElementTree).
"""

import sys
import os
import argparse
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Tuple

class JmxValidator:
    def __init__(self, jmx_path: str, csv_dir: str = None, verbose: bool = False):
        self.jmx_path = os.path.abspath(jmx_path)
        self.csv_dir = os.path.abspath(csv_dir) if csv_dir else os.path.dirname(self.jmx_path)
        self.verbose = verbose
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []
        self.tree = None
        self.root = None

    def validate(self) -> Tuple[bool, List[str], List[str], List[str]]:
        """Executes all validation phases."""
        if not os.path.isfile(self.jmx_path):
            self.errors.append(f"File not found: {self.jmx_path}")
            return False, self.errors, self.warnings, self.info

        # Phase 1: XML Well-formedness
        try:
            self.tree = ET.parse(self.jmx_path)
            self.root = self.tree.getroot()
            self.info.append("XML syntax is well-formed.")
        except ET.ParseError as e:
            self.errors.append(f"XML Parse Error: {e}")
            return False, self.errors, self.warnings, self.info
        except Exception as e:
            self.errors.append(f"Unexpected error reading file: {e}")
            return False, self.errors, self.warnings, self.info

        # Phase 2: Root element check
        if self.root.tag != "jmeterTestPlan":
            self.errors.append(f"Root tag is <{self.root.tag}>, expected <jmeterTestPlan>.")
        else:
            version = self.root.attrib.get("version", "unknown")
            properties = self.root.attrib.get("properties", "unknown")
            self.info.append(f"JMeter Test Plan detected (version: {version}, properties: {properties}).")

        # Phase 3: Structural Elements Check
        self._check_test_plan()
        self._check_thread_groups()
        self._check_http_defaults()
        self._check_csv_data_sets()
        self._check_samplers()
        self._check_extractors()
        self._check_assertions()
        self._check_timers()
        self._check_listeners()

        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings, self.info

    def _check_test_plan(self):
        test_plans = self.root.findall(".//TestPlan")
        if not test_plans:
            self.errors.append("No <TestPlan> element found in JMX.")
        else:
            self.info.append(f"Found {len(test_plans)} TestPlan root element(s).")

    def _check_thread_groups(self):
        thread_groups = self.root.findall(".//ThreadGroup")
        custom_tg = self.root.findall(".//com.blazemeter.jmeter.threads.concurrency.ConcurrencyThreadGroup")
        all_tgs = thread_groups + custom_tg

        if not all_tgs:
            self.errors.append("No ThreadGroup found. Test plan cannot execute without virtual users.")
            return

        self.info.append(f"Found {len(all_tgs)} Thread Group(s).")
        for idx, tg in enumerate(all_tgs):
            name = tg.attrib.get("testname", f"ThreadGroup_{idx+1}")
            enabled = tg.attrib.get("enabled", "true")
            
            num_threads = None
            ramp_time = None
            duration = None
            
            for string_prop in tg.findall(".//stringProp"):
                pname = string_prop.attrib.get("name")
                if pname == "ThreadGroup.num_threads":
                    num_threads = string_prop.text
                elif pname == "ThreadGroup.ramp_time":
                    ramp_time = string_prop.text
                elif pname == "ThreadGroup.duration":
                    duration = string_prop.text

            self.info.append(f"  - [{name}] (enabled={enabled}): threads={num_threads}, ramp_up={ramp_time}s, duration={duration}s")

    def _check_http_defaults(self):
        defaults = self.root.findall(".//ConfigTestElement[@testclass='ConfigTestElement']")
        http_defaults = [d for d in defaults if d.attrib.get("guiclass") == "HttpDefaultsGui"]
        if not http_defaults:
            self.warnings.append("No HTTP Request Defaults found. Individual samplers must specify host/port.")
        else:
            self.info.append(f"Found {len(http_defaults)} HTTP Request Defaults element(s).")

    def _check_csv_data_sets(self):
        csv_configs = self.root.findall(".//CSVDataSet")
        if not csv_configs:
            self.warnings.append("No CSVDataSet config found. Test may not be parameterized for multi-user concurrency.")
            return

        self.info.append(f"Found {len(csv_configs)} CSV Data Set Config(s):")
        for idx, csv in enumerate(csv_configs):
            name = csv.attrib.get("testname", f"CSVDataSet_{idx+1}")
            filename = None
            variable_names = None
            
            for prop in csv.findall(".//stringProp"):
                pname = prop.attrib.get("name")
                if pname == "filename":
                    filename = prop.text
                elif pname == "variableNames":
                    variable_names = prop.text

            if not filename:
                self.errors.append(f"CSV Data Set [{name}] has an empty or missing 'filename' property.")
            else:
                possible_paths = [
                    os.path.join(self.csv_dir, filename),
                    os.path.join(os.path.dirname(self.jmx_path), filename),
                    filename
                ]
                exists = any(os.path.isfile(p) for p in possible_paths)
                if not exists:
                    self.warnings.append(f"CSV file '{filename}' specified in [{name}] was not found at searched paths.")
                else:
                    self.info.append(f"  - [{name}]: file='{filename}' (verified on disk), vars='{variable_names}'")

    def _check_samplers(self):
        samplers = self.root.findall(".//HTTPSamplerProxy")
        if not samplers:
            self.errors.append("No HTTPSamplerProxy found in test plan. No HTTP requests will be executed.")
            return

        self.info.append(f"Found {len(samplers)} HTTP Sampler(s).")
        for idx, sampler in enumerate(samplers):
            s_name = sampler.attrib.get("testname", f"Sampler_{idx+1}")
            method = "GET"
            path = "/"
            for sp in sampler.findall(".//stringProp"):
                if sp.attrib.get("name") == "HTTPSampler.method":
                    method = sp.text or "GET"
                elif sp.attrib.get("name") == "HTTPSampler.path":
                    path = sp.text or "/"
            if self.verbose:
                self.info.append(f"    Sampler #{idx+1}: [{method}] {path} ('{s_name}')")

    def _check_extractors(self):
        json_extractors = self.root.findall(".//JSONPostProcessor")
        regex_extractors = self.root.findall(".//RegexExtractor")
        total_extractors = len(json_extractors) + len(regex_extractors)

        if total_extractors == 0:
            self.warnings.append("No Post-Processors (JSON/Regex Extractors) found. Correlation or dynamic token passing may be missing.")
        else:
            self.info.append(f"Found {total_extractors} Extractor(s) ({len(json_extractors)} JSON, {len(regex_extractors)} Regex).")
            for je in json_extractors:
                ref_name = je.attrib.get("testname", "JSON Extractor")
                self.info.append(f"  - JSON Extractor: '{ref_name}'")

    def _check_assertions(self):
        response_assertions = self.root.findall(".//ResponseAssertion")
        json_assertions = self.root.findall(".//JSONPathAssertion")
        total_assertions = len(response_assertions) + len(json_assertions)

        if total_assertions == 0:
            self.warnings.append("No Assertions found. Test plan will only check HTTP transport layer without validating business payloads.")
        else:
            self.info.append(f"Found {total_assertions} Assertion(s) ({len(response_assertions)} Response, {len(json_assertions)} JSONPath).")

    def _check_timers(self):
        gaussian = self.root.findall(".//GaussianRandomTimer")
        uniform = self.root.findall(".//UniformRandomTimer")
        constant = self.root.findall(".//ConstantTimer")
        total_timers = len(gaussian) + len(uniform) + len(constant)

        if total_timers == 0:
            self.warnings.append("No Timers found. Virtual Users will hammer endpoints without realistic human think time.")
        else:
            self.info.append(f"Found {total_timers} Timer(s) for pacing/think time simulation.")

    def _check_listeners(self):
        result_collectors = self.root.findall(".//ResultCollector")
        self.info.append(f"Found {len(result_collectors)} Listener(s).")
        for listener in result_collectors:
            name = listener.attrib.get("testname", "Listener")
            guiclass = listener.attrib.get("guiclass", "")
            enabled = listener.attrib.get("enabled", "true")
            if "ViewResultsFullVisualizer" in guiclass and enabled.lower() == "true":
                self.warnings.append(f"Listener [{name}] (View Results Tree) is ENABLED. Disable it during load runs to avoid OutOfMemory errors.")


def print_report(jmx_path: str, is_valid: bool, errors: List[str], warnings: List[str], info: List[str], verbose: bool):
    print("=" * 70)
    print(f" JMeter Test Plan Validation Report")
    print(f" Target: {os.path.basename(jmx_path)}")
    print("=" * 70)

    if errors:
        print("\n[!] FATAL ERRORS (Must be resolved before execution):")
        for err in errors:
            print(f"  [-] {err}")

    if warnings:
        print("\n[?] WARNINGS & BEST PRACTICE ALERTS:")
        for warn in warnings:
            print(f"  [!] {warn}")

    if verbose or not errors:
        print("\n[*] STRUCTURAL AUDIT DETAILS:")
        for inf in info:
            print(f"  [+] {inf}")

    print("\n" + "-" * 70)
    status_str = "PASS (Valid JMeter Plan)" if is_valid else "FAIL (Invalid Configuration)"
    print(f" OVERALL STATUS: {status_str}")
    print("-" * 70 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Validate Apache JMeter JMX Test Plans.")
    parser.add_argument("--jmx", required=True, help="Path to .jmx file to validate.")
    parser.add_argument("--csv-dir", default=None, help="Directory to search for referenced CSV datasets.")
    parser.add_argument("--verbose", "-v", action="store_true", help="Display detailed structural elements.")
    args = parser.parse_args()

    validator = JmxValidator(jmx_path=args.jmx, csv_dir=args.csv_dir, verbose=args.verbose)
    is_valid, errors, warnings, info = validator.validate()
    print_report(args.jmx, is_valid, errors, warnings, info, args.verbose)

    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
