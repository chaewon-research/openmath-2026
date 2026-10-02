#!/usr/bin/env python3
"""Offline check of a fixed certificate; no search or private scoring."""
import argparse
import hashlib
import importlib.util
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECTED = '1e533cbd5dbb17bb6ad52c7c80faa3a6abce587a32204ef5228de54da5b069e6'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify(rule):
    k, r, exponents = rule
    total = 0
    a, b = 1, 0
    x = r
    for e in exponents:
        value = 3 * x + 1
        require(value % (1 << e) == 0 and (value >> e) % 2 == 1,
                'valuation mismatch')
        # Compose (a*n+b)/2^total using integer arithmetic.
        a, b = 3 * a, 3 * b + (1 << total)
        total += e
        x = value >> e
        require(k >= total + 1, 'unstable valuation pattern')
    d = 1 << total
    require(a < d, 'noncontractive affine map')
    require(a * r + b < d * r, 'no descent at least representative')
    require(a * r + b == d * x, 'affine composition mismatch')
    return {'modulus_power': k, 'residue': r, 'exponents': list(exponents),
            'affine_numerator_factor': a, 'affine_constant': b,
            'denominator': d, 'least_representative_image': x,
            'contraction_margin': str(Fraction(d-a, d))}


def coverage(rules, powers):
    return [{'modulus_power': p,
             'covered_residues': [r for r in range(1, 1 << p, 2)
                                  if any(p >= k and r % (1 << k) == q
                                         for k, q, _ in rules)]}
            for p in powers]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    raw = (ROOT / 'solution.json').read_bytes()
    require(hashlib.sha256(raw).hexdigest() == EXPECTED, 'preserved solution hash mismatch')
    spec = importlib.util.spec_from_file_location('public_eval', ROOT / 'public-hill/eval.py')
    evaluator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(evaluator)
    # Use public schema validation, then independent affine arithmetic.
    rules = evaluator._load_rules(ROOT)
    witnesses = [verify(rule) for rule in rules]
    for rule, witness in zip(rules, witnesses):
        require(str(evaluator._verify_rule(rule)['margin']) == witness['contraction_margin'],
                'public verifier disagreement')
    public = coverage(rules, range(8, 13))
    kmax = max(k for k, _, _ in rules)
    finest = coverage(rules, [kmax])[0]
    baselines = {}
    for name in ['organizer-baseline', 'local-22-rule-baseline']:
        data = json.loads((ROOT / 'history' / (name+'.json')).read_text())
        rr = [(x['modulus_power'], x['residue'], tuple(x['exponents'])) for x in data['rules']]
        for rule in rr:
            verify(rule)
        cc = coverage(rr, range(8, 13))
        baselines[name] = {'rule_count': len(rr), 'public_covered': sum(len(x['covered_residues']) for x in cc),
                           'added_public_classes': sum(len(set(x['covered_residues'])-set(y['covered_residues'])) for x,y in zip(public, cc)),
                           'lost_public_classes': sum(len(set(y['covered_residues'])-set(x['covered_residues'])) for x,y in zip(public, cc))}
    result = {'scope': 'local offline certificate inspection; not official AutoLab evaluation',
              'solution_sha256': EXPECTED, 'rules_verified': len(rules),
              'modulus_power_min': min(k for k,_,_ in rules), 'modulus_power_max': kmax,
              'steps_max': max(len(e) for _,_,e in rules),
              'public_universe_size': 3968,
              'public_covered': sum(len(x['covered_residues']) for x in public),
              'public_classes': public, 'finest_modulus_union': finest,
              'odd_residue_density': str(Fraction(len(finest['covered_residues']), 1 << (kmax-1))),
              'baseline_comparison': baselines, 'rule_witnesses': witnesses}
    if args.output:
        args.output.write_text(json.dumps(result, indent=2)+'\n')
    print('PASS: preserved SHA-256; 512 exact descent rules; public verifier agrees')
    print(f"Public classes: {result['public_covered']}/3968 (powers 8..12)")
    print(f"Union at power {kmax}: {len(finest['covered_residues'])}/{1 << (kmax-1)} odd residues")
    print(json.dumps(baselines, sort_keys=True))


if __name__ == '__main__':
    main()
