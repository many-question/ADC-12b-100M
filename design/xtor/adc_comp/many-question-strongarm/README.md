# StrongARM comparator

The spec v0.7.0 refresh is complete: **45 fresh delay/energy/validity corners and 47 unchanged fresh records**. CMP-15 **passes at all 45 corners (0/1620 violating cycles)**; the worst losing peak is **21.237% VDD** at `sf_low_m40`. [VALIDITY.md](VALIDITY.md) lists every corner and violating cycle; [REFRESH.md](REFRESH.md) records the actual source and execution provenance.

WIP transistor candidate in 28 nm HPC+. The frozen source is revision `p56t3c1`. Fast-corner device voltages exceed 1.0 V and some slow corners fail reset, so the candidate remains unqualified.

The single-stage StrongARM core follows [Razavi, Fig. 1(b)](https://www.seas.ucla.edu/brweb/papers/Journals/BR_Magzine4.pdf). A CMOS inverter on each internal output provides the required return-to-zero interface: INP > INN discharges QP and asserts OUTP. Both external outputs reset low. The two output loads remain 10 fF each.

Input-drain precharge uses two series PMOS per side, controlled by CLKC and its locally delayed copy CKD. Output-node precharge uses two parallel PMOS per side with the same controls. This releases input-drain precharge first during evaluation and establishes output-node precharge first during reset. This reduces some earlier edge-coupling problems, but it does not eliminate all voltage violations. The clock generator is two CMOS inverters. There is no extra gain stage. The complete candidate contains 23 MOS devices and four permitted MOM capacitors.

Each input NMOS is 56 um / 30 nm with 56 fingers. The tail is 3 um and the regenerative NMOS/PMOS pairs are 12/8 um. Each input drain has 14.06 fF nominal MOM capacitance to ground; CKB and CKD each have a 4.46051 fF nominal MOM device. Device dimensions, parasitics and capacitor geometries come from successful callbacks; the actual permitted device models are simulated.

The comparison with Miyahara uses the same excitation, output loads, transient-noise bandwidth and seed. AVDD energy includes all local clock and output devices. `C_CLKC * VDD^2` is reported separately as an external clock-driver charge-energy estimate, not an exact system energy measurement. A lower-energy failing version is not a qualified winner.

Earlier variants expose a tradeoff between noise, delay, energy and edge-coupled voltage stress. The `k56t3c2` pilot reaches 159.0 uV rms and 195.3 fJ but misses the TT 30 mV delay limit and reaches 1.03741 V at ff/high/125. Larger common-clock precharge devices reach 144.6 uV rms but exceed 200 fJ and increase fast-cold overshoot to 1.08620 V. These are measurements of different frozen exploratory circuits, not evidence for the current source. [CHARACTERIZATION.md](CHARACTERIZATION.md) retains every completed experiment, including failures and hashes.

Current TT delay is 56.937/44.921 ps at 1/30 mV, reset is 28.900 ps and mixed-sequence AVDD energy is **188.590 fJ/cycle** under the exact 36-cycle meter. The preserved standard TT noise is 187.108 uV rms; all 50 mismatch samples are valid, with 1.898 mV sample standard deviation. Input/CLKC capacitance is 19.313/15.156 fF and differential kickback is 0.386579 uV. [VERIFICATION.md](VERIFICATION.md) gives settings and sources.

Both current delay and preserved kickback cover 45/45 corners. Reset fails at 4 corners; its worst value is 39.889 ps at `ss_low_125`. CMP-09 records 0 wrong decisions for tested |vd| >=100 uV. The frozen circuit retains its previously confirmed fast-corner device-voltage failures; the new standard-step sweep does not supersede those fine-step SOA checks.

Current CMP-10 integrates 100 ps–14.5 ns, exactly 36 full cycles of the mixed +/-100 mV through +/-10 uV sequence; energy is charge x VDD / 36. It is reported-only, with no acceptance limit, and excludes the external clock source. The separately estimated clock-driver charge energy is 12.277 fJ. [VERIFICATION.md](VERIFICATION.md) preserves the old v0.5.0 meter and fixed +/-1 mV fine diagnostic as historical, differently defined results. Remaining failures prevent a qualified-energy comparison.

The earlier 50%-threshold saved-waveform audit is historical. The current, stricter 30% losing-output criterion is evaluated explicitly in [VALIDITY.md](VALIDITY.md); absence of dual-high samples alone does not establish CMP-15 compliance.

![Complete transistor schematic](schematic.png)

Issues #40, #63, #69, #75, #77, #78 and #84 are acknowledged. All 92 records are fresh under current reached-dependency checks. Noise covers only TT; full common-mode/differential range, all-corner noise, full-corner SOA and mixed-top qualification remain unestablished. The candidate remains WIP, self-reported and unselected.

Priority structural direction: Rework the series input-drain precharge network to remove floating DPX/DNX intermediate nodes and give them a defined, bounded reset path, with controlled tail/precharge overlap. The known MRDP drain-source overshoot and slow-corner reset failures make this the first structural experiment. This is a repair hypothesis; preserve the observed CMP-15 pass while improving reset and terminal stress. Any added clamp or driver must be evaluated for reset, validity, device stress, noise, delay and total AVDD/clock energy.

The separate [RESET-V1 four-corner experiment](RESET-V1.md) is complete and rejected as a replacement: reset improves, but stress shifts to the new logic, TT 30 mV delay fails, and energy/clock charge increase. Its frozen source and private-diagnostic evidence do not replace this canonical baseline.

Continuous repair experiments remain separate from the canonical baseline: [V2](RESET-V2.md), [V3](RESET-V3.md), [V4](RESET-V4.md), [V5](RESET-V5.md) and [V6](RESET-V6.md) retain failed screens and actual source hashes. [V7](RESET-V7.md) tests physical diode-connected loads after clock compensation failed to bound reset peaks. A failed version stops its own expansion; design iteration continues.

[V7](RESET-V7.md) passes four-corner terminal stress but fails CMP-15 because its Q loads remain on during evaluation. [V8](RESET-V8.md) gates those loads with a physical reset clock and checks the resulting phase overlap and capacitance.

[V8](RESET-V8.md) restores four-corner timing and output validity, with only cold-FF Q stress still failing at 1.00737 V. [V9](RESET-V9.md) changes only the conductance of the reset-gated Q shunts to address that measured event.

[V9](RESET-V9.md) still fails cold-FF stress and now misses slow reset; [V10](RESET-V10.md) returns to lighter Q shunts and changes the physical clock turn-on timing while bounding its low-level excursion.

[V10](RESET-V10.md) passes four-corner stress and validity, but SS low/hot reset is 35.044926 ps and therefore fails. [V11](RESET-V11.md) increases only direct input precharge from P2 to P2.2 to recover reset margin.

[V11](RESET-V11.md) fails the added SF low/cold output-validity and SF high/27 terminal-stress checks. [V12](RESET-V12.md) changes output pull-down strength and Q-reset slew at those measured events. [Energy comparison](ENERGY-COMPARISON.md) includes the substantial cost of the repair circuitry.
