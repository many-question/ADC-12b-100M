# BUFFER-V7: physical rail headroom at raw, buffer and output nodes

> Superseded raw was released. Historical audits do not imply availability; see [retained runs](EVIDENCE-RETENTION.md).

B6 passes clock and XP/XN stress but retains small RP/RN, BP/BN and output excursions. Timing margin is limited, so this experiment keeps B6 clock drive and all capacitances. Each raw, buffer and external output node receives two parallel P0.5 um / 100 nm devices from AVDD, with gates at VSS, to create a small physical low-level offset. Each external output also receives two parallel diode-connected N0.5 um / 500 nm loads to provide high-level headroom. Every device is explicit with m=1 and complete validated parasitics.

These are conducting MOS loads, not ideal voltage clamps. They can change logic levels, static current, regeneration, mismatch and noise. All 45 devices are included in full-trace SOA and supply-energy measurements. Output validity and reset must still meet the original thresholds; the testbench and its external loads are unchanged. All new geometries reuse successful warning-free callbacks from separately recorded experiments.

The [independent source](BUFFER-V7.txt) has 45 MOS and nine MOM capacitors. Electrical SHA-256: `84adf25419d9cc426e80a5d4fc11669679a09444c3e56f1275729e7f1fdfdad1`. Full RNL on a byte-identical Spectre mirror passes core 0.5.2 with 0 errors, 0 warnings and 0 hints.

![Physical rail-offset loads](https://raw.githubusercontent.com/many-question/ADC-12b-100M/0c799462e700c1f74a9448031e14abdd56ec18e7/design/xtor/adc_comp/many-question-miyahara/buffer-v7.png)

The first TT, FF high/-40 C and SF low/-40 C screen checks all 135 MOS terminal pairs throughout the trace, actual decisions, CMP-15, delay/reset and measured AVDD energy. No earlier circuit qualification is inherited.

## Completed screen 20261031-040751-miyahara-buffer-v7-screen

All three corners pass full-trace terminal stress, correct decisions and CMP-15. SF low/cold reset is 36.559095 ps, above 35 ps, so this version is rejected for expansion. The measured output low levels are about 40-56 mV and TT AVDD energy is 668.924396 fJ/cycle. The next experiment halves the six physical PMOS pull-ups while preserving the output diode loads, then rechecks stress and reset together.

Actual clean source commit: `77e70ef858ed08f2f58d3f79d5105babf005a18c`. Electrical SHA-256: `84adf25419d9cc426e80a5d4fc11669679a09444c3e56f1275729e7f1fdfdad1`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ff_high_m40 | 42.032806 / 33.805174 | 23.988897 | 993.041121 | 36 / 36 | 0 | 0 | 0.99907 | 0 / 135 |
| sf_low_m40 | 75.305665 / 55.761104 | 36.559095 | 486.255424 | 36 / 36 | 0 | 0 | 0.82013 | 0 / 135 |
| tt_nom_27 | 57.891587 / 45.992390 | 31.940311 | 668.924396 | 36 / 36 | 0 | 0 | 0.90763 | 0 / 135 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5 ps, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 2 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | ff_high_m40 | sf_low_m40 | tt_nom_27 |
|---|---:|---:|---:|
| MINP | 0.68817 | 0.59504 | 0.59766 |
| MINN | 0.68827 | 0.59514 | 0.59771 |
| MTAIL | 0.99000 | 0.81000 | 0.90000 |
| M14 | 0.99907 | 0.81846 | 0.90755 |
| M15 | 0.99905 | 0.81847 | 0.90756 |
| M12 | 0.99239 | 0.81370 | 0.90220 |
| M13 | 0.99239 | 0.81370 | 0.90220 |
| M10 | 0.96494 | 0.79489 | 0.87857 |
| M11 | 0.96494 | 0.79489 | 0.87857 |
| M6 | 0.99339 | 0.81578 | 0.90281 |
| M7 | 0.99339 | 0.81578 | 0.90281 |
| M8 | 0.99339 | 0.81578 | 0.90281 |
| M9 | 0.99339 | 0.81577 | 0.90281 |
| MCKN | 0.99756 | 0.82013 | 0.90763 |
| MCKP | 0.99758 | 0.81817 | 0.90706 |
| MRQP | 0.99756 | 0.82013 | 0.90763 |
| MRQN | 0.99756 | 0.82013 | 0.90763 |
| MAP | 0.99187 | 0.81187 | 0.90184 |
| MAN | 0.99187 | 0.81266 | 0.90184 |
| MBPP | 0.97527 | 0.79746 | 0.88686 |
| MBPN | 0.99678 | 0.81999 | 0.90671 |
| MOPP | 0.94184 | 0.77431 | 0.85771 |
| MOPN | 0.99678 | 0.81999 | 0.90671 |
| MBNP | 0.97526 | 0.79746 | 0.88684 |
| MBNN | 0.99677 | 0.81997 | 0.90670 |
| MONP | 0.94184 | 0.77430 | 0.85770 |
| MONN | 0.99677 | 0.81997 | 0.90670 |
| MDDP | 0.98233 | 0.80936 | 0.89482 |
| MDDN | 0.98581 | 0.81266 | 0.89835 |
| MUPRP1 | 0.99339 | 0.81578 | 0.90281 |
| MUPRP2 | 0.99339 | 0.81578 | 0.90281 |
| MUPRN1 | 0.99339 | 0.81577 | 0.90281 |
| MUPRN2 | 0.99339 | 0.81577 | 0.90281 |
| MUPBP1 | 0.99678 | 0.81999 | 0.90671 |
| MUPBP2 | 0.99678 | 0.81999 | 0.90671 |
| MUPBN1 | 0.99677 | 0.81997 | 0.90670 |
| MUPBN2 | 0.99677 | 0.81997 | 0.90670 |
| MUPOUTP1 | 0.99000 | 0.81643 | 0.90000 |
| MUPOUTP2 | 0.99000 | 0.81643 | 0.90000 |
| MUPOUTN1 | 0.99000 | 0.81643 | 0.90000 |
| MUPOUTN2 | 0.99000 | 0.81643 | 0.90000 |
| MDNOUTP1 | 0.98620 | 0.81643 | 0.89848 |
| MDNOUTP2 | 0.98620 | 0.81643 | 0.89848 |
| MDNOUTN1 | 0.98620 | 0.81643 | 0.89848 |
| MDNOUTN2 | 0.98620 | 0.81643 | 0.89848 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.
