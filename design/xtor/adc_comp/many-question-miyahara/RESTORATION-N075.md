# B2-P6-N075 isolated trial

Only M12/M13 total width changes 1 -> 0.75 um (2 fingers, 30 nm); geometry comes from the 28 nm HPC+ callback. P6 PMOS6, C48 and output isolation remain unchanged. Full 31 MOS + 4 MOM net-labelled RNL is in RESTORE-B2-P6-N075.txt; check/render and visual review pass.

Raw SHA256 `302a6ddfa71bb9bb907cce08350de048e70e6b2b4d6dee3f3c5765ccc7f31e1f`; electrical `d08f24db5de16912ce555a6a37b7fc7ac5b47503afb492dfe4c9c55eb5c4b6c3`; parent electrical `993e1d7e900ad08470a928e335dcb3017181fe3691fd9e864602775e8955734e`; callback `7c01d607be45ef1e7b2f1949ef2ec89e9a6be6709412ec8d89698d4f9a21feae`.

Current adc_comp 0.9.0, 1.1 V unrounded terminal limit, physical models, APS without explicit thread count, SSD and selected saves. Formal source/results are unchanged; this is not qualification. Source and complete raw evidence are retained privately. Parent FS noise is 357.532354035666 uV; shrinking the transfer pair is a hypothesis, not an established noise improvement.

|Corner|d1 ps|d30 ps|reset ps|peak V|energy fJ|
|---|---:|---:|---:|---:|---:|
|tt_nom_27|56.013301|46.255619|24.216575|0.920616416727|211.101377|
|fs_low_125|64.703734|51.787107|26.232279|0.826017906927|219.705274|
|ss_low_125|75.278554|61.251109|32.095178|0.832326285875|193.931576|
|ff_high_m40|42.681728|35.423190|18.420938|1.015108045288|249.050159|
|sf_high_m40|55.247415|46.054610|21.321906|1.020045250160|238.258857|
TT loading: Cin 19.310905865112, CLKC 14.920785787680 fF; kickback 8.63435000581e-05 uV.


Status: Five corners/loading pass; 180 actual decisions/resets and 93 terminal pairs/corner pass. FS 17x512 noise running; TT noise gated.

New archives (CRC/member SHA verified; exact owned remote directories removed):
- `20261101-064443-soa12-n075-first`: `7b74cfa60afd66ff41ddbfcb0c1dd92fb9b7ba3cf7ac09ec3f5e71f6d7d5e670`
- `20261101-064453-soa12-n075-loading`: `42698af493b540838c6f7e3634394fd0420b1c03f1694eda7995127dd898d5af`
- `20261101-064851-soa12-n075-remaining`: `52ecbdaca462fa7db490b0a6fd93fb46b31a4270b57db403bcd8933526f91707`

Runtime seconds (solver/wrapper per job; transfer=upload+fetch; other guards separate):
first 11.8/16,12/16,23.5/28; transfer 67.6, guard 122.6, total 284.8.
loading 28.2/33; transfer 64.8, guard 122.2, total 262.2.
remaining 22.7/27,11.4/15; transfer 66.2, guard 121.4, total 276.9.
