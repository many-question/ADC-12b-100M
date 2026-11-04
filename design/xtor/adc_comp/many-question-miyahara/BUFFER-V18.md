# BUFFER-V18: test stronger input-to-XP/XN drivers

> Superseded raw was released. Historical audits do not imply availability; see [retained runs](EVIDENCE-RETENTION.md).

B17 passes four initial deterministic corners and improves cold high-voltage stress margin, but its matched short FS/low/125 diagnosis retains four errors out of 256. Changing only clock pull-down reduces mean CKB/VDD at +30 ps from 0.144669 to 0.025470; FS RP SNR at +40 ps nevertheless increases only about 1.09%. DP signs at +20/+30 ps remain correct for every sample, while RP-RN at +50 ps already contains all four final errors. [BUFFER-V17.md](BUFFER-V17.md) preserves the full result and stopped broader expansion; no formal noise pass is claimed.

This experiment branches electrically from B17. Only M14/M15, the PMOS devices driven by DP/DN and supplying XP/XN, change from 6 um/30 nm/nf6 to 8 um/30 nm/nf8. Length and 1 um finger width remain fixed; total width and finger count both increase. A new successful zero-warning P8 callback supplies full geometry and parasitics, SHA-256 `20855415d9559ad00227138e98d1e759f6c67857f07cd4c5123d67502d0fec87`. All other 41 MOS devices and all nine MOMs are identical to B17, including its N2 clock pull-down, N4 regeneration reset assists and 20-finger BP/BN capacitors.

The hypothesis is that stronger DP/DN-controlled pull-up can change earlier XP/XN and RP/RN transfer while retaining the improved clock trajectory. Geometry also changes input-drain loading, capacitance, current and noise, so no isolated transconductance or device-noise benefit is assumed. The earlier P6 experiment exposed buffer-node stress, making SF/high/-40 and FS/high/-40 the first checks again. TT and the known worst FS/low/125 follow only on a useful pass, then matched short phase diagnosis before wider qualification.

Electrical SHA-256: `188a1104b165095a8732e55525b0cd62f381715785475a525b45a13dfb50b654`. The [source](BUFFER-V18.txt) contains 43 MOS and 9 MOMs with complete RNL checked on a byte-identical mirror. Remaining known corners, actual-worst numerical convergence, source-preserving canonical promotion and genuine formal tests remain open. Canonical B13 and every original formal failure remain unchanged.

![Physical comparator with stronger DP/DN-controlled PMOS drivers](https://raw.githubusercontent.com/many-question/ADC-12b-100M/fc05ec9b504909d82e993df12fa475fd234cba5b/design/xtor/adc_comp/many-question-miyahara/buffer-v18.png)

## Completed screen 20261031-095133-miyahara-buffer-v18-screen

Both initial high-voltage cold corners fail six terminal pairs at the strict 1 V limit. All 72 actual polarities including 10 uV, resets and physical output-validity checks pass, but do not override the stress failures. B18 stops before TT, noise and further-corner expansion.

Actual clean source commit: `cbf931b4f58fc6928096110a1c99c9656c04c3ad`. Electrical SHA-256: `188a1104b165095a8732e55525b0cd62f381715785475a525b45a13dfb50b654`. The canonical netlist and 282 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fs_high_m40 | 49.757254 / 41.171691 | 21.742600 | 754.741764 | 36 / 36 | 0 | 0 | 1.00027 | 6 / 129 |
| sf_high_m40 | 54.115067 / 44.516252 | 22.543690 | 812.226852 | 36 / 36 | 0 | 0 | 1.00015 | 6 / 129 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | fs_high_m40 | sf_high_m40 |
|---|---:|---:|
| MINP | 0.70397 | 0.76922 |
| MINN | 0.70408 | 0.76939 |
| MTAIL | 0.99000 | 0.99000 |
| M14 | 0.99299 | 0.99187 |
| M15 | 0.99299 | 0.99187 |
| M12 | 0.99290 | 0.99330 |
| M13 | 0.99290 | 0.99330 |
| M10 | 0.98712 | 0.98220 |
| M11 | 0.98712 | 0.98220 |
| M6 | 0.99468 | 0.99495 |
| M7 | 0.99468 | 0.99495 |
| M8 | 0.99468 | 0.99495 |
| M9 | 0.99468 | 0.99495 |
| MCKN | 0.99000 | 0.99202 |
| MCKP | 0.99000 | 0.99000 |
| MRQP | 0.99468 | 0.99495 |
| MRQN | 0.99468 | 0.99495 |
| MAP | 0.99299 | 0.99187 |
| MAN | 0.99299 | 0.99187 |
| MBPP | 0.98878 | 0.98528 |
| MBPN | 1.00027 | 1.00014 |
| MOPP | 0.98794 | 0.97936 |
| MOPN | 1.00027 | 1.00014 |
| MBNP | 0.98876 | 0.98524 |
| MBNN | 1.00027 | 1.00015 |
| MONP | 0.98793 | 0.97935 |
| MONN | 1.00027 | 1.00015 |
| MDDP | 0.98421 | 0.98632 |
| MDDN | 0.98697 | 0.98792 |
| MUPRP1 | 0.99468 | 0.99495 |
| MUPRN1 | 0.99468 | 0.99495 |
| MUPBP1 | 1.00027 | 1.00014 |
| MUPBN1 | 1.00027 | 1.00015 |
| MUPOUTP1 | 0.99000 | 0.99115 |
| MUPOUTN1 | 0.99000 | 0.99115 |
| MDNOUTP1 | 0.98698 | 0.99115 |
| MDNOUTP2 | 0.98698 | 0.99115 |
| MDNOUTN1 | 0.98698 | 0.99115 |
| MDNOUTN2 | 0.98698 | 0.99115 |
| MCKUP | 0.99000 | 0.99202 |
| MBLEED | 0.99000 | 0.99202 |
| MUPXP | 0.99247 | 0.99330 |
| MUPXN | 0.99247 | 0.99330 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.


The following are unrounded raw buffer-node maxima, measured after rising clock midpoints:

| Corner | Node | Peak V | Time ps | Since rise ps | CLKC V | CKB V |
|---|---|---:|---:|---:|---:|---:|
| fs_high_m40 | BP | 1.000268183992 | 7328.486867899 | 23.486867899 | 0.990000000 | 0.028951747338 |
| fs_high_m40 | BN | 1.000274971668 | 7728.619010043 | 23.619010043 | 0.990000000 | 0.028961679656 |
| sf_high_m40 | BP | 1.000142918332 | 7330.784743409 | 25.784743409 | 0.990000000 | 0.037750994075 |
| sf_high_m40 | BN | 1.000148479010 | 7730.826756207 | 25.826756207 | 0.990000000 | 0.037648491153 |

The worst BN peak exceeds 1 V by 274.971668 uV. The next source retains the P8 interstage drivers and N2 clock pull-down, changing only CBP/CBN from 20 to 40 fingers. Its additional delay and reset charge require new measurements, particularly at low voltage and high temperature. No P8 noise benefit has yet been demonstrated.

Full AVDD integrals use the same 36 cycles and 100 ps–14.5 ns window, including physical reset and weak rail loads. Every supply probe is present and KCL closes; ideal external-clock delivery remains outside this boundary.

| Corner | Total fJ/cycle | Evaluation | Reset | Initial reset current uA |
|---|---:|---:|---:|---:|
| fs_high_m40 | 754.742162298 | 282.047133846 | 472.695028452 | 1491.776783064 |
| sf_high_m40 | 812.227212017 | 314.837593050 | 497.389618967 | 1659.186143996 |

Archive SHA-256: `5fd0e1881ee471b59b6b06163bb1d8e35768ce28f051b7d17b829c32e59eb327`. Every member was read back with CRC and SHA-256 verification before duplicate local raw data were removed; the owned remote run is absent. Power is reported only. Canonical B13 and all 96 genuine result records remain unchanged.
