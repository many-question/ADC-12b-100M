# BUFFER-V8: reduce the physical low-level pull-ups

> Evidence retention (2026-10-31): Superseded raw was released. Historical verification does not imply current availability; [retained evidence](EVIDENCE-RETENTION.md) determines which runs can be re-audited.

B7 passes all 135 terminal-pair checks and physical output validity at its first three corners, but SF low/cold reset is 36.559095 ps against 35 ps. Its weak pull-ups produce about 40-56 mV output low levels and substantial DC energy. This experiment removes one of the two identical PMOS pull-ups at each RP, RN, BP, BN, OUTP and OUTN. One P0.5 um / 100 nm remains at each node; both N0.5 um / 500 nm diode loads on each external output remain. All other B7 devices and capacitances are identical.

The [independent source](BUFFER-V8.txt) has 39 MOS and nine MOM capacitors. Electrical SHA-256: `641de06f404b3c9d3837b4f2c021782942633e43b9064ca2b5169c4ebaa7c841`. Remaining geometries and complete parasitics reuse their successful zero-warning callbacks. Full RNL on a byte-identical Spectre mirror passes core 0.5.2 with 0 errors, 0 warnings and 0 hints; the rendered schematic was inspected.

![Reduced physical rail-offset loads](https://raw.githubusercontent.com/many-question/ADC-12b-100M/0c799462e700c1f74a9448031e14abdd56ec18e7/design/xtor/adc_comp/many-question-miyahara/buffer-v8.png)

The initial TT, FF high/-40 C and SF low/-40 C screen checks all 117 MOS terminal pairs throughout the trace, actual decisions, CMP-15, delay/reset and AVDD energy. Only a passing screen permits the remaining key corners. The original testbench and output-validity thresholds apply without inherited qualification.

## Completed screen 20261031-042059-miyahara-buffer-v8-screen

All three initial corners pass full-trace device stress, timing/reset, actual decisions and CMP-15. SF low/cold reset improves to 33.879369 ps; cold-FF peak stress is 0.99925 V. TT energy falls from B7 668.924396 to 464.617369 fJ/cycle with the same meter. Remaining FF high/hot, SS low/hot and SF high/27 key corners are being screened on this identical electrical source before qualification expands.

Actual clean source commit: `c7b2a78fa20789f4902ef81be26160aacb6e6c58`. Electrical SHA-256: `641de06f404b3c9d3837b4f2c021782942633e43b9064ca2b5169c4ebaa7c841`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ff_high_m40 | 42.515019 / 34.349897 | 22.094980 | 664.274797 | 36 / 36 | 0 | 0 | 0.99925 | 0 / 117 |
| sf_low_m40 | 72.741047 / 56.957899 | 33.879369 | 329.026027 | 36 / 36 | 0 | 0 | 0.82243 | 0 / 117 |
| tt_nom_27 | 58.262829 / 46.752295 | 29.801018 | 464.617369 | 36 / 36 | 0 | 0 | 0.90814 | 0 / 117 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5 ps, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 2 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | ff_high_m40 | sf_low_m40 | tt_nom_27 |
|---|---:|---:|---:|
| MINP | 0.68814 | 0.59499 | 0.59763 |
| MINN | 0.68823 | 0.59509 | 0.59768 |
| MTAIL | 0.99000 | 0.81000 | 0.90000 |
| M14 | 0.99925 | 0.81870 | 0.90769 |
| M15 | 0.99916 | 0.81871 | 0.90767 |
| M12 | 0.99257 | 0.81392 | 0.90236 |
| M13 | 0.99257 | 0.81392 | 0.90236 |
| M10 | 0.97866 | 0.80553 | 0.89068 |
| M11 | 0.97866 | 0.80553 | 0.89068 |
| M6 | 0.99373 | 0.81597 | 0.90311 |
| M7 | 0.99373 | 0.81597 | 0.90311 |
| M8 | 0.99373 | 0.81597 | 0.90311 |
| M9 | 0.99373 | 0.81597 | 0.90311 |
| MCKN | 0.99757 | 0.82014 | 0.90763 |
| MCKP | 0.99758 | 0.81817 | 0.90706 |
| MRQP | 0.99757 | 0.82014 | 0.90763 |
| MRQN | 0.99757 | 0.82014 | 0.90763 |
| MAP | 0.99187 | 0.81187 | 0.90184 |
| MAN | 0.99187 | 0.81266 | 0.90184 |
| MBPP | 0.98577 | 0.80798 | 0.89581 |
| MBPN | 0.99792 | 0.82243 | 0.90814 |
| MOPP | 0.97286 | 0.79988 | 0.88450 |
| MOPN | 0.99792 | 0.82243 | 0.90814 |
| MBNP | 0.98575 | 0.80798 | 0.89579 |
| MBNN | 0.99792 | 0.82242 | 0.90814 |
| MONP | 0.97285 | 0.79988 | 0.88450 |
| MONN | 0.99792 | 0.82242 | 0.90814 |
| MDDP | 0.98233 | 0.80936 | 0.89482 |
| MDDN | 0.98581 | 0.81266 | 0.89835 |
| MUPRP1 | 0.99373 | 0.81597 | 0.90311 |
| MUPRN1 | 0.99373 | 0.81597 | 0.90311 |
| MUPBP1 | 0.99792 | 0.82243 | 0.90814 |
| MUPBN1 | 0.99792 | 0.82242 | 0.90814 |
| MUPOUTP1 | 0.99000 | 0.81912 | 0.90036 |
| MUPOUTN1 | 0.99000 | 0.81912 | 0.90036 |
| MDNOUTP1 | 0.98777 | 0.81912 | 0.90036 |
| MDNOUTP2 | 0.98777 | 0.81912 | 0.90036 |
| MDNOUTN1 | 0.98777 | 0.81912 | 0.90036 |
| MDNOUTN2 | 0.98777 | 0.81912 | 0.90036 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.

## Completed screen 20261031-042502-miyahara-buffer-v8-screen

Across all six key corners, B8 passes full-trace terminal stress, actual decisions and CMP-15. The added SS low/hot corner fails reset at 41.146991 ps, so this version is rejected for noise or full-corner expansion. Its raw output stays high while the deliberately slow CKB/reset path and input-drain recharge resolve; measured event timing is retained for the next repair. TT AVDD energy 464.617369 fJ/cycle is materially above the canonical baseline and is not attributed solely to topology.

Actual clean source commit: `c7b2a78fa20789f4902ef81be26160aacb6e6c58`. Electrical SHA-256: `641de06f404b3c9d3837b4f2c021782942633e43b9064ca2b5169c4ebaa7c841`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ff_high_125 | 50.478579 / 37.705235 | 23.874951 | 781.527313 | 36 / 36 | 0 | 0 | 0.99407 | 0 / 117 |
| sf_high_27 | 54.378291 / 44.187691 | 28.123670 | 639.252398 | 36 / 36 | 0 | 0 | 0.99824 | 0 / 117 |
| ss_low_125 | 83.370380 / 65.458525 | 41.146991 | 343.053110 | 36 / 36 | 0 | 0 | 0.81666 | 0 / 117 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5 ps, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 2 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | ff_high_125 | sf_high_27 | ss_low_125 |
|---|---:|---:|---:|
| MINP | 0.56838 | 0.71164 | 0.54083 |
| MINN | 0.56850 | 0.71174 | 0.54083 |
| MTAIL | 0.99000 | 0.99000 | 0.81000 |
| M14 | 0.98831 | 0.99407 | 0.81416 |
| M15 | 0.98831 | 0.99409 | 0.81399 |
| M12 | 0.98741 | 0.99271 | 0.81119 |
| M13 | 0.98741 | 0.99271 | 0.81119 |
| M10 | 0.95631 | 0.97302 | 0.79917 |
| M11 | 0.95631 | 0.97303 | 0.79917 |
| M6 | 0.97586 | 0.99374 | 0.81002 |
| M7 | 0.97586 | 0.99374 | 0.81002 |
| M8 | 0.98249 | 0.99374 | 0.81002 |
| M9 | 0.98624 | 0.99374 | 0.81002 |
| MCKN | 0.99407 | 0.99824 | 0.81666 |
| MCKP | 0.99000 | 0.99506 | 0.81528 |
| MRQP | 0.99407 | 0.99824 | 0.81666 |
| MRQN | 0.99407 | 0.99824 | 0.81666 |
| MAP | 0.99000 | 0.99102 | 0.81038 |
| MAN | 0.99000 | 0.99102 | 0.81039 |
| MBPP | 0.98579 | 0.98304 | 0.80619 |
| MBPN | 0.99213 | 0.99796 | 0.81559 |
| MOPP | 0.95913 | 0.96490 | 0.79467 |
| MOPN | 0.99213 | 0.99796 | 0.81559 |
| MBNP | 0.98579 | 0.98302 | 0.80618 |
| MBNN | 0.99212 | 0.99795 | 0.81559 |
| MONP | 0.95913 | 0.96490 | 0.79466 |
| MONN | 0.99212 | 0.99795 | 0.81559 |
| MDDP | 0.98249 | 0.98318 | 0.80266 |
| MDDN | 0.98624 | 0.98624 | 0.80330 |
| MUPRP1 | 0.99000 | 0.99374 | 0.81002 |
| MUPRN1 | 0.99000 | 0.99374 | 0.81002 |
| MUPBP1 | 0.99213 | 0.99796 | 0.81559 |
| MUPBN1 | 0.99212 | 0.99795 | 0.81559 |
| MUPOUTP1 | 0.99000 | 0.99000 | 0.81000 |
| MUPOUTN1 | 0.99000 | 0.99000 | 0.81000 |
| MDNOUTP1 | 0.97915 | 0.98928 | 0.80941 |
| MDNOUTP2 | 0.97915 | 0.98928 | 0.80941 |
| MDNOUTN1 | 0.97915 | 0.98928 | 0.80941 |
| MDNOUTN2 | 0.97915 | 0.98928 | 0.80941 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.
