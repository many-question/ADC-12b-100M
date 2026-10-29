# StrongARM comparator

WIP transistor candidate in 28 nm HPC+. The frozen source is revision `p56t3c1`. Fast-corner device voltages exceed 1.0 V and some slow corners fail reset, so the candidate remains unqualified.

The single-stage StrongARM core follows [Razavi, Fig. 1(b)](https://www.seas.ucla.edu/brweb/papers/Journals/BR_Magzine4.pdf). A CMOS inverter on each internal output provides the required return-to-zero interface: INP > INN discharges QP and asserts OUTP. Both external outputs reset low. The two output loads remain 10 fF each.

Input-drain precharge uses two series PMOS per side, controlled by CLKC and its locally delayed copy CKD. Output-node precharge uses two parallel PMOS per side with the same controls. This releases input-drain precharge first during evaluation and establishes output-node precharge first during reset. This reduces some earlier edge-coupling problems, but it does not eliminate all voltage violations. The clock generator is two CMOS inverters. There is no extra gain stage. The complete candidate contains 23 MOS devices and four permitted MOM capacitors.

Each input NMOS is 56 um / 30 nm with 56 fingers. The tail is 3 um and the regenerative NMOS/PMOS pairs are 12/8 um. Each input drain has 14.06 fF nominal MOM capacitance to ground; CKB and CKD each have a 4.46051 fF nominal MOM device. Device dimensions, parasitics and capacitor geometries come from successful callbacks; the actual permitted device models are simulated.

The comparison with Miyahara uses the same excitation, output loads, transient-noise bandwidth and seed. AVDD energy includes all local clock and output devices. `C_CLKC * VDD^2` is reported separately as an external clock-driver charge-energy estimate, not an exact system energy measurement. A lower-energy failing version is not a qualified winner.

Earlier variants expose a tradeoff between noise, delay, energy and edge-coupled voltage stress. The `k56t3c2` pilot reaches 159.0 uV rms and 195.3 fJ but misses the TT 30 mV delay limit and reaches 1.03741 V at ff/high/125. Larger common-clock precharge devices reach 144.6 uV rms but exceed 200 fJ and increase fast-cold overshoot to 1.08620 V. These are measurements of different frozen exploratory circuits, not evidence for the current source. [CHARACTERIZATION.md](CHARACTERIZATION.md) retains every completed experiment, including failures and hashes.

Official TT results are 187.11 uV rms (95% interval 179.33–195.28 uV), 56.94/44.92 ps at 1/30 mV, 28.90 ps reset, 19.313 fF per input, 15.156 fF at CLKC and 0.387 uV differential kickback. The 50-sample local-mismatch run has 50/50 valid samples, 0 failures and 1.898 mV sample standard deviation. These records use the standard 17 x 512 noise test and seed 6303 for mismatch. [VERIFICATION.md](VERIFICATION.md) gives the source commits, result coverage and all recorded failures.

Delay and kickback each cover 45/45 corners. The largest reset time is 39.889 ps at `ss_low_125`; 4 corners fail CMP-08. No wrong decisions at the tested differential inputs of at least 100 uV were recorded in the 45 delay runs. Fine supplemental SOA checks reach 1.05376 V at ff/high/-40 and 1.02083 V at ff/high/125. The 0.25 ps maximum-step repeat preserves the cold-corner violation.

Official TT AVDD `energy_fJ` is 187.299 fJ: average AVDD power over the 14.5 ns mixed-amplitude test, multiplied by 400 ps. It includes the initial 100 ps and is not a dedicated 1 mV measurement; [issue #75](https://github.com/many-question/ADC-12b-100M/issues/75) tracks that definition discrepancy. A separate private +/-1 mV probe measures 188.069 fJ per complete cycle over 100 ps–14.5 ns (36 cycles), including the first evaluation with no discarded warmup decisions. It uses fine numerical settings and is supplemental evidence, not acceptance JSON. A same-source mixed-sequence control with those fine settings is 189.380 fJ; differences from the official result also include numerical settings. The separate external clock-driver charge-energy estimate is 12.277 fJ. The remaining SOA failures prevent a qualified-energy comparison.

![Complete transistor schematic](schematic.png)

Issues #40, #63, #69 and #75 are acknowledged. The frozen source has official delay and kickback evidence for all 45 corners, 50 TT mismatch samples, and standard TT noise evidence. Transient-noise coverage is 1/45 corners; all-corner noise, full input common-mode/differential coverage and full-corner SOA are not established. The candidate remains WIP, self-reported and unselected. No signoff claim is made.
