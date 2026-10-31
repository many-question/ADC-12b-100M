# RESET-V12: reduce Q reset slew and lower the output trip point

> Evidence retention (2026-10-31): Historical raw/archive statements below refer to the original audit. Superseded waveforms were released under the user's retention policy. [EVIDENCE-RETENTION](EVIDENCE-RETENTION.md) lists the completed runs still available for raw re-audit.

V11 fails SF low/cold physical output validity while the two Q nodes are still regenerating, and its SF high/27 Q peak occurs 5.46 ps after the falling clock edge. This experiment strengthens each output NMOS from N2 to N3 to keep the losing output low through the common-mode dip. It also weakens each direct Q precharge from P4 to P3 to slow the measured reset coupling. The lower output trip point may offset the slower Q recharge in the external reset metric; this is a hypothesis, not an inherited pass. Q shunts and the physical clock remain unchanged. Both complete geometries reuse successful validated parameters.

The [independent source](RESET-V12.txt) has electrical SHA-256 `fbec8c61b7accb7fdf85ccff4c17f53b68589be849236a1558ba70628a46d846`. Full RNL on its byte-identical Spectre mirror passes core 0.5.2 with 0 errors, 0 warnings and 0 hints; the schematic was inspected.

![Physical reset and output repair](https://raw.githubusercontent.com/many-question/ADC-12b-100M/596782536a7b43a5a893660a926aa339927ea784/design/xtor/adc_comp/many-question-strongarm/reset-v12.png)

Six key corners now include both limiting SF cases and SS low/hot, together with TT and FF high/cold/hot. Every MOS terminal pair, all physical decisions, output validity, delay/reset and AVDD energy are checked over the entire trace. The next necessary simulations also save AVDD and device branch currents so reset/evaluation energy and persistent load current can be measured. See [energy comparison](ENERGY-COMPARISON.md); no prior qualification or topology-only efficiency advantage is claimed.

## Completed screen 20261031-043904-strongarm-reset-v12-screen

All six key corners pass physical output validity, including the prior SF low/cold failure. This version still fails SF high/27 terminal stress at 1.00002 V (four pairs) and SS low/hot reset at 35.861626 ps. Neither small exceedance is rounded into a pass. TT 30 mV delay is 47.437314 ps. The measured energy audit confirms persistent Q-reset contention; the next change targets the remaining physical output reset/slew without increasing the Q-shunt DC load.

Actual clean source commit: `9040b6f870435b961373c973525cd2bce74d28e1`. Electrical SHA-256: `fbec8c61b7accb7fdf85ccff4c17f53b68589be849236a1558ba70628a46d846`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ff_high_125 | 44.654233 / 34.202807 | 23.270977 | 903.120545 | 36 / 36 | 0 | 0 | 0.99017 | 0 / 69 |
| ff_high_m40 | 44.376792 / 35.930840 | 19.943228 | 825.236943 | 36 / 36 | 0 | 0 | 0.99760 | 0 / 69 |
| sf_high_27 | 59.227946 / 47.057952 | 22.532551 | 729.225057 | 36 / 36 | 0 | 0 | 1.00002 | 4 / 69 |
| sf_low_m40 | 85.166407 / 69.777139 | 25.592906 | 398.466436 | 36 / 36 | 0 | 0 | 0.82465 | 0 / 69 |
| ss_low_125 | 78.438410 / 61.590427 | 35.861626 | 404.010910 | 36 / 36 | 0 | 0 | 0.82155 | 0 / 69 |
| tt_nom_27 | 59.211066 / 47.437314 | 25.878703 | 574.028610 | 36 / 36 | 0 | 0 | 0.91080 | 0 / 69 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5 ps, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 3 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | ff_high_125 | ff_high_m40 | sf_high_27 | sf_low_m40 | ss_low_125 | tt_nom_27 |
|---|---:|---:|---:|---:|---:|---:|
| MINP | 0.56595 | 0.68319 | 0.70902 | 0.58947 | 0.53605 | 0.59341 |
| MINN | 0.56606 | 0.68327 | 0.70909 | 0.58957 | 0.53604 | 0.59345 |
| MTAIL | 0.99000 | 0.99000 | 0.99000 | 0.81000 | 0.81000 | 0.90000 |
| MRDP | 0.99000 | 0.99217 | 0.99000 | 0.81171 | 0.81000 | 0.90141 |
| MRDN | 0.99000 | 0.99217 | 0.99000 | 0.81318 | 0.81070 | 0.90141 |
| MLNP | 0.96001 | 0.99017 | 0.98797 | 0.80978 | 0.80208 | 0.89900 |
| MLNN | 0.96001 | 0.99017 | 0.98796 | 0.80979 | 0.80206 | 0.89900 |
| MLPP | 0.96552 | 0.99237 | 0.99002 | 0.81197 | 0.80552 | 0.90158 |
| MLPN | 0.96552 | 0.99237 | 0.99002 | 0.81197 | 0.80552 | 0.90158 |
| MRQP | 0.99000 | 0.99237 | 0.99989 | 0.82465 | 0.82155 | 0.91080 |
| MRQN | 0.99000 | 0.99237 | 0.99989 | 0.82465 | 0.82155 | 0.91080 |
| MOPN | 0.99017 | 0.99760 | 1.00002 | 0.82465 | 0.82155 | 0.91080 |
| MOPP | 0.98785 | 0.99738 | 0.99955 | 0.82412 | 0.82076 | 0.91043 |
| MONN | 0.99017 | 0.99760 | 1.00002 | 0.82465 | 0.82155 | 0.91080 |
| MONP | 0.98785 | 0.99738 | 0.99955 | 0.82412 | 0.82076 | 0.91043 |
| MDQP | 0.99017 | 0.99760 | 1.00002 | 0.82465 | 0.82155 | 0.91080 |
| MDQN | 0.99017 | 0.99760 | 1.00002 | 0.82465 | 0.82155 | 0.91080 |
| MDDP | 0.98475 | 0.98476 | 0.98558 | 0.81030 | 0.80742 | 0.89729 |
| MDDN | 0.98804 | 0.98768 | 0.98823 | 0.81318 | 0.81070 | 0.90044 |
| MCKN | 0.99000 | 0.99090 | 0.99264 | 0.81640 | 0.81271 | 0.90252 |
| MCKP | 0.99000 | 0.99000 | 0.99000 | 0.81000 | 0.81000 | 0.90000 |
| MBLEED | 0.99000 | 0.99090 | 0.99264 | 0.81640 | 0.81271 | 0.90252 |
| MUP | 0.99000 | 0.99090 | 0.99264 | 0.81640 | 0.81271 | 0.90252 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.
