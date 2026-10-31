# BUFFER-V17: test earlier physical clock release

B15 retains six wrong polarities in the paired FS/low/125 short diagnosis. B16 then reduced the two regeneration reset assists from N4 to N2. It fails the first FS/high/-40 stress screen at a raw BP peak of 1.000025374154 V and slows reset by 6.438097 ps relative to B15. B16 therefore stops before TT or noise expansion. Its measured failure is preserved in [BUFFER-V16.md](BUFFER-V16.md).

This experiment branches electrically from B15. Only the physical clock inverter NMOS MCKN changes from 1 um/30 nm/nf1 to 2 um/30 nm/nf2. The two regeneration reset assists retain their B15 N4 geometry. All other 42 MOS devices and all nine MOMs remain identical to B15, including the 20-finger BP/BN capacitors and 48-finger CKB capacitor. This tests faster CKB release while retaining reset strength. It does not assume that B16 isolated channel noise: changed geometry also changes capacitance and the clock trajectory.

The new geometry exactly matches existing M6 and every numerical parameter agrees with the successful zero-warning N2 callback, SHA-256 `d899f4fdf621dad61d7ca1a5c55d8f8022b122be5a201a46befb1154bb160c86`. This is reuse of that checked callback and existing geometry; no new callback execution is claimed. Possible clock undershoot, output-buffer overshoot, reset degradation and increased clock capacitance must be measured.

Electrical SHA-256: `f746984dca9a8b27c38058b15ad679b845a933f70653275d4fd187a41aa7be70`. The [source](BUFFER-V17.txt) contains 43 MOS and 9 MOMs with complete RNL checked on a byte-identical mirror. SF/high/-40 and FS/high/-40 are screened first, followed only on a useful pass by TT and the known worst FS/low/125 corner and a matched short phase diagnosis. Full known-corner coverage, actual-worst numerical convergence, canonical promotion and genuine formal tests remain open. Canonical B13 and every original formal failure remain unchanged.

![Physical comparator with stronger clock pull-down](buffer-v17.png)

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
