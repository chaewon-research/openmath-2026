# V4 versus V5-A diagnosis

V4 and V5-A each contain 512 rules. They share 213 exact rules; V5-A removes 299 and adds 299.
Both preserve all 3352 public coverable target classes.

The ranked removal list is in `v4-v5a-diagnosis.json`. Each removed rule includes its exact public support, margin, single-rule replacement test, and every target whose achieved margin fell after the complete V4-to-V5-A change.

Top likely explanation: V5-A kept the V3 coverage backbone, which includes low-margin rules that V4 deliberately replaced or supplemented. A full public coverage tie therefore does not preserve private-target margins.

The first ablation should start from exact V4 and alter one removed/replaced support group identified at the top of the JSON ranking. Submit only after reviewing that proposed one-change patch.
