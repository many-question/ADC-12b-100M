# RESET-V10: advance reset-load turn-on and bound the clock low level

> Evidence retention (2026-10-31): Superseded raw was released. Historical verification does not imply current availability; [retained evidence](EVIDENCE-RETENTION.md) determines which runs can be re-audited.

V9 shows that increasing Q shunt conductance alone leaves an early cold-FF peak and violates slow-corner reset. This experiment starts from V8 with the lighter N1 Q shunts. The CKB pull-up becomes P3 instead of P2 to turn the shunts on earlier. Direct input precharge becomes P2 instead of P2.4 to offset the external clock-capacitance increase. Input diode loads remain and their recharge time is rechecked.

The faster clock pull-up can increase the negative clock-edge excursion. A weak P0.5 um / 100 nm from AVDD to CKB, with its gate at VSS, provides a small physical low-level pull-up; the existing weak NMOS clock load remains. The resulting clock voltage range, low-level leakage into the Q loads, reset overlap and DC energy are all measured. This is not an ideal clamp or an extra bias supply. Both new PMOS geometries have successful zero-warning callbacks.

The [independent source](RESET-V10.txt) contains 23 MOS and three MOM capacitors. Electrical SHA-256: `a6834ef58286ccc4676a5f400d1c8a1c9abf53b05f5b7341cbf2809551ee0cb3`. Full RNL on its byte-identical Spectre mirror passes core 0.5.2 with 0 errors, 0 warnings and 0 hints.

![Earlier reset-load turn-on and physical clock floor](https://raw.githubusercontent.com/many-question/ADC-12b-100M/596782536a7b43a5a893660a926aa339927ea784/design/xtor/adc_comp/many-question-strongarm/reset-v10.png)

The first four key corners check all 69 MOS terminal pairs throughout the trace, correct decisions and CMP-15, delay/reset and exact AVDD energy. The clock-charge diagnostic does not replace official CMP-14. No inherited performance pass is claimed.

## Completed screen 20261031-040457-strongarm-reset-v10-screen

The four corners all pass full-trace device stress, correct decisions and CMP-15. Cold FF peaks at 0.99801 V. This version is still rejected for expansion because SS low/hot reset is 35.044926 ps, above the 35 ps limit; it is not rounded into a pass. TT30mV is 46.285275 ps. The next experiment changes only input-precharge strength to gain reset margin while keeping the clock-capacitance budget under review.

Actual clean source commit: `1bf252e30b64cc95a09005c4d352b6c5e302a1e9`. Electrical SHA-256: `a6834ef58286ccc4676a5f400d1c8a1c9abf53b05f5b7341cbf2809551ee0cb3`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ff_high_125 | 42.254520 / 31.980046 | 23.023389 | 874.879356 | 36 / 36 | 0 | 0 | 0.99000 | 0 / 69 |
| ff_high_m40 | 43.104127 / 34.868894 | 19.529473 | 819.782277 | 36 / 36 | 0 | 0 | 0.99801 | 0 / 69 |
| ss_low_125 | 76.520068 / 59.916895 | 35.044926 | 400.475172 | 36 / 36 | 0 | 0 | 0.82252 | 0 / 69 |
| tt_nom_27 | 57.818259 / 46.285275 | 25.328027 | 570.864284 | 36 / 36 | 0 | 0 | 0.91202 | 0 / 69 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5 ps, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 3 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | ff_high_125 | ff_high_m40 | ss_low_125 | tt_nom_27 |
|---|---:|---:|---:|---:|
| MINP | 0.56302 | 0.67973 | 0.53618 | 0.59063 |
| MINN | 0.56311 | 0.67984 | 0.53617 | 0.59068 |
| MTAIL | 0.99000 | 0.99000 | 0.81000 | 0.90000 |
| MRDP | 0.99000 | 0.99234 | 0.81000 | 0.90159 |
| MRDN | 0.99000 | 0.99234 | 0.81001 | 0.90159 |
| MLNP | 0.95956 | 0.98991 | 0.80211 | 0.89866 |
| MLNN | 0.95956 | 0.98991 | 0.80210 | 0.89866 |
| MLPP | 0.96529 | 0.99280 | 0.80597 | 0.90203 |
| MLPN | 0.96529 | 0.99280 | 0.80597 | 0.90203 |
| MRQP | 0.99000 | 0.99281 | 0.82252 | 0.91202 |
| MRQN | 0.99000 | 0.99281 | 0.82252 | 0.91202 |
| MOPN | 0.98995 | 0.99801 | 0.82252 | 0.91202 |
| MOPP | 0.98639 | 0.99769 | 0.82140 | 0.91147 |
| MONN | 0.98995 | 0.99801 | 0.82252 | 0.91202 |
| MONP | 0.98639 | 0.99769 | 0.82140 | 0.91147 |
| MDQP | 0.98995 | 0.99801 | 0.82252 | 0.91202 |
| MDQN | 0.98995 | 0.99801 | 0.82252 | 0.91202 |
| MDDP | 0.98428 | 0.98416 | 0.80657 | 0.89681 |
| MDDN | 0.98778 | 0.98729 | 0.81001 | 0.90015 |
| MCKN | 0.99000 | 0.99095 | 0.81276 | 0.90257 |
| MCKP | 0.99000 | 0.99000 | 0.81000 | 0.90000 |
| MBLEED | 0.99000 | 0.99095 | 0.81276 | 0.90257 |
| MUP | 0.99000 | 0.99095 | 0.81276 | 0.90257 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.
