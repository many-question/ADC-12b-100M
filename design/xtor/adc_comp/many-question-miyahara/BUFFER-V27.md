# B27: weaker D-gated latch clamps

Private, unqualified physical trial. Only M8/M9 change from N4 to N2 at 30 nm, using the exact verified B26 M12/M13 model, two 1 um fingers and all terminal parasitics. The other 41 MOS devices and nine MOMs are unchanged. Earlier R-node release is a hypothesis; delay, reset, output validity, unrounded SOA, port loading and full physical noise need new checks.

Electrical SHA-256 `12af77935658afe02d22cf915b436c702ebafcc0635e2fef176e62417aa52bac`. The [complete RNL source](BUFFER-V27.txt) passes check/render with zero errors or warnings; its full drawing is inspected and retained locally. A stale footer is corrected to reset N8 / buffer N2.6. B26 is preserved at [published 9036f74](https://github.com/many-question/ADC-12b-100M/blob/9036f74f024088185398717989ed589784d1d151/design/xtor/adc_comp/many-question-miyahara/BUFFER-V26.txt) and in verified archives. Canonical B20 and its formal failure remain unchanged.
