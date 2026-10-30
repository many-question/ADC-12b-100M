# RESET-V17: reduce Q reset-shunt strength

V16's matched short fine-step noise diagnosis improves from V15's 52/256 wrong polarities to 13/256 at +/-800 uV, while all 256 resets, stable early/mid-to-final signs, output validity and full 69-pair MOS stress pass. QP at rising midpoint +5 ps rises from approximately 0.586 V to 0.649 V. The +30 ps Q differential standard deviation drops to 1.34/1.52 mV, but is still large relative to the input-derived differential signal. These short two-level records are diagnostic only and do not estimate formal noise or isolate one device's noise contribution. V16 expansion stops.

This source changes only MDQP and MDQN from 1 um/30 nm to 0.5 um/30 nm, reusing the complete successful N0.5 geometry already present in V3. All terminal parasitics are copied exactly; callback SHA-256 is `fc440ca368b3063979554e2eef4ee6e93e94e1210a67f7d94f97302d09b192b2`. The N4/P3 clock inverter and 4.46 fF CKB capacitor remain. Weaker reset shunts are intended to reduce Q discharge during release and the premature growth of differential noise. Less charge absorption may restore the earlier Q overshoot, so SF/high/-40 and FS/high/-40 are mandatory first screens. No stress or noise benefit is assumed.

Electrical SHA-256: `24d5361e213a9a02c24ddf4a40a347409d16f89b5c9f43e8182fdcbb6487dbd6`. The [source](RESET-V17.txt) retains all 23 MOS and 3 MOM devices with complete RNL, checked through a byte-identical mirror. Canonical V14 and every prior failed version remain preserved. TT timing and a matched short noise diagnosis follow only if the first stress gates pass; no expanded-corner or formal qualification is claimed at source freeze.

![Physical circuit with weaker Q reset shunts](reset-v17.png)
