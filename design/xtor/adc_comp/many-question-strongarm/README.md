# StrongARM comparator

WIP transistor candidate in 28 nm HPC+. The current source is revision `p56t3c1`. It meets the measured TT pilot limits but fails fast-corner device voltage limits and slow-corner reset. No signoff claim is made.

The single-stage StrongARM core follows [Razavi, Fig. 1(b)](https://www.seas.ucla.edu/brweb/papers/Journals/BR_Magzine4.pdf). A CMOS inverter on each internal output provides the required return-to-zero interface: INP > INN discharges QP and asserts OUTP. Both external outputs reset low. The two output loads remain 10 fF each.

Input-drain precharge uses two series PMOS per side, controlled by CLKC and its locally delayed copy CKD. Output-node precharge uses two parallel PMOS per side with the same controls. This releases input-drain precharge first during evaluation and establishes output-node precharge first during reset. This reduces some earlier edge-coupling problems, but it does not eliminate all voltage violations. The clock generator is two CMOS inverters. There is no extra gain stage. The complete candidate contains 23 MOS devices and four permitted MOM capacitors.

Each input NMOS is 56 um / 30 nm with 56 fingers. The tail is 3 um and the regenerative NMOS/PMOS pairs are 12/8 um. Each input drain has 14.06 fF nominal MOM capacitance to ground; CKB and CKD each have a 4.46051 fF nominal MOM device. Device dimensions, parasitics and capacitor geometries come from successful callbacks; the actual permitted device models are simulated.

The comparison with Miyahara uses the same excitation, output loads, transient-noise bandwidth and seed. AVDD energy includes all local clock and output devices. `C_CLKC * VDD^2` is reported separately as an external clock-driver charge-energy estimate, not an exact system energy measurement. A lower-energy failing version is not a qualified winner.

Earlier variants expose a tradeoff between noise, delay, energy and edge-coupled voltage stress. The `k56t3c2` pilot reaches 159.0 uV rms and 195.3 fJ but misses the TT 30 mV delay limit and reaches 1.03741 V at ff/high/125. Larger common-clock precharge devices reach 144.6 uV rms but exceed 200 fJ and increase fast-cold overshoot to 1.08620 V. These are measurements of different frozen exploratory circuits, not evidence for the current source. [CHARACTERIZATION.md](CHARACTERIZATION.md) retains every completed experiment, including failures and hashes.

The current TT pilot measures 199.11 uV rms (95% interval 177.35–224.05 uV), 189.38 fJ from AVDD, 58.12/44.99 ps at 1/30 mV, 19.313 fF per input and 15.151 fF at CLKC. The ss/low/125 reset is 38.44 ps, exceeding 35 ps. Fine ff/high/-40 and ff/high/125 checks reach 1.05376 V and 1.02083 V, respectively. No wrong decisions at the tested differential inputs of at least 100 uV or simultaneous high outputs were observed. These pilots are not formal acceptance and do not establish all-corner coverage.

![Complete transistor schematic](schematic.png)

Issues #40, #63 and #69 are acknowledged. Spec v0.5.0 requires formal 17 x 512 noise and 50 TT local-mismatch samples with seed 6303, all valid. These tests and full corner coverage remain outstanding for the final frozen revision.
