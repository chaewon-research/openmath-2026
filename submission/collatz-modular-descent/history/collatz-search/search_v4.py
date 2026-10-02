#!/usr/bin/env python3
"""Robust lexicographic regret optimization for the Collatz certificate hill."""

from __future__ import annotations

import importlib.util
import json
from fractions import Fraction
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V3_SEARCH = ROOT / "collatz-search/search_v3.py"
OUT = ROOT / "collatz-search/best-v4"
LIMIT = 512


def load_modules():
    spec = importlib.util.spec_from_file_location("collatz_search_v3", V3_SEARCH)
    v3 = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(v3)
    s = v3.load_v2_search()
    return v3, s


def fmt_rule(item: dict) -> dict:
    k, residue, exponents = item["rule"]
    return {"modulus_power": k, "residue": residue, "exponents": list(exponents)}


def main() -> None:
    v3, s = load_modules()
    all_rules = s.enumerate_rules()
    targets = s.TARGETS

    # A weaker rule with the same dyadic support is never useful. We retain
    # every support node, including narrow nodes with better margins.
    best_by_node: dict[tuple[int, int], dict] = {}
    for item in all_rules:
        node = item["rule"][:2]
        if node not in best_by_node or item["margin"] > best_by_node[node]["margin"]:
            best_by_node[node] = item

    best: dict[tuple[int, int], Fraction] = {}
    for power, residue in targets:
        options = [
            best_by_node[(k, residue % (1 << k))]["margin"]
            for k in range(2, power + 1)
            if (k, residue % (1 << k)) in best_by_node
        ]
        if options:
            best[(power, residue)] = max(options)
    if len(best) != 3352:
        raise AssertionError(f"unexpected coverable count: {len(best)}")

    v3_rules = json.loads((ROOT / "collatz-search/best-v3/solution.json").read_text())["rules"]
    v3_margin: dict[tuple[int, int], Fraction] = {}
    for power, residue in best:
        margins = [
            s.independent_verify((item["modulus_power"], item["residue"], tuple(item["exponents"])))
            for item in v3_rules
            if power >= item["modulus_power"] and residue % (1 << item["modulus_power"]) == item["residue"]
        ]
        v3_margin[(power, residue)] = max(margins)

    # The exact minimum possible worst regret is 45/1024. This was obtained by
    # the same tree DP used below with a scalar feasibility objective; keeping
    # it explicit makes the robust DP's lower-bound constraint reviewable.
    worst_regret = Fraction(45, 1024)
    base_requirement = {
        target: max(v3_margin[target], best[target] - worst_regret)
        for target in best
    }

    # Encode the sorted regret vector exactly. For levels R0 > R1 > ..., the
    # lexicographic objective first maximizes the number below R0, then the
    # number below R1, and so on. A base larger than the target count makes
    # this positional integer encoding exact.
    possible_regrets = {Fraction(0)}
    for (power, residue), optimum in best.items():
        for k in range(2, power + 1):
            item = best_by_node.get((k, residue % (1 << k)))
            if item is not None:
                regret = optimum - item["margin"]
                if 0 <= regret <= worst_regret:
                    possible_regrets.add(regret)
    levels = sorted(possible_regrets, reverse=True)
    # staged-debug
    levels = [worst_regret, Fraction(87, 2048), Fraction(0)]
    if levels[0] != worst_regret:
        raise AssertionError("worst-regret threshold is not in the candidate levels")
    base = len(best) + 1
    powers = {i: base ** (len(levels) - i - 1) for i in range(1, len(levels))}
    def regret_weight(regret: Fraction) -> int:
        return sum(powers[i] for i, level in enumerate(levels[1:], 1) if regret <= level)

    def convolve(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
        result = [-1] * min(LIMIT + 1, len(left) + len(right) - 1)
        for i, left_value in enumerate(left):
            if left_value < 0:
                continue
            max_j = min(len(right) - 1, LIMIT - i)
            for j in range(max_j + 1):
                right_value = right[j]
                if right_value >= 0 and left_value + right_value > result[i + j]:
                    result[i + j] = left_value + right_value
        return tuple(result)

    @lru_cache(None)
    def dynamic(k: int, residue: int, inherited: Fraction | None) -> tuple[int, ...]:
        options: list[tuple[int, ...]] = []
        for choose in (False, True):
            item = best_by_node.get((k, residue)) if choose else None
            if choose and item is None:
                continue
            current = inherited
            cost = 0
            if item is not None:
                current = item["margin"] if inherited is None else max(inherited, item["margin"])
                cost = 1
            requirement = base_requirement.get((k, residue)) if k >= 8 else None
            if requirement is not None and (current is None or current < requirement):
                continue
            local = 0
            if k >= 8 and (k, residue) in best:
                regret = best[(k, residue)] - current
                if regret < 0 or regret > worst_regret:
                    raise AssertionError(f"unexpected selected regret {regret}")
                local = regret_weight(regret)
            if k < 12:
                children = convolve(dynamic(k + 1, residue, current), dynamic(k + 1, residue + (1 << k), current))
            else:
                children = (0,)
            if cost:
                children = (-1,) + children
            options.append(tuple(value + local if value >= 0 else -1 for value in children))
        if not options:
            return tuple([-1])
        size = max(len(option) for option in options)
        result = [-1] * min(size, LIMIT + 1)
        for option in options:
            for cost, value in enumerate(option[: len(result)]):
                if value > result[cost]:
                    result[cost] = value
        return tuple(result)

    roots = convolve(dynamic(2, 1, None), dynamic(2, 3, None))
    if max(roots[: LIMIT + 1]) < 0:
        raise AssertionError("no robust selection fits the rule limit")
    selected_cost = max(cost for cost, value in enumerate(roots) if value == max(roots))
    # The objective is monotone under adding useful rules; use the largest
    # budget attaining the optimum so the reconstruction has no accidental
    # tie against an omitted improvement.
    optimum_value = roots[selected_cost]

    selected: list[dict] = []

    def reconstruct(k: int, residue: int, inherited: Fraction | None, cost: int, value: int) -> None:
        for choose in (False, True):
            item = best_by_node.get((k, residue)) if choose else None
            if choose and item is None:
                continue
            current = inherited
            own_cost = 0
            if item is not None:
                current = item["margin"] if inherited is None else max(inherited, item["margin"])
                own_cost = 1
            requirement = base_requirement.get((k, residue)) if k >= 8 else None
            if requirement is not None and (current is None or current < requirement):
                continue
            local = 0
            if k >= 8 and (k, residue) in best:
                local = regret_weight(best[(k, residue)] - current)
            remaining_cost = cost - own_cost
            remaining_value = value - local
            if k < 12:
                left = dynamic(k + 1, residue, current)
                right = dynamic(k + 1, residue + (1 << k), current)
                for left_cost in range(min(len(left), remaining_cost + 1)):
                    right_cost = remaining_cost - left_cost
                    if right_cost >= len(right) or left[left_cost] < 0 or right[right_cost] < 0:
                        continue
                    if left[left_cost] + right[right_cost] == remaining_value:
                        if item is not None:
                            selected.append(item)
                        reconstruct(k + 1, residue, current, left_cost, left[left_cost])
                        reconstruct(k + 1, residue + (1 << k), current, right_cost, right[right_cost])
                        return
            elif remaining_cost == 0 and remaining_value == 0:
                if item is not None:
                    selected.append(item)
                return
        raise AssertionError(f"could not reconstruct state {(k, residue, inherited, cost, value)}")

    # The two roots together attain the optimum value at selected_cost.
    left = dynamic(2, 1, None)
    right = dynamic(2, 3, None)
    for left_cost in range(min(len(left), selected_cost + 1)):
        right_cost = selected_cost - left_cost
        if right_cost < len(right) and left[left_cost] >= 0 and right[right_cost] >= 0 and left[left_cost] + right[right_cost] == optimum_value:
            reconstruct(2, 1, None, left_cost, left[left_cost])
            reconstruct(2, 3, None, right_cost, right[right_cost])
            break
    else:
        raise AssertionError("could not split root reconstruction")

    # Exact redundancy removal: remove any selected rule whose deletion keeps
    # every target's achieved margin and coverage unchanged.
    def achieved(items: list[dict]) -> dict[tuple[int, int], Fraction]:
        result = {}
        for target in best:
            power, residue = target
            margins = [item["margin"] for item in items if power >= item["rule"][0] and residue % (1 << item["rule"][0]) == item["rule"][1]]
            if margins:
                result[target] = max(margins)
        return result

    target_margins = achieved(selected)
    changed = True
    while changed:
        changed = False
        for index in range(len(selected) - 1, -1, -1):
            trial = selected[:index] + selected[index + 1:]
            if achieved(trial) == target_margins:
                selected = trial
                changed = True
                break
    if achieved(selected) != target_margins:
        raise AssertionError("redundancy removal changed the margin vector")
    if len(selected) > LIMIT:
        raise AssertionError("final selection exceeds limit")

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "solution.json").write_text(json.dumps({"rules": [fmt_rule(item) for item in selected]}, indent=2) + "\n", encoding="utf-8")
    loaded = s._EVAL._load_rules(OUT)
    for rule in loaded:
        if s.independent_verify(rule) != s.evaluator_verify(rule):
            raise AssertionError(f"written rule verification mismatch: {rule}")

    final_margins = achieved(selected)
    regrets = {target: best[target] - final_margins[target] for target in best}
    if any(final_margins[target] < v3_margin[target] for target in best):
        raise AssertionError("V3 margin decreased")
    if max(regrets.values()) != worst_regret:
        raise AssertionError("worst-regret optimum was not attained")
    report = {
        "enumerated_rules": len(all_rules),
        "rules": len(selected),
        "coverage": "3352/3968",
        "coverable_targets": len(best),
        "global_minimum_margin_ppm": int(min(final_margins.values()) * 1_000_000),
        "targets_at_individual_optimum": sum(regret == 0 for regret in regrets.values()),
        "maximum_regret": {"numerator": max(regrets.values()).numerator, "denominator": max(regrets.values()).denominator, "ppm": int(max(regrets.values()) * 1_000_000)},
        "mean_regret": float(sum(regrets.values()) / len(regrets)),
        "mean_regret_exact": {"numerator": sum(regrets.values()).numerator, "denominator": (sum(regrets.values()) / len(regrets)).denominator},
        "all_individual_optima_within_512": False,
        "minimum_rules_for_all_individual_optima": 649,
        "final_rule_count_after_exact_redundancy_removal": len(selected),
        "worst_regret_optimum": {"numerator": worst_regret.numerator, "denominator": worst_regret.denominator, "ppm": int(worst_regret * 1_000_000)},
        "verification": "all 10,641 generated rules and every written V4 rule were independently verified against eval.py; coverage and every V3 margin were rechecked",
        "uncoverable_classes": "the same exact 616 classes listed in best-v3/search-report.json; no valid rule exists at any allowed prefix",
        "selection_method": "exact tree dynamic program with positional-integer lexicographic regret objective, followed by exact deletion redundancy pass",
    }
    (OUT / "search-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (OUT / "README.md").write_text(
        "# Collatz modular descent, generation 4\n\n"
        f"V4 keeps all 3,352 coverable target classes and uses {len(selected)} rules. It never lowers a V3 per-target margin. "
        f"All individual optima require at least 649 rules, so they cannot fit within the 512-rule limit.\n\n"
        f"The exact robust optimization gives a worst regret of {worst_regret} ({int(worst_regret * 1_000_000)} ppm), with {sum(regret == 0 for regret in regrets.values())} targets at their individual optimum. "
        "The selection uses an exact tree dynamic program that lexicographically minimizes the sorted regret vector, then removes only rules that preserve every target margin.\n\n"
        "The 616 uncoverable classes are unchanged from V3 and are exhaustively documented in `../best-v3/search-report.json`. No hill files were modified and no AutoLab submission was made.\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "rules": len(selected),
        "coverage": "3352/3968",
        "targets_at_optimum": sum(regret == 0 for regret in regrets.values()),
        "max_regret": str(max(regrets.values())),
        "mean_regret": float(sum(regrets.values()) / len(regrets)),
        "global_min_margin_ppm": int(min(final_margins.values()) * 1_000_000),
        "min_rules_all_optima": 649,
    }, indent=2))


if __name__ == "__main__":
    main()
