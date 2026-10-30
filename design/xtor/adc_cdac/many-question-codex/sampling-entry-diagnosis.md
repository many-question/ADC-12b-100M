# CDAC diagnosis and trial ledger

The formal candidate is N4, source SHA256
`3d62b80300fc5d85e3fc4e498cd22cedfa92ed006c502922526f1641e0a2ae61`.
The [README](README.md) summarizes its topology, fixed 5% per-physical-unit
parasitic assumption, formal TT pass and incomplete PVT coverage.

The complete historical report is preserved at
[commit 6a4bf94](https://github.com/many-question/ADC-12b-100M/blob/6a4bf94977db967dbd27ef47669d5d3d25735477/design/xtor/adc_cdac/many-question-codex/sampling-entry-diagnosis.md),
with all its relative image links intact in that immutable tree. The
annotated `adc-cdac-many-question-history-20261031` tag retains the snapshot.
Only duplicate current-tree prose and old diagnostic images were compacted;
the source and all 12 official result/figure files remain byte-identical.
The prior report, figures and their original provenance also have a private
hash-verified copy. New experiments never inherit the older validation.

## Evidence ledger

| Version / scope | Observed result | Disposition and provenance |
|---|---|---|
| Pre-N4 | Genuine RL12 50.1 ps, Qref 2.629 pC, SFDR/SNDR 69.6121/69.5735 dB failures | Retained by [pre-N4 tag](https://github.com/many-question/ADC-12b-100M/tree/adc-cdac-many-question-pre-n4-20261030); full history in the archived report |
| Formal N4 TT | All 17 required metrics pass; complete prescribed tracking comparison passes | [N4 TT evidence tag](https://github.com/many-question/ADC-12b-100M/tree/adc-cdac-many-question-n4-tt-20261030) retains actual clean simulation commits; source unchanged |
| Formal N4 ss_low_125 | RL12 47.4 ps and start 117.7 ps fail; RL5 69.2 ps, tau 14.809442 ps and droop 0.008844550 LSB pass | First PVT expansion stopped; weights full scale 0.993092578 V passes; original evidence unchanged |
| Unchanged N4, private strict 28 ns | RL12/start remain 47.4/117.7 ps and tau 14.809442 ps | Mechanism diagnostic, not a new official record; 17 observed MOS / 51 pairs only |
| Private bit-12 output widths +25% | RL12/start improve to 42.2/113.0 ps but fail; tau 17.111203 ps newly fails | Rejected; no TT or expensive downstream expansion; one full 70 ns SS job |

The original N4 and rejected-width-trial stop records remain preserved.
Continuing design work uses separate variants and per-variant gates, rather
than resuming a failed variant's expensive expansion.

## Formal N4: limits and numerical evidence

TT weights/calibration gives Cs 2.065011578 pF, full scale 0.993034321 V,
calibration margin 0.369060944 LSB, calibrated ENOB loss 0.000364369 bit
and TOP gain 0.893800051. TT settling gives RL5/RL12 47.3/35.3 ps,
tau 9.120184 ps, start 83.4 ps, droop 0.004380784 LSB and Qref
1.124389535 pC. DH5/PHI_S/PHI_SB/CONV loads are
0.830865/6.432310/12.231291/9.850052 fF. These are formal N4 results.

TT tracking uses the full coherent 256-sample record after four warmup
cycles: 48.828125 MHz input at 100 MS/s, -1 dBFS, 50 ohm per half,
20 fF TOP load per half, sampled 300 ps after CONV. Main SFDR/SNDR are
86.417966859/84.523548567 dB; the 0.5 ps gear2only twin gives
86.418274708/84.523764369 dB. Sample differences are 0.155934342 uV RMS
and 0.223638200 uV maximum. The actual clean commits and complete sample
records remain retained; the original twin finished after its controller
wait expired and was collected without launching a replacement.

The project prescribes reltol 1e-7, voltage tolerance 1e-8, maxstep 1 ps
and traponly for tracking, with 0.5 ps/gear2only comparison. This tests
step/method sensitivity at the prescribed tolerances, not the loosest
adequate reltol. Formal weights/settling used reltol 0.001 and voltage
tolerance 1e-6; settling maxstep is 2 ps. The stricter private diagnostics
use 0.5 ps, 1e-7, 1e-8 and traponly, with actual settings read from logs.

The same-source private TT pressure records cover all 540 MOS / 1,620
gs/gd/ds pairs for 70 ns, maximum 0.977333326 V, and both halves
(1,080 MOS / 3,240 pairs) for 125 ns of sine input, maximum 0.990224783 V.
The latter leaves only 9.775 mV to the project 1.0 V limit. Model warnings,
including gate-to-bulk checks, remain retained separately. This is neither
complete PVT/startup/long-hold reliability nor actual-bootstrap integration.

## Confirmed slow-corner mechanism

The original SS deadlines fail in adjacent raw samples, not just by
interpolation. At 40 ps after RL12, TOP error is 36.462295 mV against
9.602916 mV allowed. At the 100 ps start deadline it is 5.147058 mV
against 1.585493 mV allowed. The unchanged strict 28 ns diagnostic gives
36.429220/5.146567 mV and the same 47.4/117.7 ps settling verdicts.
Sharp local waveform details differ, so this is not isolated reltol
convergence or an assertion that whole waveforms are identical.

At start, ENB/EN 50% crossings are 17.980/22.688 ps after CONV. The
low GN and high GP enter 1% bands at 44.9/54.1 ps, but bit-12 BL/BH need
118.8/121.8 ps. BH first dips to 0.515938 V before recovering. At RL12,
LHIB -> PCOND -> GP -> BL 50% times are 6.927 -> 13.825 -> 20.459 ->
37.503 ps. At 40 ps GP/GN are 0.010873/0.003276 V while BL is only
0.513880 V toward 0.899851 V. The high plate couples upward to
0.958726 V. Significant plate motion remains after the main gate edges;
these interacting stages cannot be added as independent delays.

![Unchanged N4 slow-corner stage timing](slow-corner-stage-timing.png)

The native currents include displacement. The strict N4 diagnostic saved
bit-12 and selected buses, not every other bit's bottom plates. Its 17-MOS
terminal-pair check does not establish full-device SS pressure coverage.

## Rejected bit-12 output-width +25% experiment

Only paired H/L output widths changed: N/P 15/30 -> 18.75/37.5 um,
length 30 nm, fingers 10/20 and ratio 2 unchanged. Geometry validation
had no warnings; two shared-driver lines affect four flattened MOS.
Private source SHA256:
`d456da333fcd63c6035af1a4c69b29b156ef8a630e9d5cabad6fba42181c8dbf`.

| Metric | Official N4 SS | Private +25% SS | Variant verdict |
|---|---:|---:|---|
| RL5 | 69.2 ps | 67.5 ps | PASS <=75 ps |
| RL12 | 47.4 ps | 42.2 ps | FAIL >40 ps |
| Equivalent tau | 14.809442 ps | 17.111203 ps | New FAIL >15 ps |
| Start | 117.7 ps | 113.0 ps | FAIL >100 ps |
| Droop | 0.008844550 LSB | 0.002201507 LSB | PASS <=0.1 LSB |

The same strict 28 ns N4 baseline confirms the early-window timing
comparison. The later charge/load comparison has only the coarser official
70 ns baseline: Qref 1.745559443 -> 1.774002032 pC (+1.6294%);
DH5/PHI_S/PHI_SB/CONV 0.807291/5.966357/12.102270/9.561514 fF in the
variant. These five metrics are typ-only and remain n/a in this SS screen;
no TT charge/load result is claimed for the rejected circuit.

The official equivalent tau is `(t_1pct - t_10pct)/ln(10)`, using last
out-of-band crossings, not an independent single-pole fit. The variant's
RL12 10% crossing advances 44.1 -> 39.9 ps but 1% moves 78.2 -> 79.3 ps.
TOP overshoot increases 3.319162 -> 6.879206 mV (1.728% -> 3.581%).
Low GP's 50% edge slows 20.459 -> 20.962 ps while BL's 50% crossing
advances 37.503 -> 35.824 ps and BL's 1% time improves 84.1 -> 75.2 ps.
The low PMOS absolute native gate charge over -120..+300 ps grows
22.323 -> 27.945 fC. Faster BL recovery does not ensure a shorter TOP
tail when output-gate load and network redistribution both change.

At the variant's TOP peak (+54.247 ps), held bit-11 BL/BH remain
+61.71/+24.37 mV away from their final values. Those other plates were
not saved in the strict N4 baseline, so their separate contributions to
the before/after change are not identified. At start, the widened gates
settle later but BL/BH settle earlier; TOP still needs 113 ps. ENB/EN
50% timing is effectively unchanged. This rejects the tested sizing,
without proving that a particular branch or alternative size is the fix.

The actual 70 ns settling TB has one XDUT and no external MOS-like
devices: all 540 MOS / 1,620 pairs were checked at all 199,960 saved times.
There are zero project gs/gd/ds violations, exact maximum 0.968497692620 V
at XDUT.XB2.XDL.MNOUT ds, 60.075866 ns. This is complete coverage of that
single-sided TB, not the two-sided sine test. Actual maxstep/reltol/voltage
tolerance are 0.5 ps/1e-7/1e-8, traponly. One job used four APS solver
threads, with 395 s job time / 393 s simulator time. Raw logs retain zero
errors, 16 warnings, eight notices and suppressed warnings.

Nine raw files and 50 frozen inputs were recovered/hash-verified before
exact cleanup; archive SHA256:
`63c14b394df86f5360176f17eea9fad126adc36c069dff6ae2e417b01c395bf9`.
The private full-pair table, signed waveform/charge/coupling audits,
scripts and inspected figure remain retained. No TT, tracking, noise,
second variant or other corner followed that failed gate.

## Matched full-window reference-output family experiment

Two independent 70 ns `ss_low_125` runs share the complete original
stimulus, saves and strict numerical settings: 0.5 ps maximum step,
reltol 1e-7, voltage tolerance 1e-8, traponly. Both started from clean
commit `8a8e88a0ba4e2b5bdfb88bd7710726d36d675c7d`. The unchanged-N4
reference fills the missing held-plate and late-window observations.
The private `v1-refout-ulvt` case changes only the model family of all
52 flattened reference-output MOS; W/L/fingers, logic and capacitors
remain unchanged. Eighteen unique device geometries and pinned RNL
validation pass without warnings. Its source SHA256 is
`25ba0e52d44f0f6db08d0fa8891c6be0f5d6874bc42f3e04ce559169e78cbf7e`.

| Quantity | Matched N4 reference | Private lower-threshold outputs | Requirement at SS |
|---|---:|---:|---|
| RL5 settling | 69.3 ps | 58.7 ps | both pass, <=75 ps |
| RL12 settling | 47.4 ps | 42.7 ps | both fail, <=40 ps |
| Equivalent tau | 14.809442 ps | 11.204798 ps | both pass, <=15 ps |
| Conversion-start settling | 117.7 ps | 100.6 ps | both fail, <=100 ps |
| Hold droop | 0.008769519 LSB | 0.004251046 LSB | both pass, <=0.1 LSB |
| VREFP charge / conversion | 1.746078108 pC | 2.619548392 pC | n/a, typ-only |
| DH5 input capacitance | 0.807291 fF | 0.807291 fF | n/a, typ-only |
| PHI_S input capacitance | 5.966224 fF | 5.966242 fF | n/a, typ-only |
| PHI_SB input capacitance | 12.093625 fF | 12.059253 fF | n/a, typ-only |
| CONV input capacitance | 9.561519 fF | 9.561489 fF | n/a, typ-only |

The strict reference retains both original timing failures. Its RL5 result
is 0.1 ps later than the coarse official reference; it remains passing.
The changed circuit still fails both deadline checks, including both raw
samples bracketing each deadline. At 100 ps, start error is 1.666544 mV
versus a 1.586790 mV allowance. At 40 ps, RL12 error is 18.839163 mV
versus 9.596509 mV. No TT or tracking run follows this failed case.

![Matched complete SS reference and output-family trial](matched-output-family-screen.png)

RL12's last 10%/1% crossings change from 44.1/78.2 ps to 39.9/65.7 ps.
TOP overshoot falls from 3.319162 to 2.812952 mV. The switched BL reaches
50% at 34.527 ps instead of 37.503 ps, while its PMOS gate reaches 50%
at 20.553 ps instead of 20.459 ps. The bit-11 held BL/BH last leave a
1 mV band at 107.1/74.9 ps instead of 127.2/84.1 ps. These matching
observations support improved output and held-bank recovery, with almost
unchanged command delay; they do not identify a unique pole or branch.

The charge increase is 0.873470284 pC, or 50.0247%. Quiet-window currents
show a substantial static cost. At VIN=0.65 V during 3..4 ns, with gate
and plate voltages constant to numerical precision, bit-12 low-side
disabled NMOS/PMOS native drain currents change from +0.999487/-0.505634
uA to +14.525968/-4.222254 uA. The sampled BL is 0.649982710 V in N4
and 0.649639693 V in the trial. During neutral hold at 7..8 ns, the
disabled high-side NMOS carries 1.520908 versus 23.818919 uA, and the
disabled low-side PMOS magnitude is 2.500204 versus 20.715273 uA.
Native currents include displacement; the quiet-window audit retains
voltage/current variation. These fixed-input observations support an
off-current contribution, but do not decompose all of Qref or establish
sampling linearity across input voltage and frequency.

Both actual testbenches contain one XDUT and no external MOS devices.
Each checks all 540 MOS / 1,620 gs/gd/ds pairs over its full saved record,
with zero project-limit violations. N4's exact maximum is
0.968951801189 V at XB2.XDL.MNOUT ds (60.075866186 ns); the changed
circuit's maximum is 0.967432353689 V at XB9.XDL.MPOUT ds
(5.165299322 ns). There are 199,924/199,744 time points and 354 saved
signals (277 voltages, 77 native currents), respectively. Job times are
348/343 s; the two-job peak is within the six-job session limit.

For each case, nine raw files and all 50 frozen inputs were recovered and
SHA256-verified before exact run cleanup. Full waveform caches, all-pair
tables, measurement scripts, comparisons and quiet-window audit are retained.
Archive SHA256 values:

- N4 reference: `608fb2e6b10a19cbf25aa29b13e6a75d2c54ff60573a5844cc95c658958a20ce`
- Changed outputs: `6c3732ae6999c971ce596f292746ede69d56fd1e0aee9f11d46567f2ee039cbb`

## Continuing experiments

The next independent case starts from formal N4, retaining its nominal-
threshold output devices. It coordinates an approximately 35% output-width
increase across switched and held banks, and doubles the existing shared
ENB pull-down while retaining its finger width. The measured held-bank
recovery and enable delay motivate these changes. External DH/RL input
devices remain at their original sizes. Device geometry, RNL, gate load,
reference charge, overshoot and pressure require the new case's own evidence;
neither prior circuit's verification transfers.

A brief separately controlled reference-drive assist remains an unimplemented
hypothesis, with additional pulse alignment and loading questions.
Each case screens SS settling plus all MOS pairs in its actual TB before
TT charge/load/settling, then spectra and further corners. A failed case
stops its costly expansion and informs the next independent change.
Formal N4 and all official results remain unchanged.
