# BUFFER-V14: earlier interstage PMOS drive

B13's formal hot-corner noise fails, worst FS/low/125 at 488.025278 uV rms. The matched phase diagnosis reproduces 11/256 wrong decisions there versus 0/256 at TT, with all resets complete and stable early-to-final output signs. Existing noiseless waveforms show that DP differential transfer decays much earlier in the worst corner; at rise +30 ps its DP and XP secant gains are -2.074 and +6.685, versus TT -4.670 and +12.142. At +40 ps RP gain is +7.313 versus +27.947. The short noisy traces show the same ordering, and all 11 final errors are already present in RP-RN by +50 ps. [The diagnosis](NOISE-DIAGNOSIS-B13.md) preserves the observations and their limits.

This source changes only M14/M15, the PMOS drivers of XP/XN, from 4 um to 6 um at 30 nm with six fingers. It tests whether stronger earlier interstage drive transfers the input difference before it collapses and raises the signal entering regeneration. This is a measured hypothesis, not a proven noise attribution. Process, supply and temperature change together in the observed corner comparison. Reset-branch drain currents include displacement current, so those readings do not isolate channel contention or device noise.

Both complete geometries exactly reuse callback-validated MBPP geometry already present in B13; the successful zero-warning P6 callback has SHA-256 `ee1af01575dbb9dca5e57360e27ca64af62b4cb710b8533d97eb97d35838257d`. Every other electrical statement is unchanged, including all nine physical MOM capacitors, reset devices and output interface. The circuit still has 43 MOS and 9 MOMs. Electrical SHA-256: `1891c70233cdcacfe43d343f5388e0aaa791bdce7fc22ea7f23561c6789f887a`. Full RNL is checked and rendered on a byte-identical mirror of [BUFFER-V14.txt](BUFFER-V14.txt).

Extra gate and diffusion capacitance, switching current, reset behavior and edge stress must be measured. SF/high/-40 and FS/high/-40 come first. If they pass, TT and FS/low/125 deterministic gates precede the matched TT/worst-corner noise diagnosis, so the known worst noise corner is screened early. Remaining known corners, actual-worst convergence, canonical promotion and genuine original formal tests remain prerequisites. No B13 performance result transfers and canonical B13 with all formal failures remains preserved.

![Physical comparator with larger interstage PMOS drivers](https://raw.githubusercontent.com/many-question/ADC-12b-100M/1c82358bd327c795fc38a0b3ac1e63faf73429e5/design/xtor/adc_comp/many-question-miyahara/buffer-v14.png)

## Completed screen 20261031-080818-miyahara-buffer-v14-screen

FS/high/-40 fails six terminal-stress pairs at BP/BN; the actual raw BN maximum is 1.000091633924 V at rise+23.997853 ps. SF/high/-40 remains below 1 V at 0.99991 V. All 72 actual polarities and resets, output validity and timing checks pass, but the stress failure stops B14 before TT/noise and all further qualification. The next source tests buffer-node edge storage.

Actual clean source commit: `fe173f9df274e8fa4fdddfbdb14f20208dc441fb`. Electrical SHA-256: `1891c70233cdcacfe43d343f5388e0aaa791bdce7fc22ea7f23561c6789f887a`. The canonical netlist and 282 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fs_high_m40 | 50.254902 / 41.430173 | 20.780785 | 743.253214 | 36 / 36 | 0 | 0 | 1.00009 | 6 / 129 |
| sf_high_m40 | 54.556190 / 44.801929 | 21.445290 | 799.981756 | 36 / 36 | 0 | 0 | 0.99991 | 0 / 129 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | fs_high_m40 | sf_high_m40 |
|---|---:|---:|
| MINP | 0.70380 | 0.76899 |
| MINN | 0.70391 | 0.76917 |
| MTAIL | 0.99000 | 0.99000 |
| M14 | 0.99304 | 0.99194 |
| M15 | 0.99304 | 0.99194 |
| M12 | 0.99294 | 0.99294 |
| M13 | 0.99294 | 0.99294 |
| M10 | 0.98686 | 0.98182 |
| M11 | 0.98686 | 0.98182 |
| M6 | 0.99419 | 0.99511 |
| M7 | 0.99419 | 0.99511 |
| M8 | 0.99419 | 0.99511 |
| M9 | 0.99419 | 0.99511 |
| MCKN | 0.99000 | 0.99151 |
| MCKP | 0.99000 | 0.99000 |
| MRQP | 0.99419 | 0.99511 |
| MRQN | 0.99419 | 0.99511 |
| MAP | 0.99304 | 0.99194 |
| MAN | 0.99304 | 0.99194 |
| MBPP | 0.98772 | 0.98281 |
| MBPN | 1.00009 | 0.99991 |
| MOPP | 0.98816 | 0.97944 |
| MOPN | 1.00009 | 0.99991 |
| MBNP | 0.98772 | 0.98278 |
| MBNN | 1.00009 | 0.99991 |
| MONP | 0.98816 | 0.97944 |
| MONN | 1.00009 | 0.99991 |
| MDDP | 0.98425 | 0.98640 |
| MDDN | 0.98703 | 0.98796 |
| MUPRP1 | 0.99419 | 0.99511 |
| MUPRN1 | 0.99419 | 0.99511 |
| MUPBP1 | 1.00009 | 0.99991 |
| MUPBN1 | 1.00009 | 0.99991 |
| MUPOUTP1 | 0.99000 | 0.99233 |
| MUPOUTN1 | 0.99000 | 0.99233 |
| MDNOUTP1 | 0.98800 | 0.99233 |
| MDNOUTP2 | 0.98800 | 0.99233 |
| MDNOUTN1 | 0.98800 | 0.99233 |
| MDNOUTN2 | 0.98800 | 0.99233 |
| MCKUP | 0.99000 | 0.99151 |
| MBLEED | 0.99000 | 0.99151 |
| MUPXP | 0.99222 | 0.99294 |
| MUPXN | 0.99222 | 0.99294 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.
