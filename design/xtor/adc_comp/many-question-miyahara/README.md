# Miyahara comparator

The spec v0.7.0 refresh is complete: **45 fresh delay/energy/validity corners and 47 unchanged fresh records**. CMP-15 fails in **45/45 corners (1084/1620 cycles)**; the worst losing peak is **52.820% VDD** at `sf_high_27`. [VALIDITY.md](VALIDITY.md) lists every corner and violating cycle; [REFRESH.md](REFRESH.md) records the actual source and execution provenance.

WIP transistor candidate in 28 nm HPC+. The frozen source is revision `x56t3c1`. Fast-corner device voltages exceed 1.0 V, and SF corners show overlapping output assertions. The candidate remains unqualified.

The 15-MOS comparator core follows [Miyahara, A-SSCC 2008, Fig. 2(b)](https://www.ssc.p.isct.ac.jp/private/publications/2008/ASSCC/miyahara.pdf). DP and DN control separate M14/M15 second-stage supply devices and M12/M13 Xi reset devices. There is no shared clock-controlled second-stage supply. The calibration peripheral is omitted; the interface has no CAL or bias port.

The core directly drives the two 10 fF output loads. INP > INN asserts OUTP. Native return-to-zero outputs are supplemented by two NMOS reset devices. Each input-drain precharge device has a smaller parallel PMOS driven directly by CLKC; the main precharge devices use locally delayed CKR. A four-MOS local clock circuit generates CKR and complementary CKB for output reset. The tail remains connected directly to CLKC. This is 23 MOS devices in total, plus four permitted MOM capacitors; all clock and reset devices draw power from the measured AVDD rail.

The input pair is 56 um / 30 nm per side with 56 fingers, and the tail is 3 um. Input-drain precharge is 4 um on CKR plus 2 um on CLKC; output-reset NMOS are 2 um. The first clock inverter is N/P = 3/8 um and the second is 4/8 um. Each input drain has a 14.06 fF nominal MOM capacitor to ground; CKB and CKR each have 4.46051 fF nominal MOM capacitance to limit edge coupling. Actual geometry and device models are simulated, not ideal capacitors. MOS geometry and parasitics also come from successful callbacks.

The larger 27.42 fF capacitors improved the pilot noise but exceeded the then-applicable TT energy limit with the reset-assist circuit. Removing output buffers improved the earlier candidate's noise and energy, but the unassisted 15-MOS version failed fast-corner SOA and slow-corner reset. Weakening input precharge fixed the former at the cost of worse reset. All completed experiments, including failures and their frozen netlist hashes, are retained in [CHARACTERIZATION.md](CHARACTERIZATION.md).

Current TT delay is 47.513/38.755 ps at 1/30 mV, reset is 17.787 ps and mixed-sequence AVDD energy is **187.647 fJ/cycle** under the exact 36-cycle meter. The preserved standard TT noise is 193.758 uV rms; all 50 mismatch samples are valid, with 1.947 mV sample standard deviation. Input/CLKC capacitance is 19.310/14.924 fF and differential kickback is 0.000485769 uV. [VERIFICATION.md](VERIFICATION.md) gives settings and sources.

Both current delay and preserved kickback cover 45/45 corners. Reset fails at 0 corners; its worst value is 24.721 ps at `ss_low_125`. CMP-09 records 0 wrong decisions for tested |vd| >=100 uV. The frozen circuit retains its previously confirmed fast-corner device-voltage failures; the new standard-step sweep does not supersede those fine-step SOA checks.

Current CMP-10 integrates 100 ps–14.5 ns, exactly 36 full cycles of the mixed +/-100 mV through +/-10 uV sequence; energy is charge x VDD / 36. It is reported-only, with no acceptance limit, and excludes the external clock source. The separately estimated clock-driver charge energy is 12.089 fJ. [VERIFICATION.md](VERIFICATION.md) preserves the old v0.5.0 meter and fixed +/-1 mV fine diagnostic as historical, differently defined results. Remaining failures prevent a qualified-energy comparison.

![Complete transistor schematic](schematic.png)

The comparison uses the same input stimulus, 10 fF loads, noise bandwidth and seed for both topologies. Reported AVDD energy includes each candidate's complete local clock and output circuitry. An additional external clock-driver charge-energy estimate is `C_CLKC * VDD^2`; it is identified separately and is not an exact system energy measurement. A lower-energy failing circuit is not a qualified winner.

Issues #40, #63, #69, #75, #77, #78 and #84 are acknowledged. All 92 records are fresh under current reached-dependency checks. Noise covers only TT; full common-mode/differential range, all-corner noise, full-corner SOA and mixed-top qualification remain unestablished. The candidate remains WIP, self-reported and unselected.

Priority structural direction: Rework the native-output/reset interface while preserving the drain-triggered 15-MOS core. Evaluate a rail-restoring output stage with mutual exclusion and controlled reset isolation, so the physical losing output remains below 30% VDD and clock/reset feedthrough into the output reset devices is reduced. The observed loser excursions and MRQP gate-drain stress motivate this direction; they do not prove a shared cause. An ideal first-event latch alone cannot repair a physical losing-output excursion. Added delay, AVDD energy, clock load and noise must be measured before accepting a revision.

Active iteration: [BUFFER-V1](BUFFER-V1.md) adds a physical CMOS output interface. Its six-corner screen passes actual output validity (0/216 violating cycles, losing peak <0.564% VDD) but fails TT 30 mV delay and internal terminal stress. The independent source, RNL, complete terminal maxima and failure mechanisms are retained. The canonical measurements above remain the previous baseline; the design line is active.

[BUFFER-V2](BUFFER-V2.md) recovers TT 30 mV delay to 48.296 ps by strengthening only the first buffer pull-down. TT and the targeted SF low/-40 C trace retain output validity and pass full terminal stress locally. High-voltage reset/feedthrough still requires a separate repair and fresh screening; two corners do not establish qualification.

Continuous physical-output repair experiments remain independent of this canonical baseline: [B1](BUFFER-V1.md), [B2](BUFFER-V2.md) and [B3](BUFFER-V3.md) preserve their sources and measured failures. B2 passes validity and timing at six key corners but fails high-voltage stress. [B4](BUFFER-V4.md) simplifies input precharge and strengthens clocked raw reset after B3 cross-output feedback failed to bound all excursions.

[B4](BUFFER-V4.md) removes input-drain overvoltage and passes timing/validity at three key corners, but fast reset and clock release still produce raw, buffer and output excursions. [B5](BUFFER-V5.md) applies physical capacitance and weaker reset/clock drive at those measured events.

[B5](BUFFER-V5.md) reduces the cold-FF peak to 1.00833 V while retaining three-corner timing and validity. [B6](BUFFER-V6.md) targets the remaining clock, raw-node and buffer slew with slower physical clock drive and more intermediate/buffer MOM damping.

[B6](BUFFER-V6.md) passes clock and intermediate-node stress while small raw/buffer/output excursions remain. [B7](BUFFER-V7.md) adds physical weak rail-offset loads at those measured nodes and retains the original output-validity thresholds.

[B7](BUFFER-V7.md) passes three-corner stress and validity but fails SF low/cold reset at 36.559095 ps. [B8](BUFFER-V8.md) halves its six physical PMOS pull-ups while retaining both output diode loads per side.
