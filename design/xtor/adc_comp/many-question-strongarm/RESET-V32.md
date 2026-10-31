# RESET-V32: reduce local clock loading

[V31](RESET-V31.md) repairs the SS reset gate but fails dedicated TT clock-input capacitance at 16.65232415714863 fF against 16 fF. V32 changes only MCKN from 4 um/nf4 to 3 um/nf3, MCKP from 2.7 to 2.4 um/nf3, and the CKB MOM from 8 to 6 fingers. All lengths, port stimuli, Q precharge devices, input pair, 3 um tail, P8/N4 output buffers, other 21 MOS devices and other four MOMs remain V31.

Smaller CKB driver gates target external clock capacitance. Reducing the local CKB load partly offsets their lower drive strength; actual clock timing, output validity and unrounded device stress must be measured. No capacitance, timing or noise pass is assumed. Four critical deterministic corners and a dedicated TT capacitance/kickback measurement precede any noise expansion.

The initial 4-finger MOM request was rejected by the PDK constraint (minimum 6 fingers) and is retained as a failed geometry request. It was never used in a simulated source. An explicit 6-finger request passes with zero warnings, giving callback capacitance 1.46055 fF. Both MOS requests also pass without warnings and preserve complete callback geometry/terminal parasitics. All three accepted callbacks share the verified provider/release; their exact owned remote directories are absent.

| Callback | SHA-256 |
|---|---|
| N3 | `789ebd4902cc3560584cc5cbd0bfc8a94170a37d574f7b64190f41fce0d43be2` |
| P2.4 | `fbd2ae501149d9e263c33ae9c7ea35093767bb3d159beabba77b0ddf3bfb7344` |
| 6-finger MOM | `5203e49d3fdbdd21901ae4d33fe1937969ddacb2d55bce81580f8548ebb6a240` |

Electrical SHA-256: `0611d6028825bf29c02983e7e337a09e4627884b7aef22e20130770b72d7c557`. The [complete RNL source](RESET-V32.txt) was checked and rendered from a byte-identical mirror. The full local drawing is retained with the source-preparation evidence; a duplicate PNG is not added to the bounded candidate folder. Canonical V27 and all formal records remain unchanged.

Future runs use an explicit selected-signal policy retaining every required DUT SOA node and named energy/clock probes. Full noise uses the unchanged 17 x 512 sampler-only protocol. Output-policy differences are recorded separately from unchanged stimuli, numerical tolerances and measurement code.
