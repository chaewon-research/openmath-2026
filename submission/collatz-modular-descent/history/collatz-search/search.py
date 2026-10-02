#!/usr/bin/env python3
"""Exhaustively search the public Collatz hill's finite rule universe."""

from __future__ import annotations

import importlib.util
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HILL = ROOT / ".autolab/hills/collatz-modular-descent"
OUT = ROOT / "collatz-search/best-v2"
MAX_POWER = 12
MAX_STEPS = 24
TARGETS = [(p, r) for p in range(8, MAX_POWER + 1) for r in range(1, 1 << p, 2)]
TARGET_INDEX = {target: i for i, target in enumerate(TARGETS)}
_SPEC = importlib.util.spec_from_file_location("hill_eval", HILL / "eval.py")
_EVAL = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
_SPEC.loader.exec_module(_EVAL)


def v2(value: int) -> int:
    return (value & -value).bit_length() - 1


def independent_verify(rule: tuple[int, int, tuple[int, ...]]) -> Fraction:
    k, residue, exponents = rule
    if not (2 <= k <= 32 and 0 < residue < (1 << k) and residue & 1):
        raise AssertionError("bad rule domain")
    if not (1 <= len(exponents) <= MAX_STEPS):
        raise AssertionError("bad rule length")
    if k < 1 + sum(exponents):
        raise AssertionError("unstable rule")
    x = residue
    for exponent in exponents:
        observed = v2(3 * x + 1)
        if observed != exponent:
            raise AssertionError(f"valuation mismatch: {rule}")
        x = (3 * x + 1) >> exponent
    denominator = 1 << sum(exponents)
    numerator = 3 ** len(exponents)
    if numerator >= denominator or x >= residue:
        raise AssertionError(f"noncontractive rule: {rule}")
    return Fraction(denominator - numerator, denominator)


def evaluator_verify(rule: tuple[int, int, tuple[int, ...]]) -> Fraction:
    checked = _EVAL._verify_rule(rule)
    return checked["margin"]


def support(k: int, residue: int) -> int:
    bits = 0
    for p in range(max(8, k), MAX_POWER + 1):
        for target_residue in range(1, 1 << p, 2):
            if target_residue % (1 << k) == residue:
                bits |= 1 << TARGET_INDEX[(p, target_residue)]
    return bits


def enumerate_rules() -> list[dict]:
    rules: list[dict] = []
    for k in range(2, MAX_POWER + 1):
        for residue in range(1, 1 << k, 2):
            x = residue
            exponents: list[int] = []
            for _ in range(MAX_STEPS):
                exponent = v2(3 * x + 1)
                exponents.append(exponent)
                x = (3 * x + 1) >> exponent
                if k < 1 + sum(exponents):
                    break
                if 3 ** len(exponents) < 1 << sum(exponents) and x < residue:
                    rule = (k, residue, tuple(exponents))
                    margin = independent_verify(rule)
                    if margin != evaluator_verify(rule):
                        raise AssertionError(f"verifier disagreement: {rule}")
                    rules.append({
                        "rule": rule,
                        "margin": margin,
                        "support": support(k, residue),
                    })
                    # Later prefixes have the same residue support but cannot
                    # improve its contraction margin monotonically in general;
                    # continue enumerating all allowed prefixes.
    return rules


def reduce_same_support(rules: list[dict]) -> list[dict]:
    best: dict[int, dict] = {}
    for item in rules:
        old = best.get(item["support"])
        if old is None or (item["margin"], -item["rule"][0]) > (old["margin"], -old["rule"][0]):
            best[item["support"]] = item
    return list(best.values())


def dominated(item: dict, by_support: dict[tuple[int, int], dict]) -> bool:
    k, residue, _ = item["rule"]
    for ancestor_k in range(2, k):
        ancestor = by_support.get((ancestor_k, residue % (1 << ancestor_k)))
        if ancestor is not None and ancestor["margin"] >= item["margin"]:
            return True
    return False


def prune_dominated(rules: list[dict]) -> list[dict]:
    by_node = {(item["rule"][0], item["rule"][1]): item for item in rules}
    return [item for item in rules if not dominated(item, by_node)]


def best_at_margin(rules: list[dict], threshold: Fraction) -> tuple[int, list[dict]]:
    eligible = [item for item in rules if item["margin"] >= threshold]
    union = 0
    for item in eligible:
        union |= item["support"]
    # Supports are laminar.  The inclusion-maximal supports are a minimum
    # cardinality cover of this union: each maximal support has a target bit
    # that no disjoint maximal support can cover.
    maximal = []
    for item in eligible:
        if not any(item["support"] != other["support"] and item["support"] | other["support"] == other["support"] for other in eligible):
            maximal.append(item)
    unique = {item["support"]: item for item in maximal}
    return union.bit_count(), list(unique.values())


def fmt_rule(item: dict) -> dict:
    k, residue, exponents = item["rule"]
    return {"modulus_power": k, "residue": residue, "exponents": list(exponents)}


def baseline_stats() -> dict:
    path = ROOT / ".autolab/climb/attempt-1/solution.json"
    rules = json.loads(path.read_text(encoding="utf-8"))["rules"]
    bits = 0
    margins = []
    for item in rules:
        rule = (item["modulus_power"], item["residue"], tuple(item["exponents"]))
        margins.append(independent_verify(rule))
        bits |= support(rule[0], rule[1])
    return {"rules": len(rules), "coverage": bits.bit_count(), "minimum_margin": min(margins)}


def main() -> None:
    all_rules = enumerate_rules()
    same_support = reduce_same_support(all_rules)
    candidates = prune_dominated(same_support)
    max_union = 0
    for item in candidates:
        max_union |= item["support"]
    max_coverage = max_union.bit_count()

    thresholds = sorted({item["margin"] for item in candidates}, reverse=True)
    chosen_threshold = None
    chosen: list[dict] = []
    for threshold in thresholds:
        coverage, selection = best_at_margin(candidates, threshold)
        if coverage == max_coverage:
            chosen_threshold = threshold
            chosen = selection
            break
    assert chosen_threshold is not None
    if len(chosen) > 512:
        raise AssertionError(f"minimum cover exceeds rule limit: {len(chosen)}")
    if len(chosen) != len({item["support"] for item in chosen}):
        raise AssertionError("duplicate supports in selection")
    selected_union = 0
    for item in chosen:
        independent_verify(item["rule"])
        if independent_verify(item["rule"]) != evaluator_verify(item["rule"]):
            raise AssertionError("selected verifier disagreement")
        selected_union |= item["support"]
    if selected_union != max_union:
        raise AssertionError("selection does not attain maximum coverage")

    uncovered = [(p, r) for (p, r), bit in TARGET_INDEX.items() if not (max_union >> bit) & 1]
    baseline = baseline_stats()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "solution.json").write_text(json.dumps({"rules": [fmt_rule(item) for item in chosen]}, indent=2) + "\n", encoding="utf-8")
    report = {
        "enumerated_rules": len(all_rules),
        "same_support_rules": len(same_support),
        "undominated_rules": len(candidates),
        "selected_rules": len(chosen),
        "minimum_rule_count_at_selected_margin": len(chosen),
        "universe_size": len(TARGETS),
        "maximum_coverable": max_coverage,
        "coverage_fraction": f"{max_coverage}/{len(TARGETS)}",
        "full_universe_100_percent_coverable": max_coverage == len(TARGETS),
        "minimum_margin": {"numerator": chosen_threshold.numerator, "denominator": chosen_threshold.denominator, "ppm_floor": int(chosen_threshold * 1_000_000)},
        "baseline_22_rule_candidate": {
            "rules": baseline["rules"],
            "coverage": baseline["coverage"],
            "minimum_margin": {"numerator": baseline["minimum_margin"].numerator, "denominator": baseline["minimum_margin"].denominator, "ppm_floor": int(baseline["minimum_margin"] * 1_000_000)},
        },
        "delta_from_baseline": {"rules": len(chosen) - baseline["rules"], "coverage": max_coverage - baseline["coverage"], "minimum_margin_ppm": int(chosen_threshold * 1_000_000) - int(baseline["minimum_margin"] * 1_000_000)},
        "selection_method": "maximum union first; highest margin threshold retaining that union; inclusion-maximal laminar supports for minimum cardinality",
        "uncovered_classes": [
            {
                "modulus_power": p,
                "residue": r,
                "checked_rule_modulus_powers": list(range(2, p + 1)),
                "reason": "no valid stable contractive rule exists at any checked k; every possible rule at those prefixes fails exact valuation, stability, or strict contraction",
            }
            for p, r in uncovered
        ],
        "verification": "every enumerated rule was checked independently and against eval.py; selected rules were checked again",
    }
    (OUT / "search-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
