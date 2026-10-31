# BUFFER-V17: test earlier physical clock release

> Evidence retention (2026-10-31): Superseded raw was released. Historical verification does not imply current availability; [retained evidence](EVIDENCE-RETENTION.md) determines which runs can be re-audited.

B15 retains six wrong polarities in the paired FS/low/125 short diagnosis. B16 then reduced the two regeneration reset assists from N4 to N2. It fails the first FS/high/-40 stress screen at a raw BP peak of 1.000025374154 V and slows reset by 6.438097 ps relative to B15. B16 therefore stops before TT or noise expansion. Its measured failure is preserved in [BUFFER-V16.md](BUFFER-V16.md).

This experiment branches electrically from B15. Only the physical clock inverter NMOS MCKN changes from 1 um/30 nm/nf1 to 2 um/30 nm/nf2. The two regeneration reset assists retain their B15 N4 geometry. All other 42 MOS devices and all nine MOMs remain identical to B15, including the 20-finger BP/BN capacitors and 48-finger CKB capacitor. This tests faster CKB release while retaining reset strength. It does not assume that B16 isolated channel noise: changed geometry also changes capacitance and the clock trajectory.

The new geometry exactly matches existing M6 and every numerical parameter agrees with the successful zero-warning N2 callback, SHA-256 `d899f4fdf621dad61d7ca1a5c55d8f8022b122be5a201a46befb1154bb160c86`. This is reuse of that checked callback and existing geometry; no new callback execution is claimed. Possible clock undershoot, output-buffer overshoot, reset degradation and increased clock capacitance must be measured.

Electrical SHA-256: `f746984dca9a8b27c38058b15ad679b845a933f70653275d4fd187a41aa7be70`. The [source](BUFFER-V17.txt) contains 43 MOS and 9 MOMs with complete RNL checked on a byte-identical mirror. SF/high/-40 and FS/high/-40 are screened first, followed only on a useful pass by TT and the known worst FS/low/125 corner and a matched short phase diagnosis. Full known-corner coverage, actual-worst numerical convergence, canonical promotion and genuine formal tests remain open. Canonical B13 and every original formal failure remain unchanged.

![Physical comparator with stronger clock pull-down](https://raw.githubusercontent.com/many-question/ADC-12b-100M/1c82358bd327c795fc38a0b3ac1e63faf73429e5/design/xtor/adc_comp/many-question-miyahara/buffer-v17.png)

## Completed screen 20261031-091848-miyahara-buffer-v17-screen

Both tested corners pass all 72 actual polarities including 10 uV, all 72 resets, timing, physical output validity and every one of 129 MOS terminal pairs. These private deterministic observations do not establish noise qualification.

Actual clean source commit: `2cc9aff4544f5073f6e4f479687e85e6f426d756`. Electrical SHA-256: `f746984dca9a8b27c38058b15ad679b845a933f70653275d4fd187a41aa7be70`. The canonical netlist and 282 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fs_high_m40 | 50.616524 / 41.782495 | 21.245274 | 744.528061 | 36 / 36 | 0 | 0 | 0.99967 | 0 / 129 |
| sf_high_m40 | 54.905999 / 45.142324 | 21.895480 | 801.594671 | 36 / 36 | 0 | 0 | 0.99967 | 0 / 129 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | fs_high_m40 | sf_high_m40 |
|---|---:|---:|
| MINP | 0.70376 | 0.76899 |
| MINN | 0.70388 | 0.76917 |
| MTAIL | 0.99000 | 0.99000 |
| M14 | 0.99304 | 0.99194 |
| M15 | 0.99304 | 0.99194 |
| M12 | 0.99294 | 0.99333 |
| M13 | 0.99294 | 0.99333 |
| M10 | 0.98685 | 0.98186 |
| M11 | 0.98685 | 0.98186 |
| M6 | 0.99416 | 0.99515 |
| M7 | 0.99416 | 0.99515 |
| M8 | 0.99416 | 0.99515 |
| M9 | 0.99416 | 0.99515 |
| MCKN | 0.99000 | 0.99202 |
| MCKP | 0.99000 | 0.99000 |
| MRQP | 0.99416 | 0.99515 |
| MRQN | 0.99416 | 0.99515 |
| MAP | 0.99304 | 0.99194 |
| MAN | 0.99304 | 0.99194 |
| MBPP | 0.98880 | 0.98528 |
| MBPN | 0.99967 | 0.99967 |
| MOPP | 0.98744 | 0.97894 |
| MOPN | 0.99967 | 0.99967 |
| MBNP | 0.98877 | 0.98525 |
| MBNN | 0.99966 | 0.99967 |
| MONP | 0.98743 | 0.97893 |
| MONN | 0.99966 | 0.99967 |
| MDDP | 0.98425 | 0.98639 |
| MDDN | 0.98703 | 0.98796 |
| MUPRP1 | 0.99416 | 0.99515 |
| MUPRN1 | 0.99416 | 0.99515 |
| MUPBP1 | 0.99967 | 0.99967 |
| MUPBN1 | 0.99966 | 0.99967 |
| MUPOUTP1 | 0.99000 | 0.99216 |
| MUPOUTN1 | 0.99000 | 0.99216 |
| MDNOUTP1 | 0.98771 | 0.99216 |
| MDNOUTP2 | 0.98771 | 0.99216 |
| MDNOUTN1 | 0.98771 | 0.99216 |
| MDNOUTN2 | 0.98771 | 0.99216 |
| MCKUP | 0.99000 | 0.99202 |
| MBLEED | 0.99000 | 0.99202 |
| MUPXP | 0.99265 | 0.99333 |
| MUPXN | 0.99265 | 0.99333 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.

## Completed screen 20261031-092615-miyahara-buffer-v17-screen

Both tested corners pass all 72 actual polarities including 10 uV, all 72 resets, timing, physical output validity and every one of 129 MOS terminal pairs. These private deterministic observations do not establish noise qualification.

Actual clean source commit: `2cc9aff4544f5073f6e4f479687e85e6f426d756`. Electrical SHA-256: `f746984dca9a8b27c38058b15ad679b845a933f70653275d4fd187a41aa7be70`. The canonical netlist and 282 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fs_low_125 | 68.583527 / 52.995069 | 26.472453 | 448.177377 | 36 / 36 | 0 | 0 | 0.81214 | 0 / 129 |
| tt_nom_27 | 57.481557 / 46.561764 | 24.274297 | 573.231882 | 36 / 36 | 0 | 0 | 0.90844 | 0 / 129 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | fs_low_125 | tt_nom_27 |
|---|---:|---:|
| MINP | 0.54155 | 0.60584 |
| MINN | 0.54155 | 0.60591 |
| MTAIL | 0.81000 | 0.90000 |
| M14 | 0.81121 | 0.90190 |
| M15 | 0.81121 | 0.90190 |
| M12 | 0.81085 | 0.90223 |
| M13 | 0.81134 | 0.90223 |
| M10 | 0.80006 | 0.89286 |
| M11 | 0.80006 | 0.89286 |
| M6 | 0.80056 | 0.90286 |
| M7 | 0.80056 | 0.90286 |
| M8 | 0.80796 | 0.90286 |
| M9 | 0.81134 | 0.90286 |
| MCKN | 0.81000 | 0.90167 |
| MCKP | 0.81000 | 0.90000 |
| MRQP | 0.80788 | 0.90286 |
| MRQN | 0.80788 | 0.90286 |
| MAP | 0.81121 | 0.90190 |
| MAN | 0.81134 | 0.90190 |
| MBPP | 0.81043 | 0.89784 |
| MBPN | 0.81214 | 0.90844 |
| MOPP | 0.80351 | 0.89335 |
| MOPN | 0.81214 | 0.90844 |
| MBNP | 0.81042 | 0.89781 |
| MBNN | 0.81213 | 0.90844 |
| MONP | 0.80351 | 0.89336 |
| MONN | 0.81213 | 0.90844 |
| MDDP | 0.80796 | 0.89764 |
| MDDN | 0.81134 | 0.90045 |
| MUPRP1 | 0.81043 | 0.90286 |
| MUPRN1 | 0.81042 | 0.90286 |
| MUPBP1 | 0.81214 | 0.90844 |
| MUPBN1 | 0.81213 | 0.90844 |
| MUPOUTP1 | 0.81000 | 0.90000 |
| MUPOUTN1 | 0.81000 | 0.90000 |
| MDNOUTP1 | 0.80252 | 0.89980 |
| MDNOUTP2 | 0.80252 | 0.89980 |
| MDNOUTN1 | 0.80252 | 0.89980 |
| MDNOUTN2 | 0.80252 | 0.89980 |
| MCKUP | 0.81000 | 0.90167 |
| MBLEED | 0.81000 | 0.90167 |
| MUPXP | 0.81085 | 0.90223 |
| MUPXN | 0.81085 | 0.90223 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.


All four initial corners pass 144 actual polarities and resets. TT 1/30 mV delay is 57.481557432/46.561764212 ps; reset is 24.274296669 ps. Mixed-sequence clock capacitance is 10.441402692 fF, a diagnostic rather than the original formal CMP-14 result. The next step is the matched short TT and known-worst FS/low/125 phase diagnosis. The six remaining known keys and actual-worst tight integration remain open; no canonical promotion or formal noise pass is inferred.

Raw evidence archives, with every member read back for CRC and SHA-256 verification:

- `20261031-091848-miyahara-buffer-v17-screen`: `0b545959578e8a0be6759deb0f15c6bd6216cad7a636daa3094cdf2d82227448`.
- `20261031-092615-miyahara-buffer-v17-screen`: `975e6b2ab2ea82da40382868cc8fee07a37e5ce3a82b201f978fa476cdd7ea5c`.

## Matched TT and worst-corner noise phase diagnosis

Run `20261031-093304-miyahara-buffer-v17-noise-phase-diagnostic-screen` uses clean source `14071b8f720a24f44b0f60ba25cbc7d79c296f8d`, electrical SHA-256 `f746984dca9a8b27c38058b15ad679b845a933f70653275d4fd187a41aa7be70`. Both corners retain B15's +/-800 uV, 128 decisions per level, 50 GHz bandwidth, seed 1, 0.5 ps / 1e-6 / 1e-8 integration, 10 fF load and VCM 0.49 V. The testbench hash and complete short protocol match; the source changes only the clock pull-down geometry.

| Corner | OUTP at -800 / +800 uV | Wrong / 256 | Reset max ps | Max MOS stress V |
|---|---:|---:|---:|---:|
| tt_nom_27 | 0 / 128 | 0 | 24.184547965 | 0.90522 |
| fs_low_125 | 3 / 127 | 4 | 26.559492165 | 0.81177 |

All 256 resets complete at each corner, with no +80/+150 ps-to-final sign changes, late-reset, output-validity or full-trace stress violations. All 129 terminal pairs are checked. The four FS errors occur at cycles 10, 58, 70 and 157; every sample is retained. At +50 ps RP-RN has those same four errors and matches every final decision. DP signs at +20/+30 ps remain correct for every cycle, including all four final errors. This does not rule out earlier coupled interface contributions.

B15 had 0/256 TT and 6/256 FS errors. The finite-count change does not establish a formal noise improvement, and the same seed does not make nonlinear waveforms independent trials. Gains below are two-level secants; SNR is the mean of each level’s absolute differential mean divided by its sample standard deviation. They are descriptive phase statistics, not input-referred noise.

| Phase and node | TT gain B15 / B17 | FS gain B15 / B17 | TT SNR B15 / B17 | FS SNR B15 / B17 |
|---|---:|---:|---:|---:|
| +20 ps DP_minus_DN | -3.506789 / -3.506717 | -2.956183 / -2.956662 | 4.014832 / 4.015654 | 3.194453 / 3.195179 |
| +30 ps DP_minus_DN | -4.553212 / -4.547374 | -2.249823 / -2.248842 | 4.945071 / 4.944207 | 3.561494 / 3.561315 |
| +30 ps XP_minus_XN | 11.979471 / 12.232638 | 6.881498 / 7.102307 | 3.869898 / 3.866597 | 2.577531 / 2.577334 |
| +30 ps RP_minus_RN | 2.020416 / 2.013317 | 1.441994 / 1.451648 | 1.990195 / 1.992883 | 1.252984 / 1.243384 |
| +40 ps RP_minus_RN | 40.142838 / 40.558436 | 12.734365 / 13.415482 | 4.390070 / 4.395448 | 2.265981 / 2.290627 |
| +50 ps RP_minus_RN | 322.821752 / 326.456393 | 59.577713 / 63.782637 | 4.675992 / 4.690828 | 2.198461 / 2.232008 |

At +30 ps the mean CKB/VDD changes from 0.132463067 to 0.028298909 at TT, and from 0.144668969 to 0.025469623 at FS/low/125. Despite this earlier release, FS RP SNR at +40 ps increases only 1.087671%. The input-drain statistics remain almost unchanged. The measured phase response does not support treating stronger clock pull-down alone as the noise repair.

| +30 ps drain-current mean uA | TT | FS low/hot |
|---|---:|---:|
| M14 | -514.884094 | -548.332717 |
| M12 | 212.179507 | 197.777129 |
| M10 | -97.338159 | -123.751927 |
| M8 | 161.234838 | 125.793318 |
| MRQP | 22.174081 | 25.486025 |
| MUPRP1 | -155.906528 | -99.966240 |

These terminal currents include displacement and do not isolate channel contention or device noise. B17 retains its improved cold high-voltage stress margin but remains unpromoted; further known-corner, tight-integration and formal expansion stops here. The next experiment retains B17’s clock and all capacitors, changing only M14/M15 from P6 to P8 to test the earlier DP-to-XP/XN transfer. Stress, timing and phase behavior must all be measured again.

| Device | TT maximum stress V | FS low/hot maximum stress V |
|---|---:|---:|
| MINP | 0.59554 | 0.49229 |
| MINN | 0.59590 | 0.49236 |
| MTAIL | 0.90017 | 0.81000 |
| M14 | 0.90238 | 0.81177 |
| M15 | 0.90234 | 0.81164 |
| M12 | 0.90274 | 0.81155 |
| M13 | 0.90269 | 0.81164 |
| M10 | 0.89330 | 0.80096 |
| M11 | 0.89331 | 0.80096 |
| M6 | 0.90344 | 0.80137 |
| M7 | 0.90344 | 0.80137 |
| M8 | 0.90344 | 0.80638 |
| M9 | 0.90333 | 0.80636 |
| MCKN | 0.90222 | 0.81000 |
| MCKP | 0.90000 | 0.81000 |
| MRQP | 0.90344 | 0.80857 |
| MRQN | 0.90333 | 0.80857 |
| MAP | 0.90238 | 0.81177 |
| MAN | 0.90226 | 0.81164 |
| MBPP | 0.89832 | 0.81082 |
| MBPN | 0.90522 | 0.81146 |
| MOPP | 0.89006 | 0.80040 |
| MOPN | 0.90522 | 0.81146 |
| MBNP | 0.89841 | 0.81093 |
| MBNN | 0.90509 | 0.81156 |
| MONP | 0.88953 | 0.79991 |
| MONN | 0.90509 | 0.81156 |
| MDDP | 0.89753 | 0.80638 |
| MDDN | 0.89750 | 0.80636 |
| MUPRP1 | 0.90344 | 0.81082 |
| MUPRN1 | 0.90333 | 0.81093 |
| MUPBP1 | 0.90522 | 0.81146 |
| MUPBN1 | 0.90509 | 0.81156 |
| MUPOUTP1 | 0.90039 | 0.81000 |
| MUPOUTN1 | 0.90029 | 0.81000 |
| MDNOUTP1 | 0.90039 | 0.80331 |
| MDNOUTP2 | 0.90039 | 0.80331 |
| MDNOUTN1 | 0.90029 | 0.80322 |
| MDNOUTN2 | 0.90029 | 0.80322 |
| MCKUP | 0.90222 | 0.81000 |
| MBLEED | 0.90222 | 0.81000 |
| MUPXP | 0.90274 | 0.81155 |
| MUPXN | 0.90269 | 0.81164 |

Archive SHA-256 `a98acf86b0630eb1bef7bc340248ede683d5b6be9dda03e83de106608da0baf5` preserves all raw evidence, full phase comparison and actual error indices. Every member is verified by read-back CRC and SHA-256; the owned remote run is absent. The 102.5 ns run has noisefmin about 9.7561 MHz rather than the original 287.216 kHz, and read-only samplers add time points. This is not a formal noise result. Canonical B13 and all genuine original records, including its four formal failures, remain unchanged.
