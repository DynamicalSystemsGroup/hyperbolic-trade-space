Levels and ranges (read from the model by the views generator):

- wheelClass (enum WheelClass): small | medium | large
- grade (enum TrackerGrade): coarse | medium | fine
- panelSpan: 0.3 m .. 1 m
- batteryCapacity: 20 W*h .. 200 W*h
- Gains Kp and Kd: one range per regime
- Kp: 0.03 .. 1 (baseline regime, baselineGains); 0.2 .. 2 (primary regime, aggressiveGains)
- Kd: 0.3 .. 1.5 (both regimes)
