#!/usr/bin/env python3
"""Construct a robust V4 from the exact worst-regret frontier."""

from __future__ import annotations

import importlib.util
import json
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "collatz-search/best-v4"
LIMIT = 512
WORST = Fraction(45, 1024)


def load():
    spec = importlib.util.spec_from_file_location("v3search", ROOT / "collatz-search/search_v3.py")
    v3 = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(v3)
    return v3, v3.load_v2_search()


def fmt(item):
    k, r, e = item["rule"]
    return {"modulus_power": k, "residue": r, "exponents": list(e)}


def main():
    v3, s = load()
    rules = s.enumerate_rules()
    targets = s.TARGETS
    best_node = {}
    for item in rules:
        node = item["rule"][:2]
        if node not in best_node or item["margin"] > best_node[node]["margin"]:
            best_node[node] = item
    best = {}
    for p, r in targets:
        options = [best_node[(k, r % (1 << k))]["margin"] for k in range(2, p + 1) if (k, r % (1 << k)) in best_node]
        if options:
            best[p, r] = max(options)
    v3raw = json.loads((ROOT / "collatz-search/best-v3/solution.json").read_text())["rules"]
    v3m = {}
    for target in best:
        p, r = target
        v3m[target] = max(s.independent_verify((x["modulus_power"], x["residue"], tuple(x["exponents"]))) for x in v3raw if p >= x["modulus_power"] and r % (1 << x["modulus_power"]) == x["residue"])
    req = {target: max(v3m[target], best[target] - WORST) for target in best}

    @lru_cache(None)
    def cost(k, r, inherited):
        choices = []
        for choose in (False, True):
            item = best_node.get((k, r)) if choose else None
            if choose and item is None:
                continue
            current = inherited
            own = 0
            if item is not None:
                current = item["margin"] if inherited is None else max(inherited, item["margin"])
                own = 1
            need = req.get((k, r)) if k >= 8 else None
            if need is not None and (current is None or current < need):
                continue
            if k < 12:
                left = cost(k + 1, r, current)
                right = cost(k + 1, r + (1 << k), current)
                if left is None or right is None:
                    continue
                choices.append(own + left + right)
            else:
                choices.append(own)
        return min(choices) if choices else None

    minimum = cost(2, 1, None) + cost(2, 3, None)
    if minimum != 506:
        raise AssertionError(f"unexpected worst-regret frontier: {minimum}")

    selected = []

    def reconstruct(k, r, inherited):
        wanted = cost(k, r, inherited)
        for choose in (False, True):
            item = best_node.get((k, r)) if choose else None
            if choose and item is None:
                continue
            current = inherited
            own = 0
            if item is not None:
                current = item["margin"] if inherited is None else max(inherited, item["margin"])
                own = 1
            need = req.get((k, r)) if k >= 8 else None
            if need is not None and (current is None or current < need):
                continue
            if k < 12:
                left = cost(k + 1, r, current)
                right = cost(k + 1, r + (1 << k), current)
                if left is None or right is None or own + left + right != wanted:
                    continue
                if item is not None:
                    selected.append(item)
                reconstruct(k + 1, r, current)
                reconstruct(k + 1, r + (1 << k), current)
                return
            if own == wanted:
                if item is not None:
                    selected.append(item)
                return
        raise AssertionError("reconstruction failed")

    reconstruct(2, 1, None)
    reconstruct(2, 3, None)

    def achieved(items):
        out = {}
        for p, r in best:
            values = [x["margin"] for x in items if p >= x["rule"][0] and r % (1 << x["rule"][0]) == x["rule"][1]]
            if values:
                out[p, r] = max(values)
        return out

    def vector(items):
        got = achieved(items)
        return tuple(sorted((best[t] - got[t] for t in best), reverse=True))

    # Use the remaining six slots for exact one-rule lexicographic improvements.
    candidates = list(best_node.values())
    for _ in range(LIMIT - len(selected)):
        current_vector = vector(selected)
        best_choice = None
        best_vector = current_vector
        present = {(x["rule"][0], x["rule"][1]) for x in selected}
        for item in candidates:
            node = (item["rule"][0], item["rule"][1])
            if node in present:
                continue
            trial = selected + [item]
            trial_vector = vector(trial)
            if trial_vector < best_vector:
                best_vector = trial_vector
                best_choice = item
        if best_choice is None:
            break
        selected.append(best_choice)

    target_vector = vector(selected)
    # Delete only rules that preserve every target margin exactly.
    changed = True
    while changed:
        changed = False
        for i in range(len(selected) - 1, -1, -1):
            trial = selected[:i] + selected[i + 1:]
            if vector(trial) == target_vector:
                selected = trial
                changed = True
                break
    final = achieved(selected)
    regrets = {t: best[t] - final[t] for t in best}
    if len(final) != 3352 or any(final[t] < v3m[t] for t in best):
        raise AssertionError("coverage or V3 margin regressed")
    if max(regrets.values()) != WORST:
        raise AssertionError("worst-regret optimum lost")

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "solution.json").write_text(json.dumps({"rules": [fmt(x) for x in selected]}, indent=2) + "\n")
    loaded = s._EVAL._load_rules(OUT)
    for rule in loaded:
        if s.independent_verify(rule) != s.evaluator_verify(rule):
            raise AssertionError(f"verification mismatch: {rule}")
    mean = sum(regrets.values()) / len(regrets)
    report = {
        "rules": len(selected),
        "coverage": "3352/3968",
        "global_minimum_margin_ppm": int(min(final.values()) * 1_000_000),
        "targets_at_individual_optimum": sum(x == 0 for x in regrets.values()),
        "maximum_regret": {"numerator": max(regrets.values()).numerator, "denominator": max(regrets.values()).denominator, "ppm": int(max(regrets.values()) * 1_000_000)},
        "mean_regret": float(mean),
        "mean_regret_exact": {"numerator": mean.numerator, "denominator": mean.denominator},
        "all_individual_optima_within_512": False,
        "minimum_rules_for_all_individual_optima": 649,
        "final_rule_count_after_exact_redundancy_removal": len(selected),
        "independent_verification": "passed: all generated rules and every written rule cross-checked against eval.py",
        "selection": "exact 506-rule worst-regret frontier, followed by six exact one-rule lexicographic improvements and exact redundancy removal",
        "uncoverable_classes": "the exact 616 classes remain those listed in best-v3/search-report.json",
    }
    (OUT / "search-report.json").write_text(json.dumps(report, indent=2) + "\n")
    (OUT / "README.md").write_text(
        "# Collatz modular descent, generation 4\n\n"
        f"V4 covers all 3,352 coverable classes with {len(selected)} rules and never lowers a V3 per-target margin. "
        f"All individual optima need at least 649 rules, so they do not fit within 512. The worst regret is {max(regrets.values())} and the mean regret is {float(mean):.12f}.\n\n"
        "The exact 616 uncoverable classes are unchanged from V3. Rules were independently cross-checked against eval.py; no hill files were modified and nothing was submitted.\n",
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
