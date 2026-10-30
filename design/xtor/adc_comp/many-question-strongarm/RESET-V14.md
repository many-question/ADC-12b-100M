# RESET-V14: earlier reset-shunt enable

V13 passes delay, reset and physical output validity at all ten measured corners, but SF/high/-40 reaches QN=1.001890426 V and fails 10 terminal pairs. The peak occurs 5.355228 ps after the falling clock 50% crossing, with CKB still at 0.635933 V. The clock-controlled Q shunt therefore has limited gate drive during the coupled reset peak.

This experiment changes only MCKP from P3/nf3 to P4/nf4, using the complete identical callback-validated geometry of MOPP. The stronger pull-up is intended to enable the existing N1 Q shunts earlier. All 23 MOS and 3 physical MOM capacitors remain individually represented. The extra clock input charge and persistent-current cost must be measured.

The [independent source](RESET-V14.txt) has electrical SHA-256 `dd44da2a98a529e3f4dced4b72a1728101738d03a1bdc63d4042371206fa6455`. Full RNL on a byte-identical Spectre mirror passes core 0.5.2 with 0 errors, 0 warnings and 0 hints. The rendered schematic was inspected.

![Earlier Q-shunt enable](reset-v14.png)

Screen SF/high/-40 and FS/high/-40 first. Only after they pass, complete TT, SS low/hot, SF low/cold, FF high/cold and high/hot, SF high/27 and high/hot, and FS low/hot. Check every MOS terminal voltage over the complete trace, all 36 physical polarities and resets, validity, delay, regeneration time and AVDD energy. Keep the total session concurrency at or below six jobs. No prior noise, mismatch or capacitance performance is inherited.

Passing screening would be supplemental evidence. Canonical promotion and qualification use the existing official runner, with old records preserved and honestly marked stale until replaced.

## Completed screen 20261031-051253-strongarm-reset-v14-screen

Both known cold high-voltage target corners pass delay, reset, regeneration, full-trace terminal stress and physical output validity. Each has 36 correct decisions including 10 uV and 36 completed resets. SF/high/-40 maximum stress is 0.99962 V; FS/high/-40 is 0.99831 V. This authorizes screening the eight remaining known key corners, not canonical promotion or noise/MC. The SF margin is only about 0.38 mV, so motivated numerical convergence is required before qualification.

Actual clean source commit: `37096377eecb0be000eb6f532e9f6803b5bf95d8`. Electrical SHA-256: `dd44da2a98a529e3f4dced4b72a1728101738d03a1bdc63d4042371206fa6455`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fs_high_m40 | 52.545659 / 43.680660 | 21.760831 | 790.890395 | 36 / 36 | 0 | 0 | 0.99831 | 0 / 69 |
| sf_high_m40 | 66.079582 / 53.660276 | 19.910932 | 747.431846 | 36 / 36 | 0 | 0 | 0.99962 | 0 / 69 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | fs_high_m40 | sf_high_m40 |
|---|---:|---:|
| MINP | 0.68738 | 0.75586 |
| MINN | 0.68746 | 0.75601 |
| MTAIL | 0.99000 | 0.99000 |
| MRDP | 0.99333 | 0.99210 |
| MRDN | 0.99333 | 0.99210 |
| MLNP | 0.99116 | 0.99011 |
| MLNN | 0.99116 | 0.99011 |
| MLPP | 0.99349 | 0.99236 |
| MLPN | 0.99349 | 0.99236 |
| MRQP | 0.99573 | 0.99646 |
| MRQN | 0.99572 | 0.99646 |
| MOPN | 0.99786 | 0.99962 |
| MOPP | 0.99831 | 0.99938 |
| MONN | 0.99786 | 0.99962 |
| MONP | 0.99831 | 0.99938 |
| MDQP | 0.99786 | 0.99962 |
| MDQN | 0.99786 | 0.99962 |
| MDDP | 0.98352 | 0.98519 |
| MDDN | 0.98663 | 0.98767 |
| MCKN | 0.99289 | 0.99506 |
| MCKP | 0.99000 | 0.99000 |
| MBLEED | 0.99289 | 0.99506 |
| MUP | 0.99289 | 0.99506 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.

## Completed screen 20261031-051938-strongarm-reset-v14-screen

All eight remaining key corners pass delay, reset, regeneration, full-trace terminal stress and physical output validity. Each has 36 correct polarities including 10 uV and 36 completed resets. Together with the first two corners, all ten known key corners pass; actual worst stress remains SF/high/-40 at 0.99962 V from the first batch. TT 1/30 mV delays are 60.215237/48.208714 ps; worst measured reset is SS/low/125 at 33.737829 ps. TT mixed-sequence energy is 580.511994 fJ/cycle. Targeted 0.125 ps, reltol 1e-7, vabstol 1e-9 convergence at SF/high/-40 is required before canonical promotion. No capacitance/noise/MC or remaining-corner qualification is inferred.

Actual clean source commit: `37096377eecb0be000eb6f532e9f6803b5bf95d8`. Electrical SHA-256: `dd44da2a98a529e3f4dced4b72a1728101738d03a1bdc63d4042371206fa6455`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ff_high_125 | 46.600090 / 36.007388 | 21.454984 | 922.440049 | 36 / 36 | 0 | 0 | 0.99095 | 0 / 69 |
| ff_high_m40 | 45.285151 / 36.647814 | 18.847976 | 834.579339 | 36 / 36 | 0 | 0 | 0.99654 | 0 / 69 |
| fs_low_125 | 61.867614 / 48.867012 | 30.290929 | 486.386089 | 36 / 36 | 0 | 0 | 0.81264 | 0 / 69 |
| sf_high_125 | 58.123893 / 45.217426 | 23.250480 | 783.036207 | 36 / 36 | 0 | 0 | 0.99605 | 0 / 69 |
| sf_high_27 | 60.377061 / 47.952654 | 21.194777 | 738.522172 | 36 / 36 | 0 | 0 | 0.99841 | 0 / 69 |
| sf_low_m40 | 86.282335 / 70.421511 | 23.954596 | 402.807388 | 36 / 36 | 0 | 0 | 0.82212 | 0 / 69 |
| ss_low_125 | 79.904546 / 62.802871 | 33.737829 | 409.809589 | 36 / 36 | 0 | 0 | 0.82028 | 0 / 69 |
| tt_nom_27 | 60.215237 / 48.208714 | 24.336324 | 580.511994 | 36 / 36 | 0 | 0 | 0.90789 | 0 / 69 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 4 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | ff_high_125 | ff_high_m40 | fs_low_125 | sf_high_125 | sf_high_27 | sf_low_m40 | ss_low_125 | tt_nom_27 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| MINP | 0.56571 | 0.68302 | 0.53160 | 0.64097 | 0.70890 | 0.58946 | 0.53599 | 0.59333 |
| MINN | 0.56581 | 0.68310 | 0.53160 | 0.64100 | 0.70899 | 0.58957 | 0.53598 | 0.59338 |
| MTAIL | 0.99000 | 0.99000 | 0.81000 | 0.99000 | 0.99000 | 0.81000 | 0.81000 | 0.90000 |
| MRDP | 0.99000 | 0.99217 | 0.81000 | 0.99000 | 0.99000 | 0.81167 | 0.81000 | 0.90139 |
| MRDN | 0.99000 | 0.99217 | 0.81063 | 0.99000 | 0.99000 | 0.81318 | 0.81067 | 0.90139 |
| MLNP | 0.96000 | 0.99016 | 0.79447 | 0.97478 | 0.98795 | 0.80974 | 0.80201 | 0.89899 |
| MLNN | 0.96000 | 0.99016 | 0.79447 | 0.97478 | 0.98795 | 0.80975 | 0.80200 | 0.89899 |
| MLPP | 0.96550 | 0.99237 | 0.80135 | 0.97576 | 0.99000 | 0.81194 | 0.80545 | 0.90156 |
| MLPN | 0.96550 | 0.99237 | 0.80135 | 0.97576 | 0.99000 | 0.81194 | 0.80545 | 0.90156 |
| MRQP | 0.99000 | 0.99237 | 0.81264 | 0.99219 | 0.99468 | 0.82212 | 0.82028 | 0.90744 |
| MRQN | 0.99000 | 0.99236 | 0.81264 | 0.99219 | 0.99468 | 0.82212 | 0.82028 | 0.90744 |
| MOPN | 0.98892 | 0.99654 | 0.81264 | 0.99605 | 0.99841 | 0.82212 | 0.82028 | 0.90789 |
| MOPP | 0.98853 | 0.99635 | 0.81217 | 0.99416 | 0.99801 | 0.82175 | 0.81960 | 0.90763 |
| MONN | 0.98892 | 0.99654 | 0.81264 | 0.99605 | 0.99841 | 0.82212 | 0.82028 | 0.90789 |
| MONP | 0.98853 | 0.99635 | 0.81217 | 0.99416 | 0.99801 | 0.82175 | 0.81960 | 0.90763 |
| MDQP | 0.99095 | 0.99654 | 0.81264 | 0.99605 | 0.99841 | 0.82212 | 0.82028 | 0.90789 |
| MDQN | 0.99095 | 0.99654 | 0.81264 | 0.99605 | 0.99841 | 0.82212 | 0.82028 | 0.90789 |
| MDDP | 0.98475 | 0.98476 | 0.80683 | 0.98555 | 0.98558 | 0.81030 | 0.80740 | 0.89729 |
| MDDN | 0.98803 | 0.98767 | 0.81063 | 0.98843 | 0.98823 | 0.81318 | 0.81067 | 0.90043 |
| MCKN | 0.99095 | 0.99341 | 0.81195 | 0.99447 | 0.99515 | 0.81863 | 0.81573 | 0.90518 |
| MCKP | 0.99000 | 0.99000 | 0.81000 | 0.99000 | 0.99000 | 0.81000 | 0.81000 | 0.90000 |
| MBLEED | 0.99095 | 0.99341 | 0.81195 | 0.99447 | 0.99515 | 0.81863 | 0.81573 | 0.90518 |
| MUP | 0.99095 | 0.99341 | 0.81195 | 0.99447 | 0.99515 | 0.81863 | 0.81573 | 0.90518 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.

## Completed screen 20261031-052832-strongarm-reset-v14-screen

The actual worst key corner SF/high/-40 passes the targeted tighter numerical run: maxstep 0.125 ps, reltol 1e-7, vabstol 1e-9. Effective simulator settings are confirmed in the log. All 69 terminal pairs pass; maximum stress remains 0.99962 V, with at most 0.010 mV difference in any tabulated pair peak (10 uV reporting precision). Relative to the 0.5 ps run on the same electrical source, 1 mV delay changes +0.009429 ps, 30 mV delay +0.002262 ps, reset -0.098389 ps and energy +0.017411 fJ/cycle. All 36 actual polarities including 10 uV and all 36 resets pass. This supports canonical promotion for official new-source TT capacitance/kickback and noise tests; all remaining qualification remains open.

Actual clean source commit: `b4e50b179f47bd9d4856013bd908fe6f3ed49649`. Electrical SHA-256: `dd44da2a98a529e3f4dced4b72a1728101738d03a1bdc63d4042371206fa6455`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| sf_high_m40 | 66.089011 / 53.662539 | 19.812544 | 747.449257 | 36 / 36 | 0 | 0 | 0.99962 | 0 / 69 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.125p, reltol=1e-7 and vabstol=1e-9. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | sf_high_m40 |
|---|---:|
| MINP | 0.75586 |
| MINN | 0.75601 |
| MTAIL | 0.99000 |
| MRDP | 0.99210 |
| MRDN | 0.99210 |
| MLNP | 0.99012 |
| MLNN | 0.99012 |
| MLPP | 0.99237 |
| MLPN | 0.99237 |
| MRQP | 0.99647 |
| MRQN | 0.99647 |
| MOPN | 0.99962 |
| MOPP | 0.99938 |
| MONN | 0.99962 |
| MONP | 0.99938 |
| MDQP | 0.99962 |
| MDQN | 0.99962 |
| MDDP | 0.98519 |
| MDDN | 0.98767 |
| MCKN | 0.99506 |
| MCKP | 0.99000 |
| MBLEED | 0.99506 |
| MUP | 0.99506 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.
