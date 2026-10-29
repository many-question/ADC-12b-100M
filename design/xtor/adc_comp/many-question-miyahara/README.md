# Miyahara comparator

WIP transistor candidate in 28 nm HPC+. The current source is exploratory revision `q0t3c1`; it is not yet qualified.

The 15-MOS comparator core follows [Miyahara, A-SSCC 2008, Fig. 2(b)](https://www.ssc.p.isct.ac.jp/private/publications/2008/ASSCC/miyahara.pdf). DP and DN control separate M14/M15 second-stage supply devices and M12/M13 Xi reset devices. There is no shared clock-controlled second-stage supply. The calibration peripheral is omitted; the interface has no CAL or bias port.

The core directly drives the two 10 fF output loads. INP > INN asserts OUTP. The core has native return-to-zero outputs, supplemented by two NMOS reset devices. A four-MOS local clock circuit delays the input-drain precharge controls and generates the complementary output-reset control. The tail remains connected directly to CLKC. This is 21 MOS devices in total, plus two permitted MOM capacitors; all clock and reset devices draw power from the measured AVDD rail.

The input pair is 48 um / 30 nm per side with 48 fingers, the tail is 3 um, input-drain precharge devices are 6 um, and the added output reset devices are 4 um. The first clock inverter is N/P = 1/8 um and the second is 8/8 um. Each DP/DN-to-ground MOM capacitor has a callback nominal value of 14.06 fF. Its actual geometry and model are simulated, not an ideal capacitor. MOS geometry and parasitics also come from successful device callbacks.

The larger 27.42 fF capacitors improve the pilot noise but fail the TT energy limit with the reset-assist circuit. Removing output buffers improves the earlier candidate's noise and energy, but the unassisted 15-MOS version fails fast-corner SOA and slow-corner reset. Weakening input precharge fixes the former at the cost of worse reset. All completed experiments, including failures and their frozen netlist hashes, are retained in [CHARACTERIZATION.md](CHARACTERIZATION.md).

The immediately preceding `r0t3c1` experiment measured 181.4 uV rms in a 17-level x 64-decision TT pilot, 185.2 fJ from AVDD, 47.8/38.9 ps at 1/30 mV, and 18.0 ps reset at ss/low/125. Its ff/high/125 maximum device voltage was 0.99994 V, so the current revision changes the clock-device sizes before further voltage and cold-corner checks. These numbers are not evidence for the current source or formal acceptance.

The comparison uses the same input stimulus, 10 fF loads, noise bandwidth and seed for both topologies. Reported AVDD energy includes each candidate's complete local clock and output circuitry. An additional external clock-driver charge-energy estimate is `C_CLKC * VDD^2`; it is identified separately and is not an exact system energy measurement. A lower-energy failing circuit is not a qualified winner.

Issues #40, #63 and #69 are acknowledged. Spec v0.5.0 requires the standard 17 x 512 noise test and 50 TT local-mismatch samples with seed 6303, all valid. Formal evidence for the final frozen revision and full corner coverage remain outstanding. No signoff claim is made.
