# Miyahara comparator

WIP transistor candidate in 28 nm HPC+. The current source is revision `x56t3c1`. Its TT pilot meets the measured limits, but it remains unqualified because fast-corner device voltages exceed 1.0 V.

The 15-MOS comparator core follows [Miyahara, A-SSCC 2008, Fig. 2(b)](https://www.ssc.p.isct.ac.jp/private/publications/2008/ASSCC/miyahara.pdf). DP and DN control separate M14/M15 second-stage supply devices and M12/M13 Xi reset devices. There is no shared clock-controlled second-stage supply. The calibration peripheral is omitted; the interface has no CAL or bias port.

The core directly drives the two 10 fF output loads. INP > INN asserts OUTP. Native return-to-zero outputs are supplemented by two NMOS reset devices. Each input-drain precharge device has a smaller parallel PMOS driven directly by CLKC; the main precharge devices use locally delayed CKR. A four-MOS local clock circuit generates CKR and complementary CKB for output reset. The tail remains connected directly to CLKC. This is 23 MOS devices in total, plus four permitted MOM capacitors; all clock and reset devices draw power from the measured AVDD rail.

The input pair is 56 um / 30 nm per side with 56 fingers, and the tail is 3 um. Input-drain precharge is 4 um on CKR plus 2 um on CLKC; output-reset NMOS are 2 um. The first clock inverter is N/P = 3/8 um and the second is 4/8 um. Each input drain has a 14.06 fF nominal MOM capacitor to ground; CKB and CKR each have 4.46051 fF nominal MOM capacitance to limit edge coupling. Actual geometry and device models are simulated, not ideal capacitors. MOS geometry and parasitics also come from successful callbacks.

The larger 27.42 fF capacitors improve the pilot noise but fail the TT energy limit with the reset-assist circuit. Removing output buffers improves the earlier candidate's noise and energy, but the unassisted 15-MOS version fails fast-corner SOA and slow-corner reset. Weakening input precharge fixes the former at the cost of worse reset. All completed experiments, including failures and their frozen netlist hashes, are retained in [CHARACTERIZATION.md](CHARACTERIZATION.md).

The current TT pilot is 184.95 uV rms (95% interval 164.10–208.97 uV), with 186.34 fJ from AVDD, 47.61/38.75 ps at 1/30 mV, 19.311 fF per input and 14.924 fF at CLKC. Slow-corner reset is 23.55 ps. The fine fast-corner checks still fail: ff/high/-40 reaches 1.01599 V and ff/high/125 reaches 1.00488 V. No wrong decisions at the tested differential inputs of at least 100 uV or simultaneous high outputs were observed. These are supplemental pilots, not formal acceptance, and do not establish all-corner coverage.

![Complete transistor schematic](schematic.png)

The comparison uses the same input stimulus, 10 fF loads, noise bandwidth and seed for both topologies. Reported AVDD energy includes each candidate's complete local clock and output circuitry. An additional external clock-driver charge-energy estimate is `C_CLKC * VDD^2`; it is identified separately and is not an exact system energy measurement. A lower-energy failing circuit is not a qualified winner.

Issues #40, #63 and #69 are acknowledged. Spec v0.5.0 requires the standard 17 x 512 noise test and 50 TT local-mismatch samples with seed 6303, all valid. Formal evidence for the final frozen revision and full corner coverage remain outstanding. No signoff claim is made.
