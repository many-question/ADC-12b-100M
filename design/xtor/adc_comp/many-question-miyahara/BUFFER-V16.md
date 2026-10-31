# BUFFER-V16: test regeneration reset-assist loading

> Evidence retention (2026-10-31): Superseded raw was released. Historical verification does not imply current availability; [retained evidence](EVIDENCE-RETENTION.md) determines which runs can be re-audited.

B15's paired short diagnosis has 0/256 wrong polarities at TT and 6/256 at FS/low/125, with complete reset, no later interface sign changes and no full-trace stress violation. The FS result is improved from B13's 11/256 in this finite sample, but does not establish the 240 uV requirement. All six errors are already present in RP-RN at +50 ps, which agrees with every final decision. B15 remains unpromoted, including its separate 13.345 uV cold high-voltage stress-margin concern.

The FS input difference remains correct for every sample at +20 and +30 ps, while later transfer loses discrimination. At +30 ps B15's two-level DP/XP/RP descriptive SNR values are 3.561/2.578/1.253. At +40 ps RP gain/SNR is 12.734/2.266, versus B13 7.557/1.852. Stronger interstage drive improved early transfer but residual errors remain; B13 to B15 also changed buffer capacitors, so it is not a one-variable causal comparison.

At +30 ps, normalized CKB remains about 0.14467 VDD and RP is about 0.06063 VDD. The observed MRQP drain current averages 47.3505 uA, with the weak RP PMOS at -100.0087 uA. These terminal currents include displacement and do not isolate channel contention or a device noise contribution. They motivate a controlled reset-assist geometry test rather than proving that the reset transistor causes all residual noise.

Only MRQP/MRQN change from 4 um/30 nm/nf4 to 2 um/30 nm/nf2. The geometry is exactly the existing M6 device and every parameter matches a successful zero-warning callback, SHA-256 `d899f4fdf621dad61d7ca1a5c55d8f8022b122be5a201a46befb1154bb160c86`. All other 41 MOS devices and all nine MOMs remain identical. This reduces reset-assist drive and loading, including CKB gate load; possible benefits to release timing and possible costs in reset speed, validity and voltage excursion must all be measured.

Electrical SHA-256: `dbec21e70ed9aaf442210a58df360b115215013bcf1b60301347e306f0e8dffd`. The [source](BUFFER-V16.txt) contains 43 MOS and 9 MOMs with complete RNL checked on a byte-identical mirror. First SF/high/-40 and FS/high/-40 screens are followed, only if useful, by TT and the known worst FS/low/125 corner and their matched short phase diagnosis. Full known-corner coverage, actual-worst convergence and genuine formal tests remain open. Canonical B13 and every genuine formal failure remain unchanged.

![Physical comparator with smaller regeneration reset assists](https://raw.githubusercontent.com/many-question/ADC-12b-100M/1c82358bd327c795fc38a0b3ac1e63faf73429e5/design/xtor/adc_comp/many-question-miyahara/buffer-v16.png)

## Completed screen 20261031-090356-miyahara-buffer-v16-screen

B16 fails the strict 1 V terminal-stress limit in FS/high/-40, with six failing terminal pairs. All 72 actual polarities including 10 uV, all resets and physical output-validity checks pass, but they do not override the stress failure. This source stops before TT, remaining corners or noise expansion.

Actual clean source commit: `0c799462e700c1f74a9448031e14abdd56ec18e7`. Electrical SHA-256: `dbec21e70ed9aaf442210a58df360b115215013bcf1b60301347e306f0e8dffd`. The canonical netlist and 282 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fs_high_m40 | 50.104406 / 41.543622 | 27.420507 | 731.942029 | 36 / 36 | 0 | 0 | 1.00003 | 6 / 129 |
| sf_high_m40 | 54.400128 / 44.887355 | 27.938615 | 788.032719 | 36 / 36 | 0 | 0 | 0.99997 | 0 / 129 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | fs_high_m40 | sf_high_m40 |
|---|---:|---:|
| MINP | 0.70381 | 0.76901 |
| MINN | 0.70392 | 0.76919 |
| MTAIL | 0.99000 | 0.99000 |
| M14 | 0.99304 | 0.99194 |
| M15 | 0.99304 | 0.99194 |
| M12 | 0.99294 | 0.99389 |
| M13 | 0.99294 | 0.99389 |
| M10 | 0.98513 | 0.98038 |
| M11 | 0.98513 | 0.98038 |
| M6 | 0.99450 | 0.99514 |
| M7 | 0.99450 | 0.99514 |
| M8 | 0.99450 | 0.99514 |
| M9 | 0.99450 | 0.99514 |
| MCKN | 0.99000 | 0.99197 |
| MCKP | 0.99000 | 0.99000 |
| MRQP | 0.99450 | 0.99514 |
| MRQN | 0.99450 | 0.99514 |
| MAP | 0.99304 | 0.99194 |
| MAN | 0.99304 | 0.99194 |
| MBPP | 0.98426 | 0.98299 |
| MBPN | 1.00003 | 0.99997 |
| MOPP | 0.98764 | 0.97918 |
| MOPN | 1.00003 | 0.99997 |
| MBNP | 0.98426 | 0.98299 |
| MBNN | 1.00002 | 0.99997 |
| MONP | 0.98764 | 0.97918 |
| MONN | 1.00002 | 0.99997 |
| MDDP | 0.98425 | 0.98640 |
| MDDN | 0.98703 | 0.98796 |
| MUPRP1 | 0.99450 | 0.99514 |
| MUPRN1 | 0.99450 | 0.99514 |
| MUPBP1 | 1.00003 | 0.99997 |
| MUPBN1 | 1.00002 | 0.99997 |
| MUPOUTP1 | 0.99000 | 0.99047 |
| MUPOUTN1 | 0.99000 | 0.99047 |
| MDNOUTP1 | 0.98500 | 0.99047 |
| MDNOUTP2 | 0.98500 | 0.99047 |
| MDNOUTN1 | 0.98500 | 0.99047 |
| MDNOUTN2 | 0.98500 | 0.99047 |
| MCKUP | 0.99000 | 0.99197 |
| MBLEED | 0.99000 | 0.99197 |
| MUPXP | 0.99246 | 0.99389 |
| MUPXN | 0.99246 | 0.99389 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.


The raw BP maximum is **1.000025374154 V**, exceeding the limit by 25.374153936 uV, at 7328.711696158 ps (23.711696158 ps after the nearest rising 50% clock crossing). At that point CLKC is 0.990000000 V and CKB is 0.097217076948 V. The separate BN maximum is 1.000022407242 V at 7728.792381276 ps. These are unrounded waveform extrema; the public summary rounds the maximum to 1.00003 V. The strict failure is retained without a rounding exception.

Compared with B15 at the same corners, FS reset slows by 6.438096701 ps and SF reset by 6.340871069 ps. B16 changes reset strength and capacitance together; this experiment does not establish a channel-noise cause. The next independent test branches from B15, retaining N4 reset assists while changing only the clock inverter pull-down geometry.

The full AVDD waveform integral includes all 36 cycles, the same 100 ps–14.5 ns window, physical reset and weak rail loads. External ideal clock delivery remains outside this boundary. All saved device terminal probes are present and their supply-current sum closes to numerical precision:

| Corner | Total fJ/cycle | Evaluation | Reset | Initial reset current uA |
|---|---:|---:|---:|---:|
| fs_high_m40 | 731.942477171 | 276.173964617 | 455.768512554 | 1491.520619332 |
| sf_high_m40 | 788.033042717 | 307.939523575 | 480.093519142 | 1658.632028138 |

Every archived member was read back with CRC and SHA-256 verification before local raw duplicates were removed. Archive SHA-256: `c03ced16e3c7b672064e0b70b8caf1db014ee93044a80c5053175166ba414ead`. Canonical B13 and all 96 original result records are unchanged. No formal qualification is inferred.
