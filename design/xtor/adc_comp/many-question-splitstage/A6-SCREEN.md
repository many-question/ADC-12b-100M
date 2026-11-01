# A6 second input-pair screen

A6 changes only MSIP/MSIN from W4/nf4 to W6/nf6, with L=30 nm, Wfg=1 um and complete callback-derived geometry. All connections, tails, regeneration, clocks, MOM and outputs are unchanged. It remains a fully dynamic 40-MOS/10-MOM circuit with the same interface. Status is `wip`.

A5 is frozen at commit `97b387c8e57fe431e81db00767f26e1465926c63`; its [FS noise failure](A5-NOISE.md) and deterministic evidence remain historical, not A6 results. A6 currently has no measured result. The prior six-device noise mask did not isolate this input pair, so a larger pair's gm cannot be treated as the six-device group's noise benefit.

Authorized first screen: official TT and SF 36-cycle delay plus TT loading/kickback, three jobs. Check all applicable specification 0.9.0 gates, every decision/reset, all MOS terminal pairs, TT d30 margin, SF validity and stress, Cin <=20 fF and CLK <=16 fF. Report physical phase changes without adding a CKL-invariance threshold. Save only metric/SOA voltages, supply current, and MSIP/MSIN gm/ids/cgg/cdd/css. If all three pass and are archived, one FS-low125 official 36-cycle deterministic screen is permitted. Any failure stops expansion. No long noise, additional corners, MC, CM or parameter sweep is authorized.

## Source identity

Source SHA256: `8d300f399e0ff5b9f2273ba23c166ce6de63aa8218da1dd434ad4b2225d00621`

Electrical SHA256: `fb35051d0ec3e345c550baddafc8e3ab43d9de7187453188e365cddca1544274`

Callback SHA256: `366665f177a5e0fa47867870abb748ef434192c29fa58f63463f476a80847c8e`
