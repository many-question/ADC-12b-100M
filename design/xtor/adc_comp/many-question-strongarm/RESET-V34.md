# V34: stronger N latch pair

Private, unqualified physical trial. Only MLNP/MLNN change N4 to N16 (16 one-um fingers, L30nm; twice V32 N8), with complete zero-warning callback geometry/parasitics. Other 21 MOS and five MOMs are unchanged. V33 full FS noise failed at 483.2613219887676 uV; stronger latch drive is a new hypothesis, not a measured noise benefit.

Electrical SHA-256 `56babc884fca6a518621de8d4eec451b64c60dd45bf1af2ff393f3cc374e215b`; callback `f7dd3061987c03157e7411ed97c5554d5d6981d377691e3da1413bee8298ef85`. [Complete RNL](RESET-V34.txt) checks/renders without errors or warnings; drawing inspected locally. [Predecessor source](https://github.com/many-question/ADC-12b-100M/blob/d2dd7184b0f435b46b351b948eb1ca4bdbeeb99b/design/xtor/adc_comp/many-question-strongarm/RESET-V33.txt) and failures retained. Fresh baseline/tighter timing, reset, validity, private 1.0 V stress, loading and full physical noise are pending. Canonical/formal failure unchanged.
