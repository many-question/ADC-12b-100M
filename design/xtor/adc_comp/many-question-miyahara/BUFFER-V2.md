# BUFFER-V2: recover threshold-stage speed

BUFFER-V1 has a large output-validity margin in its six screened corners but misses the TT 30 mV delay by 2.984 ps. This experiment changes only the first buffer NMOS from 0.5 um/nf1 to 1 um/nf1, using the existing successful callback geometry. It increases pull-down drive and lowers the first-stage switching region. The P6 first-stage device, second inverter, core and reset circuitry remain electrically identical to V1.

The first diagnostic compares TT and SF low/-40 C against their existing V1 traces at the same 0.5 ps settings. It tests whether the speed recovery preserves physical losing-output suppression before spending work on a separate reset/feedthrough redesign. V1's high-voltage failures remain known concerns; no high-voltage qualification is inherited or claimed.

Independent source: [BUFFER-V2.txt](BUFFER-V2.txt), 31 MOS and four MOM. Electrical SHA-256: `2fcb783897758f6e3191cf85edcb8dc3a3fc8b4b357e80f8a59de2cfefa1b666`. Full RNL passes core 0.5.2 on a byte-identical `.scs` mirror with 0 errors, 0 warnings and 0 hints. This source-freeze commit claims no performance result.

![Faster first-stage pull-down](buffer-v2.png)
